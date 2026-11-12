# 模組八 素材地圖

> 對象：懂深度學習（訓練/驗證/測試集、loss 曲線、過擬合），沒碰過 NLP／生成式 AI／LangChain。
> 所有 URL 均於 2026-11-12 以 WebFetch 實際開啟核實；打不開（403/404）或需登入者已剔除（見文末「剔除清單」）。
> 注意：WebFetch 只讀得到文字與圖說，讀不到圖片像素。「可借的圖解結構」是依原文段落、圖說與流程文字整理的重畫藍圖。

## 論點清單

1. **LLM 應用是非確定性的多步黑盒，除錯第一步是 tracing**：一次請求 = 一棵 run 樹（trace），每個 LLM 呼叫、檢索、工具執行都是一個節點，各自記延遲、token、輸入輸出；多回合對話再用 thread 串起來。
2. **Eval 就是 LLM 時代的驗證集／測試集**：評測集（dataset）＋評分器（程式規則／LLM-as-judge／人工）＋實驗比較；離線評測擋回歸、線上評測看真實流量。
3. **LLM-as-judge 本身也是一個要被驗證的模型**：先用人工標註（二元 pass/fail ＋理由）當 ground truth，調 judge prompt 直到與人一致；先做錯誤分析（看 trace）再決定要寫哪些 eval，而不是先想像一堆指標。
4. **Vibe Coding ≠ AI 輔助工程**：Vibe coding 是「不看 AI 寫的程式碼」；要進 repo 的程式碼，工程師仍要能審、能測、能解釋。2026 年業界用語已轉向「agentic engineering」。
5. **AI 工程師站在「API 線」的應用側**：不需要訓練基礎模型，但要擁有產品的資料與評測；履歷要寫「拆解了什麼問題、量化改善多少、怎麼驗證」，公開 trace 與 eval 結果就是工程嚴謹度的證據。

## 素材

### 論點 1：Tracing — 把黑盒打開

- **Observability concepts** — LangSmith 官方文件 — https://docs.langchain.com/langsmith/observability-concepts （已核實 2026-11-12）
  - 適合程度：定義短而精準：run 是單一工作單位（一次模型呼叫、一次檢索），「熟悉 OpenTelemetry 的話，run 就是 span」；trace 是單一操作的 run 集合（一棵 run 樹，上限 25,000 個 run）；thread 是多回合對話的 trace 序列（以 `thread_id` metadata 串接）；feedback 是綁在 run 上的 tag + 分數；tags/metadata 用來過濾分組。也說明不用 LangChain 也能追蹤（`@traceable` 裝飾器、`trace` context manager、`RunTree`）。
  - 可借的圖解結構：三層巢狀圖——最外框 Thread（對話 session），裡面三個 Trace（每回合一個），展開其中一個 Trace 成瀑布圖（waterfall）：根 run「agent」底下依時間排列子 run「LLM 呼叫 1（820ms，1.2k tokens）→ tool: search（300ms）→ LLM 呼叫 2（640ms）」，右側欄標延遲與 token。最後在某個 run 上貼一張 feedback 便利貼（👍/分數）。
  - 搭橋：**PyTorch Profiler / TensorBoard 的 trace view**：forward pass 拆成每一層的耗時瀑布圖，找瓶頸的思路完全相同；只是這裡每個「層」是一次 LLM 或工具呼叫，還多了「輸入輸出內容」可看。
- **Introduction to Agent Observability & Evaluations** — LangChain Academy — https://academy.langchain.com/courses/intro-to-langsmith （已核實 2026-11-12；免費，7.5 小時影片／43 課，報名需註冊帳號）
  - 適合程度：官方入門課，Module 1 Tracing（Tracing Basics、Types of Runs、Conversational Threads）→ 2 Testing and Evaluation（datasets、evaluators、experiments）→ 3 Prompt Engineering（Playground、Prompt Hub）→ 4 Human Feedback → 5 Production Observability。剛好涵蓋課綱「追蹤、可視化調試、Prompt 線上微調、回歸測試」全部項目。
  - 可借的圖解結構：課程目錄就是一條「建構 → 測試 → 調 prompt → 收回饋 → 上線監控」的生命週期，可畫成橫向五站的流程條當模組八開場地圖。
  - 搭橋：等同 ML 專案的「訓練 → 驗證 → 調參 → 標註 → 部署監控」流程。
