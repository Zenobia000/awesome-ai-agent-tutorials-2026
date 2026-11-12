# 模組二 素材地圖

> 對象：懂深度學習，已上完模組一（知道 LLM 是逐 token 的 softmax 分類器、模型無狀態、輸入是一條攤平的 token 序列）。
> 用途：參考下列來源的「圖解結構」自己重畫，不搬圖。所有網址於 2026-11-12 以 WebFetch 實際抓取核實。

## 論點清單

1. **提示詞是模型的「輸入規格」，結構化之後才可維護、可測試**：角色／指令／範例／背景分區，用 Markdown 標題與 XML 標籤劃邊界；few-shot 是在輸入端示範輸出分佈，不改權重。
2. **CoT 有效是因為「多生成的 token = 多出來的計算步驟」；ToT 是在這之上加搜尋。推理模型把 CoT 內建了，手寫「一步步想」不再必要**：提示詞的重心從「教模型怎麼想」轉到「定義成功條件、讓程式評估路徑」。
3. **Prompt injection 的根源是指令與資料在同一條 token 序列裡，沒有型別系統可以區分**：XML 隔離只能降低機率，不能根除；生產環境要靠縱深防禦（輸入篩檢、輸出驗證、最小權限、人工核准）。
4. **Structured outputs 用約束解碼保證輸出符合 JSON Schema；Pydantic 一端產生 schema、一端驗證結果**：tool calling 是同一機制套在「模型提出呼叫、程式執行」的迴圈上。保證的是格式，不是內容正確。
5. **Text2SQL 是上面四點的綜合題**：schema（DDL）當背景放進提示詞、few-shot 範例、Pydantic 結構化輸出、再用非 AI 的檢查（解析、dry run、唯讀帳號）兜底。

## 素材

### 論點 1：提示詞的工程化結構

- **Prompt engineering（Message formatting 一節）** — OpenAI API 文件 — https://developers.openai.com/api/docs/guides/prompt-engineering（已核實 2026-11-12）
  - 適合程度：官方直接給出 developer message 的四段式結構 **Identity → Instructions → Examples → Context**，並建議 Markdown 標題分段、XML 標籤包住文件與使用者輸入。和課綱四區塊幾乎一一對應，可當「業界標準」的出處。
  - 可借的圖解結構：一個長方形的 system prompt，切成四條橫帶（Identity／Instructions／Examples／Context），每條帶左側一個圖示、右側一行用途；最底下另一個顏色的方塊 `<user_query>` 標示「外部輸入，與上面隔開」。
  - 搭橋：函式簽章與 docstring——Identity/Instructions 是函式說明，Examples 是單元測試，Context 是參數。
- **Prompting best practices** — Anthropic（Claude API 文件）— https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices（已核實 2026-11-12；舊的 use-xml-tags 等子頁已整併到這頁）
  - 適合程度：「Give Claude a role」「Use examples effectively（3–5 個、包在 `<example>` 裡）」「Structure prompts with XML tags」「長文件放最上面、問題放最後」各自一節，每節有短範例。
  - 可借的圖解結構：長上下文排版圖——上方是多個 `<document>`（含 `<source>`、`<document_content>`）堆疊，中間 `<instructions>`，最下方一行問題；旁邊標「資料在上、問題在下」。
  - 搭橋：few-shot ＝ in-context 的「示範資料」，與訓練資料不同的是不經反向傳播、只影響這次推論的條件分佈。
- **Prompt Engineering Interactive Tutorial** — Anthropic（GitHub）— https://github.com/anthropics/prompt-eng-interactive-tutorial（已核實 2026-11-12；內容以 Claude 3 寫成，官方文件註明與 best practices 衝突時以後者為準）
  - 適合程度：9 章由淺入深，第 3 章角色、第 4 章「Separating Data from Instructions」、第 7 章 few-shot、第 8 章避免幻覺，正好可拆成課堂練習題。
  - 可借的圖解結構：每章的「壞提示 → 好提示」左右對照格式，適合做成投影片的 before/after 頁。
  - 搭橋：A/B 實驗，固定模型只改輸入，看輸出變化。
### 論點 2：CoT／ToT 與推理模型時代的轉變

- **Chain-of-Thought Prompting** — DAIR.AI Prompt Engineering Guide — https://www.promptingguide.ai/techniques/cot（已核實 2026-11-12）
  - 適合程度：few-shot CoT（Wei 2022）→ zero-shot CoT「Let's think step by step」（Kojima 2022）→ Auto-CoT 三段演進，例子是算蘋果這種小學數學，零門檻。
  - 可借的圖解結構：同一題左右兩欄——左欄直接答（錯），右欄先寫推理步驟再答（對）；推理步驟用淺色字標「多花的 token」。
  - 搭橋：模型每生成一個 token 只做一次前向傳播；讓它先寫推理，就是給它更多層「可寫回的中間結果」，類似把一個深網路展開成更多步。
