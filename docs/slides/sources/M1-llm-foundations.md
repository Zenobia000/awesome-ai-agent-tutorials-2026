# 模組一 素材地圖

> 對象：懂深度學習（MLP、softmax、反向傳播、embedding 層、遷移學習），沒學過 NLP／生成式 AI。
> 用途：參考下列來源的「圖解結構」自己重畫，不搬圖。所有網址於 2026-11-12 以 WebFetch 實際抓取核實。

## 論點清單

1. **文字進模型前要先變成整數，再查表變成向量**：tokenization 把字串切成 subword、對到詞表 id；embedding 層就是 one-hot × 權重矩陣的查表，跟 DL 裡的 `nn.Embedding` 是同一個東西。
2. **語言模型 = 詞表上的 softmax 分類器，生成 = 把分類器跑成迴圈**：每一步輸出「下一個 token」的機率分佈，抽一個接回輸入再跑一次；temperature／top-p 只是在這個 softmax 上動手腳。
3. **Attention 是為了解決 RNN 的瓶頸，本質是「依內容決定權重的加權平均」**：RNN 把整句壓進一個固定向量又只能循序算；self-attention 讓每個 token 用 Q·K 打分、softmax、對 V 加權，可平行計算。
4. **Transformer 一層 = attention + MLP，外加殘差與 LayerNorm；代價是 O(N²)**：attention 矩陣是 N×N，所以 context window 有上限、長上下文又慢又貴。
5. **模型本身無狀態，「記得對話」是每次把整段歷史重送一遍**：chat 介面背後是把 messages 串成一條 token 序列；超出 context window 的內容模型根本看不到。
6. **聊天模型是「預訓練 → 指令微調 → 偏好對齊」的遷移學習產物；部署上分開源權重與 API，兩者都能用 OpenAI 相容介面呼叫**：Ollama 在本機提供 `/v1` 端點，換 base_url 就能在本地與雲端間切換。

## 素材

### 論點 1：文字 → token id → embedding 向量

- **Tokenizers（LLM Course 第 2 章）** — Hugging Face — https://huggingface.co/learn/llm-course/chapter2/4（已核實 2026-11-12）
  - 適合程度：用「word-based → character-based → subword」三段比較，講清詞表大小與 OOV 的取捨，再接到 `convert_tokens_to_ids()`。沒有 NLP 術語門檻。另有簡中完整譯本（https://huggingface.co/course/zh-CN/chapter1/1）。
  - 可借的圖解結構：同一句話三種切法上下並排（整詞方塊／單字元方塊／subword 方塊），每列右側標「詞表大小 vs 序列長度」；最後一列 subword 方塊下方對應整數 id。
  - 搭橋：分類任務的 label encoding；詞表大小 = 最後一層 softmax 的類別數（埋伏筆給論點 2）。
- **Let's build the GPT Tokenizer** — Andrej Karpathy（YouTube）— https://www.youtube.com/watch?v=zduSFxRajkE（已核實 2026-11-12）
  - 適合程度：從 bytes 開始手寫 BPE，懂 Python 就跟得上；可只剪前 15 分鐘「為什麼 tokenization 是很多怪問題的根源」（拼字、算術、非英文更貴）。
  - 可借的圖解結構：BPE 合併過程做成逐步動畫——字元序列 → 找最常出現的相鄰對 → 合併成新方塊 → 詞表 +1，重複。
  - 搭橋：資料前處理；中文 token 數比英文多 → 直接影響成本與 context 用量（接論點 4）。
- **The Illustrated Word2vec** — Jay Alammar — https://jalammar.github.io/illustrated-word2vec/（已核實 2026-11-12）
  - 適合程度：從「用 5 個人格分數描述一個人」開始，再推到詞向量，完全不需 NLP 背景；king − man + woman ≈ queen 是最好記的 embedding 直覺。
  - 可借的圖解結構：(a) 每個詞畫成一條 50 格的色條（紅＝正、藍＝負），king/man/woman/queen 上下對齊，讓學生看出共同色帶；(b) Embedding 矩陣與 Context 矩陣兩張表、取兩列做點積再過 sigmoid 的訓練示意。
  - 搭橋：one-hot × 權重矩陣 = 查表 = `nn.Embedding`；embedding 是「用反向傳播學出來的特徵」，跟 CNN 學出 filter 同理。