- **Your AI Product Needs Evals** — Hamel Husain，2024-03-29 — https://hamel.dev/blog/posts/evals/ （已核實 2026-11-12）
  - 適合程度：用 Rechat 的房仲助理 Lucy 案例說明「沒有 eval 就會修一個壞一個」；強調要記錄 trace、把看資料的摩擦降到最低（甚至自建檢視工具）、先用二元好/壞標籤。案例中他們用 LangSmith 記 trace，可直接接本模組工具。
  - 可借的圖解結構：見論點 2。此處借用「看 trace 的介面該長什麼樣」：一個畫面放齊使用者輸入、中間步驟、最終輸出、好/壞按鈕與備註欄。
  - 搭橋：「先看資料再調模型」＝訓練前先看幾百張樣本圖、看混淆矩陣裡分錯的樣本。

### 論點 2：Eval ＝ 驗證集／測試集

- **Evaluation concepts** — LangSmith 官方文件 — https://docs.langchain.com/langsmith/evaluation-concepts （已核實 2026-11-12）
  - 適合程度：一頁講清楚 dataset/example（inputs + 可選 reference outputs）、experiment（某版本在整個 dataset 上的輸出＋分數＋trace）、評分器種類（human / code / LLM-as-judge / pairwise）、離線（上線前、可有標準答案）vs 線上（真實流量、沒有標準答案）、回歸測試（新版本不得比 baseline 差）、annotation queue。
  - 可借的圖解結構：頁面內附的生命週期流程（Development → Testing → Deployment → Monitoring → Iteration），Offline 虛線接在前兩站、Online 虛線接在後兩站、兩者都回饋到 Iteration。可重畫成一條水平軸上下兩排標籤：上排「離線：dataset + reference」、下排「線上：production traces、無 reference」。
  - 搭橋：dataset ≈ 驗證集；experiment ≈ 一次 validation run；回歸測試 ≈「新 checkpoint 在 held-out set 上不能比舊的差才部署」；線上評測 ≈ 部署後監控 data drift。
- **Demystifying evals for AI agents** — Anthropic，2026-01-09 — https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents （已核實 2026-11-12）
  - 適合程度：把 agent eval 的術語定義成一套乾淨的詞彙：task、trial（同一 task 多跑幾次，因為輸出有隨機性）、grader、transcript、outcome（環境最終狀態，例如資料庫裡真的有那筆訂位）。三種 grader 各自的優缺點表；capability eval（從低通過率往上爬）vs regression eval（應接近 100%）；建議從 20–50 個取自真實失敗的任務起步。
  - 可借的圖解結構：(a) **pass@k vs pass^k 雙曲線**：k=1 時兩線重合，pass@k 往 100% 爬升、pass^k 往 0% 下滑；標一個數字例子「單次成功率 75% → 連續三次都成功只有 42%（0.75³）」。(b) 瑞士起司模型：多層評測方法疊在一起，每層的洞位置不同，合起來才擋得住失敗。
  - 搭橋：trial 多跑幾次 ≈ 用不同 random seed 重跑實驗看變異數；pass^k 就是獨立事件機率連乘，學生一算就懂為何「demo 能跑」不等於「上線穩定」。