- **Tree of Thoughts (ToT)** — DAIR.AI Prompt Engineering Guide — https://www.promptingguide.ai/techniques/tot（已核實 2026-11-12）
  - 適合程度：用 24 點遊戲說明「每步產生多個候選 → 模型自評 sure/maybe/impossible → BFS/DFS 保留前 5 個」，並收錄單一提示詞版本（三位專家輪流發言）。
  - 可借的圖解結構：一棵三層的樹，每個節點是一步部分解，節點顏色標自評結果（綠／黃／紅），紅色節點剪枝；旁邊並排一條直線代表 CoT，凸顯「一條路 vs 搜尋」。
  - 搭橋：beam search（模組一講過）與搜尋演算法；ToT 是把 beam search 從 token 層級提升到「想法」層級，評分函數由模型自己扮演。
- **Reasoning best practices** — OpenAI API 文件 — https://developers.openai.com/api/docs/guides/reasoning-best-practices（已核實 2026-11-12）
  - 適合程度：官方明寫對推理模型下「think step by step」是不必要的，甚至可能有害；建議先 zero-shot、需要時才加範例、明確寫出限制與成功條件。可當「CoT 角色演變」這一頁的權威出處。
  - 可借的圖解結構：兩欄對照表「一般模型 vs 推理模型」——CoT 指令（有用／不必要）、few-shot（常需要／先不要）、提示詞長度（詳細／簡潔＋成功條件）。
  - 搭橋：把評估標準寫清楚，類似先定義 loss 再訓練。
### 論點 3：Prompt injection 的本質與防禦

- **Delimiters won't save you from prompt injection** — Simon Willison — https://simonwillison.net/2023/May/11/delimiters-wont-save-you/（已核實 2026-11-12）
  - 適合程度：短文，一個例子就打破「用分隔符號包起來就安全」：攻擊者在被包住的文字裡先寫一段假摘要，假裝任務完成，再下新指令，模型就照做。核心句是「模型看到的只是一條扁平的 token 序列」，和模組一的論點完全接得上。
  - 可借的圖解結構：系統指令（藍）與使用者文字（橘）在人眼中有框線分隔；下方同一段內容被攤平成一排 token 方塊，顏色全部變灰——「模型眼中沒有顏色」。
  - 搭橋：模組一的 chat template 攤平圖；對比 SQL injection 有參數化查詢可解，LLM 目前沒有對等的「型別分離」。
- **LLM01:2025 Prompt Injection** — OWASP GenAI Security Project — https://genai.owasp.org/llmrisk/llm01-prompt-injection/ ；總表 https://genai.owasp.org/llm-top-10/（已核實 2026-11-12）
  - 適合程度：權威、條列清楚，區分直接注入與間接注入，列出 7 項緩解措施（限制模型行為、驗證輸出格式、輸入輸出過濾、最小權限、高風險動作人工核准、隔離並標示外部內容、對抗測試），並明說「目前不清楚有沒有萬無一失的防法」。
  - 可借的圖解結構：兩條攻擊路徑——(a) 使用者直接輸入惡意指令；(b) 使用者無害，惡意指令藏在網頁／文件／工具回傳裡流進模型。下方一排 7 個盾牌代表緩解層。
  - 搭橋：資安的 defense in depth；把 LLM 當成「不可信的使用者」看待。
- **Mitigate jailbreaks and prompt injections** — Anthropic（Claude API 文件）— https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks（已核實 2026-11-12）
  - 適合程度：比 OWASP 更貼近實作，每項防禦都附提示詞或 JSON 範例：用小模型 + structured output 做 harmlessness screen、不可信內容只放 tool result、JSON-encode 不可信字串（攻擊者無法「閉合標籤」跳出）、最小權限。
  - 可借的圖解結構：多層管線——使用者輸入 → 小模型篩檢（輸出 `{"is_harmful": bool}`）→ 主模型（system prompt 含 `<untrusted_content_policy>`）→ 輸出驗證 → 執行；每層旁標「擋什麼」。
  - 搭橋：分類器當前置過濾器（學生熟悉的二元分類）；structured output 讓篩檢結果可被程式分支判斷，接論點 4。
### 論點 4：Structured outputs、tool calling 與 Pydantic

- **Structured Outputs** — OpenAI API 文件 — https://developers.openai.com/api/docs/guides/structured-outputs（已核實 2026-11-12）
  - 適合程度：有一張 JSON mode vs Structured Outputs 的比較表（JSON mode 只保證是合法 JSON，Structured Outputs 才保證符合 schema），並說明「function calling 用於呼叫你的工具；`json_schema` 格式用於回覆使用者」的分工；Python SDK 可直接吃 Pydantic。明講 refusal 與截斷時輸出可能不符 schema。
  - 可借的圖解結構：三層階梯「純文字提示要 JSON → JSON mode → Structured Outputs（strict）」，每階標「保證程度」與「會失敗的情況」。
  - 搭橋：模型輸出本來就是 token 機率分佈；約束解碼＝每一步把不符合語法的 token 機率遮成 0 再 softmax（和模組一 attention mask 設 −∞ 同一招）。