### 論點 2：LLM = 詞表上的 softmax 分類器；逐字生成與採樣

- **Large Language Models explained briefly** — 3Blue1Brown（YouTube，約 8 分鐘）— https://www.youtube.com/watch?v=LPZh9BOjkQs（已核實 2026-11-12）
  - 適合程度：整個系列的入口短片，「模型只是在預測下一個詞」這個核心講得最乾淨，適合當開場。
  - 可借的圖解結構：一句未完的句子 → 右側長條圖列出候選詞與機率 → 抽中的詞接到句尾，畫面左移、重複。
  - 搭橋：影像分類器輸出 1000 類機率；這裡類別換成 ~5 萬～15 萬個 token。
- **Transformers, the tech behind LLMs（Deep Learning Chapter 5）** — 3Blue1Brown（Grant Sanderson）— https://www.3blue1brown.com/lessons/gpt ；影片 https://www.youtube.com/watch?v=wjZofJX0v4M（已核實 2026-11-12）
  - 適合程度：同時有文字版與影片，從 token → embedding 矩陣 W_E → 最後的 unembedding 矩陣 W_U → softmax 一路講完，還直接講 temperature 公式。對懂 softmax 的學生是最順的一條路。
  - 可借的圖解結構：(a) W_E 畫成「一欄一個詞」的大矩陣，W_U 是它的轉置形狀；(b) softmax 前後兩組長條圖對照，加一個 T 滑桿，T 大 → 長條趨平、T→0 → 只剩最高那根。
  - 搭橋：softmax(z/T) 就是知識蒸餾裡的溫度；W_U 就是分類器最後一層 Linear。
- **How to generate text: using different decoding methods** — Patrick von Platen, Hugging Face — https://huggingface.co/blog/how-to-generate（已核實 2026-11-12）
  - 適合程度：greedy／beam／sampling／temperature／top-k／top-p 各配一張樹狀或長條圖，逐個比較，是講採樣參數最完整的單篇。
  - 可借的圖解結構：top-k vs top-p 並排兩張長條圖——top-k 固定砍到前 k 根；top-p 依累積機率畫一條水平虛線，分佈尖時只留 2 根、分佈平時留很多根。
  - 搭橋：機率分佈、抽樣；beam search 類似在決策樹上做有限寬度搜尋。
### 論點 3：RNN 瓶頸 → attention 直覺 → self-attention Q/K/V

- **Visualizing A Neural Machine Translation Model (Seq2seq Models With Attention)** — Jay Alammar — https://jalammar.github.io/visualizing-neural-machine-translation-mechanics-of-seq2seq-models-with-attention/（已核實 2026-11-12）
  - 適合程度：學生懂 RNN 就能看。文中直接寫出「context vector 是瓶頸」，再示範 attention 怎麼解。這篇是「為什麼需要 attention」的最佳前導。
  - 可借的圖解結構：(a) encoder 一格一格吃字，最後只把一個向量交給 decoder（畫成細窄的漏斗）；(b) 改成把所有 hidden state 都交出去，decoder 每步對它們打分 → softmax → 加權和；(c) 翻譯對齊熱圖（European Economic Area 語序反轉）。
  - 搭橋：RNN／LSTM 的長距依賴與梯度消失；循序計算無法平行。
- **Attention in transformers, step-by-step（Deep Learning Chapter 6）** — 3Blue1Brown — https://www.3blue1brown.com/lessons/attention ；影片 https://www.youtube.com/watch?v=eMlx5fFNoYc（已核實 2026-11-12）
  - 適合程度：用「名詞去問前面有沒有形容詞」這個具體例子解釋 Q/K/V，不用抽象符號開場；masking 與 context 平方成長也在同一集講到。
  - 可借的圖解結構：一個 N×N 格子，列是 key、欄是 query，格子亮度＝點積大小；每欄做 softmax；右上三角塗黑（mask）；最後把 V 依權重加回原 embedding，畫成箭頭「推動」向量的方向。
  - 搭橋：點積＝相似度；softmax 當作權重；整件事是「可學習、依輸入動態改變的加權平均」，跟固定權重的全連接層形成對比。