- **Patterns for Building LLM-based Systems & Products** — Eugene Yan（約 2023-08）— https://eugeneyan.com/writing/llm-patterns/ （已核實 2026-11-12）
  - 適合程度：七大模式（Evals、RAG、Fine-tuning、Caching、Guardrails、Defensive UX、User feedback）的總覽地圖，Evals 一節特別適合 DL 學生：從 BLEU / ROUGE / BERTScore 這些傳統指標講起，說明為何它們對開放式生成相關性差，再過渡到 LLM-as-judge 與其偏誤（位置、冗長、自我偏好）。文中提到「Eval Driven Development」。
  - 可借的圖解結構：2×2 定位圖：一軸「靠近資料 ↔ 靠近使用者」，另一軸「提升效能（offensive）↔ 降低成本/風險（defensive）」，七個模式散布其中（Evals、RAG、Fine-tuning 靠資料端；Defensive UX、User feedback 靠使用者端）。可當整門課的「總複習地圖」，把模組三（RAG）、六（微調）、八（Evals）放進同一張圖。
  - 搭橋：BERTScore 用 embedding 相似度取代 n-gram 比對——直接接學生熟悉的 embedding；「傳統指標與人類判斷相關性低」≈ 分類任務中 accuracy 在類別不平衡時失真。

### 論點 3：LLM-as-judge 要校準；錯誤分析先於指標

- **Using LLM-as-a-Judge For Evaluation: A Complete Guide** — Hamel Husain，2024-10-29（2026-09-01 更新）— https://hamel.dev/blog/posts/llm-judge/ （已核實 2026-11-12）
  - 適合程度：「Critique Shadowing」六步驟可直接變成投影片流程：找主要領域專家 → 建多樣化資料集 → 專家做二元 pass/fail ＋寫詳細理由 → 先修明顯錯誤 → 以專家理由當 few-shot 反覆調 judge prompt 直到與專家一致（類別不平衡時看 TPR/TNR，不看原始一致率）→ 在新資料上做錯誤分析。
  - 可借的圖解結構：文中有 mermaid 流程（`graph TB`）：一條主線加三個菱形回圈——「發現錯誤？」回到修錯、「一致率可接受？」回到調 prompt、「發現關鍵問題？」回到專家審查。可直接照這個拓撲重畫。
  - 搭橋：**judge 就是一個分類器，人工標註是 ground truth**，要算 precision/recall、看混淆矩陣；調 judge prompt ≈ 調超參數直到驗證集指標收斂。類別不平衡時不看 accuracy——學生在 DL 課就學過。
- **AI Evals: Everything You Need to Know（Evals FAQ）** — Hamel Husain、Shreya Shankar，2026-09-18 — https://hamel.dev/blog/posts/evals-faq/ （已核實 2026-11-12）
  - 適合程度：目前最完整的 eval 實務 FAQ。三個重點與課綱直接相關：(1) 錯誤分析是「最重要的活動」：open coding（逐條 trace 寫自由筆記）→ axial coding（歸納成失敗分類並計數）；建議先親自標至少 30 條 trace。(2) 偏好二元 pass/fail 而非 1–5 Likert 量表（標註者之間不一致、傾向給中間值）。(3) **「Should I practice eval-driven development? Generally no.」**——LLM 的失敗面無限大，應「為你發現的錯誤寫 evaluator，而不是為你想像的錯誤寫」；例外是成功標準非常明確的約束（例如「絕不提及競品」）。
  - 可借的圖解結構：錯誤分析四步漏斗：一堆 trace → 每條貼自由筆記（open coding）→ 筆記聚類成 5–8 個失敗類別並畫長條圖計數（axial coding）→ 只對最高的幾根長條寫自動 evaluator。
  - 搭橋：axial coding 長條圖 ≈ 把錯分樣本按錯誤類型歸類（標註錯、模糊、少見類別），先修最大宗——DL 的 error analysis 老做法（Andrew Ng 在 ML 課程常講的那套）。
- **Patterns for Building LLM-based Systems & Products（Evals 一節）** — Eugene Yan — https://eugeneyan.com/writing/llm-patterns/ （已核實 2026-11-12）
  - 適合程度：LLM-as-judge 三種偏誤與對策寫得最簡潔：位置偏誤（交換順序、兩次都贏才算）、冗長偏誤（長度要相近）、自我偏好（不要用同一個模型評自己）。
  - 可借的圖解結構：三列表格「偏誤 → 現象 → 對策」，每列配一個 A/B 回答卡片示意。
  - 搭橋：等同資料洩漏／評估偏誤的防範——不要用訓練集評測、不要讓模型「自己出題自己改」。