- **Structured outputs** — Anthropic（Claude API 文件）— https://platform.claude.com/docs/en/build-with-claude/structured-outputs（已核實 2026-11-12）
  - 適合程度：明寫機制：schema 被編譯成文法，以 constrained decoding 約束輸出；首次使用有編譯延遲、快取 24 小時；列出不支援的 schema 特性（遞迴、數值上下限、字串長度）。Python 範例 `client.messages.parse(..., output_format=ContactInfo)` 直接回傳 Pydantic 物件。
  - 可借的圖解結構：Pydantic class → JSON Schema → 文法（grammar）→ 解碼時逐 token 遮罩 → 合法 JSON → `parsed_output`（Pydantic 物件）的環形流程；在「遮罩」那一步放一個小長條圖，部分長條被打叉。
  - 搭橋：同上；另外點出 Pydantic 的數值範圍等限制要靠「解析後」驗證，不是解碼時保證。
- **Function calling** — OpenAI API 文件 — https://developers.openai.com/api/docs/guides/function-calling（已核實 2026-11-12）
  - 適合程度：五步流程講得最清楚：送出 tools 定義 → 模型回 `function_call`（名稱 + JSON 參數）→ 你的程式執行 → 回傳 `function_call_output` → 模型產出最終答案。並說明 `strict: true` 的條件（`additionalProperties: false`、所有欄位列在 `required`、可選欄位用 null）。
  - 可借的圖解結構：左「你的程式」右「模型」兩條垂直泳道，五支來回箭頭編號 1–5；第 3 步「執行」只發生在左側，強調模型從不自己執行任何東西。
  - 搭橋：模型只是輸出一段「結構化的意圖」，執行權在程式；為模組五的 Agent 迴圈埋伏筆。
### 論點 5：Text2SQL 綜合實作

- **Getting AI to write good SQL: Text-to-SQL techniques explained** — Per Jacobsson, Google Cloud Blog（2025-05-17）— https://cloud.google.com/blog/products/databases/techniques-for-improving-text-to-sql（已核實 2026-11-12）
  - 適合程度：業界實作視角、不講公式。四個技巧剛好對應本模組：schema linking（只挑相關表與欄位放進提示詞）、few-shot（業務與 SQL 方言範例）、self-correction（先用解析器與 dry run 這類非 AI 檢查，把錯誤回饋給模型重寫）、disambiguation（問題不明確時反問使用者）。附 BigQuery vs MySQL 方言對照。
  - 可借的圖解結構：管線圖——自然語言問題 → 檢索相關 schema → 組提示詞（DDL + few-shot + 問題）→ LLM → SQL → 解析／dry run → 失敗則帶錯誤回到 LLM，成功則執行；旁支「問題模糊 → 反問使用者」。
  - 搭橋：論點 1（DDL 是 Context）、論點 4（輸出用 Pydantic 收）、論點 3（SQL 本身就是要防注入的輸出，要用唯讀帳號 + 語句白名單兜底）。
## 事實核實

- **OpenAI Moderation API**：✅ 仍在服務。模型名 `omni-moderation-latest`，**免費**，支援文字與圖片（不支援音訊），13 個類別（harassment、hate、illicit、self-harm、sexual、violence 及其子類）；頁面無棄用公告，但說明底層模型會持續更新，用 `category_scores` 自訂門檻需定期重新校準。舊的 `text-moderation-*` 已於 2025-10-27 關閉。出處：https://developers.openai.com/api/docs/guides/moderation 、https://developers.openai.com/api/docs/deprecations
  - 補充：本地／內網情境可考慮 Ollama 上的 `gpt-oss-safeguard`（已列於 Ollama library），或依 Anthropic 文件做法用小模型 + structured output 自建篩檢器。出處：https://ollama.com/library 、https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks
- **OpenAI Structured Outputs**：✅ 支援。Responses API 用 `text.format` + `json_schema` + `strict: true`；function calling 亦可 `strict: true`；Python SDK 支援 Pydantic；首次使用新 schema 有額外延遲；refusal 走獨立 `refusal` 欄位，可能不符 schema；輸出被 max tokens 截斷時也可能不完整。出處：https://developers.openai.com/api/docs/guides/structured-outputs 、https://developers.openai.com/api/docs/guides/function-calling
- **Anthropic Claude Structured Outputs**：✅ 已 GA（Claude API、Bedrock、Google Cloud、Microsoft Foundry）。參數為 `output_config.format`（`type: "json_schema"`），舊的 beta 參數 `output_format` 已棄用；工具上設 `strict: true` 為 strict tool use；Python SDK `client.messages.parse()` 接受 Pydantic。機制為 constrained decoding。`stop_reason` 為 `refusal` 或 `max_tokens` 時輸出可能不符 schema。出處：https://platform.claude.com/docs/en/build-with-claude/structured-outputs
- **Ollama Structured Outputs**：✅ 原生 API 的 `format` 參數可傳 JSON Schema；OpenAI 相容端點可用 `response_format`（文件未附範例）；Ollama 雲端目前不支援；`/v1/chat/completions` 不支援 `tool_choice`。出處：https://docs.ollama.com/capabilities/structured-outputs 、https://docs.ollama.com/api/openai-compatibility
- **「百分之百穩定度輸出符合 Schema」**：⚠️ 需加但書。三家文件都寫明：約束解碼保證的是「完成且未拒答」的輸出符合 schema；拒答、達到 max tokens 截斷、API 錯誤仍要處理；schema 表達不了的業務規則（數值範圍、SQL 是否只讀）要在程式端驗證。
- **DeepSeek-R1 作為「原生自反思模型」**：✅ 描述合理。R1 以 RL 訓練出先產生 thinking tokens 再回答的行為。但官方對 R1 distill 的使用建議是**不要用 system prompt、指令全放 user prompt、temperature 0.6**，與本模組「角色設定放 system prompt」的標準結構相衝突，Lab 若用 R1 distill 需改寫。出處：https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-8B 、https://newsletter.languagemodels.co/p/the-illustrated-deepseek-r1
- **推理模型與 CoT**：OpenAI 官方指引：對推理模型下「think step by step」不必要，可能有害；建議先 zero-shot。出處：https://developers.openai.com/api/docs/guides/reasoning-best-practices
- **OWASP Top 10 for LLM Applications**：目前最新為 **2025 版**，Prompt Injection 為 LLM01:2025；頁面未見 2026 版或獨立的 Agentic Top 10 清單（有 Agentic Security 計畫）。出處：https://genai.owasp.org/llm-top-10/
- **XML 標籤隔離**：OpenAI 與 Anthropic 官方都建議用 XML 標籤劃分輸入區塊（出處同論點 1）；但 OWASP 與 Simon Willison 都明說分隔符號無法徹底防止注入。Anthropic 對不可信內容的最新建議是放進 tool result 並 JSON-encode。出處：https://simonwillison.net/2023/May/11/delimiters-wont-save-you/ 、https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks

## 投影片建議

1. **「XML 標籤硬隔離」不要講成「防禦方案」，要講成「降低機率的第一層」**。課綱踩坑表寫「工程防禦必須使用 XML 標籤將外部輸入與系統指令硬隔離」，容易讓學生以為這樣就安全。建議：先用模組一的「攤平 token 序列」圖說明為什麼分隔符號擋不住（Willison 的假摘要例子當場示範），再給 OWASP／Anthropic 的多層防禦，Text2SQL 最後一道防線是**資料庫唯讀帳號**，而不是提示詞裡寫「嚴禁 DROP」。
2. **刪掉或降級「LangChain OutputParser 正則清理」**。三家主流 API 與 Ollama 都已有原生 structured outputs，正則清理是 2023 年的做法。建議排序：原生 structured outputs／strict tool calling → 不支援時用 Instructor（https://python.useinstructor.com/ ，已核實 2026-11-12，支援 Ollama）這類「驗證失敗自動重試」→ 最後才是字串清理。
3. **「百分之百」改成「格式保證，內容不保證」**，並明列三個仍會失敗的情況：拒答、截斷、業務規則（schema 表達不了的限制）。Lab 2 的 `SQLGenerationResult` 裡「安全性風險評級」是模型自評，不能拿來當安全閘門，要另寫程式判斷 SQL 語句類型。
4. **CoT/ToT 用「多算幾步」解釋，並把推理模型的轉變講成「CoT 從提示詞技巧變成訓練出來的能力」**。對懂 DL 的學生，「每個 token 一次前向傳播，多寫推理＝多給運算步數」比「讓模型像人一樣思考」好懂；ToT 直接說成「把 beam search 搬到想法層級」。同時提醒：用推理模型時別再加「一步步想」，改寫清楚的成功條件。
5. **Lab 若用本地 R1 distill，提示詞結構要調整**。R1 distill 官方建議不用 system prompt、temperature 0.6，與本模組的角色區塊與模組一的「temperature 置 0」都衝突。建議 Lab 2 以支援 structured outputs 與 tool calling 的通用模型（如 Ollama 上的 `qwen3`／`qwen3.5`，或雲端 `deepseek-flash`）為主，R1 distill 只拿來示範「推理模型的思考 token」。