- **The Illustrated Transformer** — Jay Alammar — https://jalammar.github.io/illustrated-transformer/（已核實 2026-11-12；頁面已附 2025 年更新，連到動畫版免費短課，並註明擴充內容收在《Hands-On Large Language Models》第 3 章）
  - 適合程度：Q/K/V 計算一步步拆成向量與矩陣兩種畫法，是最常被引用的 self-attention 圖解。注意它畫的是原始 encoder-decoder 翻譯模型，投影片要提醒現今 LLM 只用 decoder 那半。
  - 可借的圖解結構：兩個詞 Thinking / Machines 各自乘 W_Q、W_K、W_V 得到三個小向量 → q₁·k₁、q₁·k₂ → ÷√d_k → softmax → 乘 v 相加；接著改畫成矩陣版 X·W_Q = Q 一張圖收尾。
  - 搭橋：W_Q／W_K／W_V 就是三個 Linear 層；√d_k 縮放是為了 softmax 不飽和（接梯度消失）。

### 論點 4：Transformer 一層的組成；O(N²) 與 context window

- **Transformer Explainer（互動工具）** — Georgia Tech Polo Club — https://poloclub.github.io/transformer-explainer/（已核實 2026-11-12）
  - 適合程度：瀏覽器裡跑真的 GPT-2 small，可點開 embedding → QKV → masked multi-head attention → MLP → 輸出機率，還有 temperature、top-k、top-p 滑桿。一個工具串起論點 2～4，適合課堂 live demo。
  - 可借的圖解結構：左到右的區塊流程圖（Embedding → [Attention → MLP] × N → 機率），每個區塊可展開；這個「可展開的流程圖」排版很適合做成投影片的總覽頁。
  - 搭橋：殘差連接（ResNet）、LayerNorm（BatchNorm 的近親）、MLP 就是學生熟的全連接網路。
- **How GPT3 Works - Visualizations and Animations** — Jay Alammar — https://jalammar.github.io/how-gpt3-works-visualizations-animations/（已核實 2026-11-12）
  - 適合程度：用「2048 條平行軌道」表示 context window，比公式直觀。
  - 可借的圖解結構：一排固定長度的格子（context window），每格一個 token 往上穿過多層 decoder；新 token 從右邊進、最舊的從左邊被擠出。
  - 搭橋：固定輸入尺寸（如 CNN 的 224×224）；擠出去的就不在輸入裡（接論點 5）。
- **【生成式AI導論 2024】第10講：今日的語言模型是如何做文字接龍的 — 淺談Transformer** — 李宏毅（台大，中文）— https://www.youtube.com/watch?v=uhNsUCb2fJI ；課程頁 https://speech.ee.ntu.edu.tw/~hylee/genai/2024-spring.php（已核實 2026-11-12）
  - 適合程度：中文、針對非 NLP 背景，從「文字接龍」講到 Transformer 各模組與 attention 的計算量問題，講法與本課學生的起點最接近。
  - 可借的圖解結構：「Tokenization → Input Layer（embedding + 位置）→ Attention → Feed Forward → Output Layer」五段直排積木，每段旁註一句白話，可當 Transformer 單元的投影片骨架。（只核實了影片標題與課程頁，五段分法是依講題推定，借用前請先看片確認；同頁另有「第14講 欺騙大型語言模型」可供模組二使用。）
  - 搭橋：每個積木都對應一個 DL 已知元件（查表、加權平均、MLP、softmax 分類）。

### 論點 5：模型無狀態，「記住對話」靠每次重送