### 論點 4：Vibe Coding vs AI 輔助工程

- **Not all AI-assisted programming is vibe coding (but vibe coding rocks)** — Simon Willison，2025-03-19 — https://simonwillison.net/2025/Mar/19/vibe-coding/ （已核實 2026-11-12）
  - 適合程度：引用 Karpathy 原始定義（「fully give in to the vibes, embrace exponentials, and forget that the code even exists」），並把 vibe coding 收斂為「用 LLM 寫軟體但不審查它寫的程式碼」；他自己的規則是「我不會 commit 任何我無法向別人解釋清楚的程式碼」。同時肯定 vibe coding 適合低風險原型與學習。
  - 可借的圖解結構：一條光譜：左端「Vibe coding：不看程式碼、只看結果能不能跑」→ 中段「AI 寫、人審、人測」→ 右端「人寫、AI 補全」。在光譜上標兩條線：「可以拿去 demo」「可以 commit 進 repo」。
  - 搭橋：跟「只看 loss 下降、不看預測結果」一樣危險——指標好看不代表模型學到對的東西（shortcut learning）。
- **Karpathy said vibe coding is obsolete** — Jeff Gothelf，2026-05-25 — https://jeffgothelf.com/blog/karpathy-said-vibe-coding-is-obsolete/ （已核實 2026-11-12）
  - 適合程度：作為「2026 年業界用語已變」的佐證：報導 Karpathy 在 Sequoia AI Ascent（2026 年 5 月）說 vibe coding「already obsolete」、未來是「agentic engineering」，並轉述 agentic engineering 的七項工作：寫設計規格、監督計畫、檢查 diff、寫測試、建評測迴圈、管理權限、守住品質。注意這些是作者轉述，非 Karpathy 逐字原話。
  - 可借的圖解結構：七項工作排成一圈「工程師仍然擁有的責任」環形圖，中間是「AI 負責實作」。另加時間軸：2025-02 Karpathy 在 X 提出 vibe coding → 2026-02 發文說已過時、偏好「agentic engineering」（二手報導）→ 2026-05 Sequoia 演講。
  - 搭橋：七項裡的「建評測迴圈」「寫測試」直接回扣論點 2–3，讓 Vibe Coding 段落和 Eval 段落接成一個故事。
  - 注意：The New Stack 原文回應 403 已剔除；Karpathy 原始 X 貼文無法以 WebFetch 讀取，上投影片前建議講師自行截圖確認原句。

### 論點 5：AI 工程師的定位與履歷

- **The Rise of the AI Engineer** — swyx（Latent Space），2023-06-30 — https://www.latent.space/p/ai-engineer （已核實 2026-11-12）
  - 適合程度：定義「AI Engineer」這個職稱的經典文章。核心是「API 線」：線的一側是 ML 研究員／ML 工程師（預訓練、通用 benchmark），另一側是 AI 工程師（在 API 之上做產品，擁有產品特定的資料與 eval）；不需要博士，Karpathy 被引述說可以「without ever training anything」就勝任。
  - 可借的圖解結構：水平光譜「ML Researcher — ML Engineer —｜API 線｜— AI Engineer — Full-stack Engineer」，線兩側分別列出工作內容（左：預訓練、資料規模、通用 benchmark；右：prompt、RAG、agent、產品 eval）。可直接改造成課綱的「AI 產業三層架構」圖，把第二層（應用層）對準 AI Engineer 區段。
  - 搭橋：**這群學生的優勢在於跨在 API 線兩側**：懂反向傳播、微調（模組六），也能做應用——履歷要強調這個「能往線左側延伸」的差異化。
- **AI Engineering（書）配套 repo** — Chip Huyen — https://github.com/chiphuyen/aie-book （已核實 2026-11-12）
  - 適合程度：免費的章節摘要、學習筆記、案例研究、資源清單，可作為「AI 工程師該會什麼」的權威能力清單；書中問題清單包含「怎麼評測我的應用」「什麼是 agent、怎麼建與評測」。
  - 可借的圖解結構：以書的目錄做一張「能力雷達圖」：基礎模型理解、評測、prompt、RAG/agent、微調、資料、推論優化、架構與回饋——讓學生標出自己上完本課後的位置。
  - 搭橋：—
- **Practical guide to writing FAANG-ready software engineer resumes** — Yangshun Tay（Tech Interview Handbook）— https://www.techinterviewhandbook.org/resume/ （已核實 2026-11-12）
  - 適合程度：工程師履歷的通用原則，非 AI 專屬但可信度高：成就要可量化；給出「[成就摘要]：[行動] that resulted in [可量化結果]」模板；至少放 2 個專案並附 GitHub 連結。
  - 可借的圖解結構：Before/After 對照卡：Before「熟悉 LangChain、會調用 OpenAI API」；After「以 LangGraph 設計含人工審批的 SQL agent：導入 checkpointer 中斷恢復，敏感操作 100% 經審批；以 40 題回歸評測集將錯誤 SQL 率由 X% 降至 Y%（附 LangSmith 公開 trace）」。（數字留空由學生填自己的實測值）
  - 搭橋：寫履歷 ≈ 寫論文的 results 段：方法 + 指標 + 對照組，沒有 baseline 的數字沒有意義。

## 事實核實

- **LangSmith 功能（追蹤、可視化調試、Prompt 線上微調、回歸測試）**：皆存在。Tracing 概念（run/trace/thread/feedback）見 https://docs.langchain.com/langsmith/observability-concepts ；評測（dataset、experiment、LLM-as-judge、pairwise、回歸測試、annotation queue）見 https://docs.langchain.com/langsmith/evaluation-concepts ；Prompt 調整對應的是 Playground 與 Prompt Hub（https://academy.langchain.com/courses/intro-to-langsmith Module 3）。Python SDK `langsmith` 最新 0.14.17（2026-11-02，https://pypi.org/project/langsmith/ ）。課綱「Prompt 在線微調」用詞易被誤解為模型微調，應寫「Prompt 線上調試（Playground）」。
- **公開 Trace 鏈接（Lab 8）**：LangSmith 支援分享 trace，但本次只核實到概念文件，未逐頁核對「公開分享」操作頁；製作 Lab 講義前需再確認目前 UI 流程。
- **LangChain Chat-UI**：正式名稱 **Agent Chat UI**（`langchain-ai/agent-chat-ui`，`npx create-agent-chat-app`）。**GitHub repo 已於 2026-11-03 封存為唯讀**（GitHub API `archived: true`），官方文件 https://docs.langchain.com/oss/python/langchain/ui 目前仍推薦，託管版 agentchat.vercel.app 仍在；未見官方後繼專案。**和課綱不一致**：名稱錯，且課程若要長期使用，需準備替代方案或 fork 版本。
- **WorkBuddy 是否真實存在**：**存在**，但定位與課綱不符。WorkBuddy 是騰訊雲的「全場景 AI 辦公工作台」（desktop agent，涵蓋日常辦公、程式開發、設計），2026 年初於中國推出、2026-05-29 推向全球（https://intl.cloud.tencent.com/products/workbuddy 、https://technode.com/2026/05/29/tencent-launches-workbuddy-productivity-ai-agent-for-global-users/ ）。它主打辦公自動化（報告、試算表、簡報、檔案處理、透過 MCP 串 GitHub/Jira 等），**不是**和 Cursor 同類的程式碼編輯器；騰訊的程式開發 agent 是 **CodeBuddy**（依二手報導，未取得官方頁面核實）。課綱把「Cursor、WorkBuddy」並列為 Vibe Coding 研發工具，應改為 Cursor / Claude Code / CodeBuddy 等程式碼 agent，或明講 WorkBuddy 是辦公類 agent。
- **Vibe Coding 一詞**：Karpathy 於 2025-02-02 在 X 提出（多個二手來源一致；Simon Willison 原文引述其定義）。2026 年 2 月 Karpathy 表示偏好改稱「agentic engineering」（二手報導，原始貼文未能直接讀取），2026 年 5 月 Sequoia AI Ascent 演講再稱 vibe coding「already obsolete」（https://jeffgothelf.com/blog/karpathy-said-vibe-coding-is-obsolete/ ，作者轉述）。課綱稱「2026 年興起的 Vibe Coding」**時間不正確**：該詞興起於 2025 年，到 2026 年已被提出者本人視為過時用語。
- **Eval-driven development**：Eugene Yan 文中以正面語氣提到「Eval Driven Development」；但 Hamel Husain 與 Shreya Shankar 的 2026 年 Evals FAQ 明確回答「Generally no」，主張先做錯誤分析、再為已發現的錯誤寫 evaluator（https://hamel.dev/blog/posts/evals-faq/ ）。課綱未直接寫 EDD，但任務需求提到；投影片若要講，需呈現兩派觀點。
- **AI 產業三層架構**：非任何權威來源的固定框架，屬課綱自行歸納；最接近的權威說法是 swyx 的「API 線」（https://www.latent.space/p/ai-engineer ）。引用時不要寫成業界共識。