- **Chat templates** — Hugging Face Transformers 文件 — https://huggingface.co/docs/transformers/chat_templating（已核實 2026-11-12）
  - 適合程度：開宗明義寫「所有 causal LM 都只是在接續一串 token」，並把 messages 清單渲染成帶 `<|user|>`、`<|assistant|>` 控制 token 的純文字給你看。同一個 base model 的兩個微調版模板不同，很有說服力。
  - 可借的圖解結構：左邊是 JSON 形式的 messages（role/content 三則），中間一個箭頭標 `apply_chat_template`，右邊是一整條攤平的字串，控制 token 用醒目色標出；最後一行 `<|assistant|>` 後面留空白游標＝「輪到模型接龍」。
  - 搭橋：模型是純函數 f(輸入序列) → 下一個 token 分佈，權重在推論時不變，沒有任何地方存「上一輪」。
- **Conversation state** — OpenAI API 文件 — https://developers.openai.com/api/docs/guides/conversation-state（已核實 2026-11-12）
  - 適合程度：官方明講每個請求是無狀態的，要嘛自己帶歷史、要嘛用 `previous_response_id`／Conversations API 讓伺服器代存，而且「舊輪次的 token 仍照算 input 費用」。這句最能打破「模型會記得」的錯覺。
  - 可借的圖解結構：三輪對話畫成三個請求，每個請求的輸入方塊比上一個長一截（歷史累積），右側標 token 數與費用遞增；最後一個方塊撞到 context window 上限紅線。
  - 搭橋：推論時沒有梯度更新，所以對話不會改到權重；「記憶」全在輸入端。
- **Ollama API：/api/chat** — Ollama 文件 — https://docs.ollama.com/api/chat（已核實 2026-11-12）
  - 適合程度：參數表裡 `messages` 就是「chat history as an array」，加上 `num_ctx` 參數，正好讓 Lab 1 學生自己驗證「不帶歷史就忘記」。
  - 可借的圖解結構：課堂 demo 用——同一問題分別帶／不帶前一輪 messages 送出，對照回答。
  - 搭橋：同上。

### 論點 6：預訓練 → 指令微調 → 對齊；開源權重 vs API；Ollama 與 OpenAI 相容介面

- **[1hr Talk] Intro to Large Language Models** — Andrej Karpathy（YouTube）— https://www.youtube.com/watch?v=zjkBMFhNj_g（已核實 2026-11-12）
  - 適合程度：「一個 LLM 就是兩個檔案：參數檔 + 一段跑它的程式」這個開場最適合講開源權重；接著講「預訓練＝把網路壓縮進參數、微調＝把文件生成器變助手」。偏概念、零公式。
  - 可借的圖解結構：(a) 兩個檔案圖示（`parameters` 140GB + `run.c` 500 行）；(b) 兩階段表格：Stage 1 預訓練（大量網路文字、大量 GPU、數月）vs Stage 2 微調（少量高品質問答、數天）。
  - 搭橋：遷移學習——ImageNet 預訓練 backbone + 少量資料 fine-tune，就是同一套路。
- **RLHF: Reinforcement Learning from Human Feedback** — Chip Huyen — https://huyenchip.com/2023/05/02/rlhf.html（已核實 2026-11-12）
  - 適合程度：開頭一張「ChatGPT 三階段」總覽，每階段標資料量級（預訓練兆級 token、SFT 1萬～10萬對、RM 10萬～100萬比較），數字讓學生對成本有感。
  - 可借的圖解結構：三段橫向管線，方塊寬度依資料量遞減（預訓練最寬），每段下方寫資料型態（原始文字 → 問答對 → 偏好比較）；可加 Shoggoth 戴笑臉面具的比喻當插畫提示（自繪）。
  - 搭橋：預訓練＝自監督（label 免費來自下一個字）；SFT＝監督式微調；RM＝訓練一個打分的回歸模型。
- **OpenAI compatibility** — Ollama 文件 — https://docs.ollama.com/api/openai-compatibility（已核實 2026-11-12）
  - 適合程度：一頁講完本地 `http://localhost:11434/v1/` 與支援的端點，加上「api_key 必填但會被忽略」這個新手必踩點。
  - 可借的圖解結構：一個 Python client 在中央，`base_url` 像切換開關，分別指向 Ollama（本機）／DeepSeek／OpenAI 三朵雲，三條線上都寫同一個 `chat.completions.create(...)`。
  - 搭橋：同一介面、換後端，類似 PyTorch 換 device（cpu/cuda）而程式碼不變。