## 投影片建議

1. **把 Eval 直接框成「驗證集」。** 這群學生最熟的就是 train/val/test 切分與「不能在測試集上調參」。一張對照表（val set ↔ eval dataset、val loss ↔ evaluator 分數、新 checkpoint 不能變差 ↔ 回歸測試、部署監控 data drift ↔ 線上評測）可以省掉半小時的概念鋪陳，剩下時間留給「LLM 輸出沒有唯一正確答案，所以評分器本身也要被驗證」這個真正的新觀念。
2. **LLM-as-judge 用「它也是個分類器」來教，並補上錯誤分析。** 課綱只寫「回歸測試評估」，缺了最實用的一步：先親自看 30+ 條 trace 做錯誤分類，再決定寫哪些 evaluator。用 Hamel 的 open/axial coding 漏斗圖，加上「judge vs 人工標註的混淆矩陣」，學生會覺得是 DL 老功夫換場景。
3. **Vibe Coding 段落改名、改框架。** 「2026 年興起的 Vibe Coding」時間錯，而且提出者本人已改稱 agentic engineering。建議標題改為「AI 輔助開發：從 Vibe Coding 到 Agentic Engineering」，用 Simon Willison 的「能解釋才 commit」當核心規則；工具清單拿掉 WorkBuddy（辦公 agent），改放實際的程式碼 agent。
4. **Lab 8 的前端不要綁 Agent Chat UI。** repo 剛封存（2026-11-03），學生照著 `npx create-agent-chat-app` 可能還能跑，但遇到問題不會再有修復。建議改用 LangSmith Studio 做互動除錯展示，或預先 fork 一份固定版本給學生。
5. **「三層架構」改用 swyx 的 API 線圖，並強調這群學生的差異化。** 課綱把第一層寫成「HC 稀缺、門檻極高」、第三層「極易被替代」，資訊量低且偏情緒。換成 API 線光譜圖後可以講出具體的定位：這群學生懂反向傳播與微調，是少數能從應用側往模型側延伸的人，履歷要把模組六（LoRA）與模組八（eval 數據）放在同一個專案敘事裡。

## 剔除清單

- The New Stack《Vibe coding is passé》— https://thenewstack.io/vibe-coding-is-passe/ — 回應 HTTP 403。
- Tencent Cloud Techpedia「What is WorkBuddy?」— https://www.tencentcloud.com/techpedia/142834 — 回應 HTTP 404。
- 各家履歷產生器／求職網站的「AI Engineer Resume Guide」（careery.pro、resumegeni.com 等）— 內容為廠商行銷，數據無獨立來源，不採用。