## 事實核實

- **Ollama OpenAI 相容端點 `http://localhost:11434/v1`**：✅ 正確。本機 base URL 為 `http://localhost:11434/v1/`，支援 `/v1/chat/completions`（含串流、JSON mode、tools、vision）、`/v1/embeddings`、`/v1/completions`、`/v1/models`，以及無狀態的 `/v1/responses`；`tool_choice` 不支援；api_key 需填任意值（例 `ollama`）但會被忽略。出處：https://docs.ollama.com/api/openai-compatibility
- **Ollama 預設 context 長度**（課綱未提，但與「上下文窗口極限」直接相關）：預設 `num_ctx` = **4096**，即使模型本身支援 128K。超過會被截斷，學生容易誤以為模型「忘記」。可用 `OLLAMA_CONTEXT_LENGTH` 或請求的 `num_ctx` 調整。出處：https://docs.ollama.com/faq
- **Ollama 模型生命週期**：預設閒置 5 分鐘卸載，`keep_alive` 可調（0＝立即卸載、負值＝常駐）；`ollama stop <model>` 手動卸載。出處：https://docs.ollama.com/faq
- **DeepSeek-R1-Distill 1.5B／8B**：⚠️ 與課綱寫法不完全一致。
  - HF 原始 distill 系列：1.5B＝DeepSeek-R1-Distill-**Qwen**-1.5B（基於 Qwen2.5-Math-1.5B），8B＝DeepSeek-R1-Distill-**Llama**-8B（基於 Llama-3.1-8B）。出處：https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-8B
  - 但 Ollama 的 `deepseek-r1:8b`（也是 `latest`）**已改指向 DeepSeek-R1-0528-Qwen3-8B**（基於 Qwen3-8B），不再是 Llama distill；要原版需拉 `deepseek-r1:8b-llama-distill-q4_K_M`。大小：1.5b 1.1GB、8b 5.2GB。標示「1 year ago」更新。出處：https://ollama.com/library/deepseek-r1 、https://ollama.com/library/deepseek-r1/tags
  - 官方使用建議：**temperature 0.5–0.7（建議 0.6）、不要用 system prompt、所有指令放 user prompt**。與課綱「代碼生成 Temperature 必須置 0」及模組二的角色設定寫法衝突（見投影片建議）。
- **Qwen2.5-3B／7B**：✅ 存在，但已過時。Ollama `qwen2.5:3b` 1.9GB、`qwen2.5:7b` 4.7GB，context 32K，標示「2 years ago」。出處：https://ollama.com/library/qwen2.5
- **Qwen3-14B**：✅ 存在。Ollama `qwen3:14b` 9.3GB、context 40K；HF 原生 32,768（YaRN 可到 131,072）、14.8B 參數、Apache-2.0，支援 `enable_thinking` 與 `/think`、`/no_think` 切換。出處：https://ollama.com/library/qwen3 、https://huggingface.co/Qwen/Qwen3-14B
- **較新的 Qwen**（課綱未列，供替換參考）：Ollama 上已有 `qwen3.5`（0.8b／2b／4b／9b／27b／35b／122b，context 256K，支援 vision、tools、thinking；`9b` 約 6.6–7.6GB，16GB 顯存可跑），另有 `qwen3.6`、`qwen3.8`。出處：https://ollama.com/library/qwen3.5 、https://ollama.com/library
- **nomic-embed-text**：✅ 存在。`latest`＝v1.5、274MB、僅能產生 embedding、需 Ollama ≥ 0.1.26；Ollama 頁面列 context 2K；標示「2 years ago」更新。較新替代：`qwen3-embedding`、`embeddinggemma`、`embeddinggemma-2`。出處：https://ollama.com/library/nomic-embed-text 、https://ollama.com/library
- **GPT-4o（課綱列為閉源商業代表）**：⚠️ 已被標為棄用。`gpt-4o-2024-05-13` 已於 **2026-10-23** 關閉；`gpt-4o-2024-08-06`、`gpt-4o-2024-11-20`、`gpt-4o-mini-2024-07-18` 將於 **2027-01-14** 關閉；`chatgpt-4o-latest` 已於 2026-02-17 關閉。開課時可能已不能呼叫。出處：https://developers.openai.com/api/docs/deprecations
- **Claude 系列**：✅ 仍為現役商業 API；目前文件列出的模型含 Claude Opus 5.5、Sonnet 5.5、Haiku 5.5 等。出處：https://platform.claude.com/docs/en/build-with-claude/structured-outputs
- **DeepSeek 雲端 API（Lab 1 故障切換對象）**：OpenAI 相容 base URL `https://api.deepseek.com`（另有 Anthropic 相容 `/anthropic`）。目前定價頁列出的模型名為 `deepseek-flash`（DeepSeek-V4.1-Flash-1017）與 `deepseek-v4-pro`（DeepSeek-V4-Pro-0813），context 1M，支援 JSON output 與 tool calls；頁面**未列出** `deepseek-chat`／`deepseek-reasoner`，是否仍可用未核實。Lab 程式中的模型名須依此更新。出處：https://api-docs.deepseek.com/ 、https://api-docs.deepseek.com/quick_start/pricing
- **OpenAI Assistants API**（若有學生找到舊教學）：已於 2026-08-26 關閉，改用 Responses／Conversations API；Chat Completions 未列入棄用。出處：https://developers.openai.com/api/docs/deprecations
- **Hugging Face LLM Course 中文版**：簡中完整、繁中翻譯進行中。出處：https://huggingface.co/learn/llm-course/chapter1/1

## 投影片建議

1. **「Temperature 0 → 不會幻覺」要改講法**。temperature 只控制 softmax 分佈的尖銳度（輸出的隨機性），不控制事實正確性；T=0 時模型照樣會很有把握地答錯。建議改成「需要可重現、格式穩定的輸出時調低 temperature；正確性靠 grounding 與驗證」。另外，課綱推薦的 DeepSeek-R1-Distill 官方建議 temperature 0.6，設 0 反而容易無限重複，踩坑表那一列要加這個例外。
2. **在 Transformer 之前插一張「RNN 瓶頸」頁，再進 Q/K/V**。課綱直接從「self-attention 打破 RNN 序列限制」開講，但學生沒看過 seq2seq。建議順序：分類器 → 語言模型 = 詞表 softmax → RNN 語言模型與單一 context vector 瓶頸（Alammar seq2seq 圖）→ attention 是加權平均 → self-attention。每步都只多一個新概念。
3. **把「為什麼記不住對話」從面試題提前成正式教學內容，並和 Ollama `num_ctx` 綁在一起演示**。chat template 攤平圖 + 「每輪請求越來越長」圖，再現場把 `num_ctx` 調小讓模型「失憶」。這一頁同時講清楚無狀態、context window、O(N²) 成本三件事，也為模組三的 RAG 鋪路。
4. **更新模型清單**。GPT-4o 在 2027-01-14 前全部關閉，Qwen2.5 已兩年未更新，`deepseek-r1:8b` 在 Ollama 上已不是 Llama distill。建議：閉源代表改用現役型號；本地輕量模型以 `qwen3.5:4b`／`qwen3.5:9b`（或 `qwen3:8b`／`qwen3:14b`）取代 Qwen2.5；R1 distill 明確寫出 Ollama tag。DeepSeek 雲端模型名改為 `deepseek-flash`／`deepseek-v4-pro`。
5. **「預訓練 → 指令微調 → 對話模型」直接用遷移學習框架講**。學生已懂 ImageNet 預訓練 + fine-tune，畫成兩列對照表（CV vs LLM：資料、目標、標籤從哪來）即可，不需引入 RLHF 細節；RL 只點名「再用人類偏好調一次」，細節留給模組六。
