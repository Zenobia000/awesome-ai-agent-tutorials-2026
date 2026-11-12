# 模組六 素材地圖

> 對象：懂深度學習（反向傳播、遷移學習、embedding），沒碰過 NLP／生成式 AI。
> 所有 URL 均於 2026-11-12 以 WebFetch 實際開啟核實；打不開或需登入者已剔除（見文末「剔除清單」）。

## 論點清單

1. **先判斷「缺知識」還是「缺行為」**：Prompt → RAG → 微調是由便宜到昂貴的階梯；RAG 補知識，微調改行為（格式、語氣、術語），兩者可疊加。
2. **LoRA = 凍結原權重 W，只學一個低秩的更新量 ΔW = B·A**；rank r 決定容量，alpha/r 決定更新量放大倍率。
3. **QLoRA = 把凍結的 W 壓成 4-bit 存，再在上面接 LoRA**，讓消費級 GPU（24GB）也能微調 7B–14B 模型。
4. **微調資料就是「對話格式的監督標籤」**：Alpaca／ShareGPT 只是存檔格式，真正餵進模型的是套用 chat template 後的 token 序列；格式錯 = 標籤錯。
5. **訓練監控沿用 DL 老功夫**：看 train/eval loss、早停防過擬合；LLM 特有的風險是災難性遺忘，而 LoRA「學得少、也忘得少」。
6. **訓練完要「合併→匯出→本地推理」**：ΔW 可以加回 W 變成單一模型、零額外延遲；多模態模型（Qwen3-VL）走同一條本地部署路線。

## 素材

### 論點 1：先判斷「缺知識」還是「缺行為」

- **Optimizing LLM Accuracy** — OpenAI 官方指南 — https://developers.openai.com/api/docs/guides/optimizing-llm-accuracy （已核實 2026-11-12；舊網址 platform.openai.com/docs/guides/optimizing-llm-accuracy 會 301 轉到此）
  - 適合程度：不需任何 NLP 背景，用「in-context memory（考試帶小抄）vs learned memory（真的背起來）」切分 RAG 與微調，概念清楚、無數學。
  - 可借的圖解結構：二維矩陣。X 軸「LLM optimization（行為一致性：格式、語氣、推理方式）」、Y 軸「Context optimization（知識：缺失、過時、私有）」；左下角是起點 Prompt engineering，往上走是 RAG、往右走是 Fine-tuning、右上角是兩者合用。可直接重畫成課綱「選型決策矩陣」的視覺版。另有一個反例可上投影片：對「行為問題」硬加 RAG，BLEU 反而掉 4 分。
  - 搭橋：「欠擬合 vs 缺資料」的診斷思維——先找出錯誤來源，再決定是改輸入（特徵/上下文）還是改模型（權重）。
- **Finetuning Large Language Models** — Sebastian Raschka（Ahead of AI）— https://magazine.sebastianraschka.com/p/finetuning-large-language-models （已核實 2026-11-12）
  - 適合程度：從 CV 遷移學習的學生最熟的三種做法出發，幾乎是為這群學生寫的橋樑文章。
  - 可借的圖解結構：三欄並排——(a) Feature-based：整個預訓練模型凍結、只拿 embedding 訓練一個外接分類器；(b) Finetuning I：凍結 backbone、只訓新加的輸出層；(c) Finetuning II：全部層都更新。下方再加一張「效能 vs 訓練成本」取捨曲線；最左側可再補一欄 In-context learning（完全不訓練，只改輸入）。
  - 搭橋：直接對應 ImageNet 預訓練 → 凍結 conv 層、換 FC 頭的遷移學習；再補一句「LoRA 是第四種：全部層都動，但每層只動一點點」。
- **RAG vs. fine-tuning vs. prompt engineering** — IBM Think（Ivan Belcic、Cole Stryker）— https://www.ibm.com/think/topics/rag-vs-fine-tuning-vs-prompt-engineering （已核實 2026-11-12）
  - 適合程度：沒有圖，但用「家庭廚師」比喻貫穿三種方法（改食譜說明 / 給參考書 / 送去上烹飪課），適合當口語講稿素材。
  - 可借的圖解結構：本身無圖；可把它的比喻畫成三格漫畫，各格標註「成本」「改了什麼」（輸入／上下文／權重）。
  - 搭橋：三者分別對應「改輸入」「改輸入的內容來源」「改參數」，學生用 forward/backward 的位置就能定位。

### 論點 2：LoRA = 凍結 W，只學低秩 ΔW = B·A

- **Improving LoRA: Implementing DoRA from Scratch**（前半段為 LoRA 從零實作）— Sebastian Raschka — https://magazine.sebastianraschka.com/p/lora-and-dora-from-scratch （已核實 2026-11-12）
  - 適合程度：用 PyTorch `nn.Module` 寫出 LoRALayer，學生看程式碼比看公式快；附 1000×1000 矩陣算參數量的具體例子。
  - 可借的圖解結構：左右對照圖——左「一般微調：x → W + ΔW → h」，右「LoRA：x 同時走兩條路，主路是凍結的 W，旁路是 A（d×r，瘦長）→ B（r×d，扁寬），兩路輸出相加」。在旁路下方標數字：d=1000、r=2 時 ΔW 要 1,000,000 參數，A+B 只要 4,000（少 250 倍）。
  - 搭橋：(1) 矩陣低秩分解／SVD 截斷——任何 d×d 矩陣都可近似為 d×r 乘 r×d；(2) 反向傳播只對 A、B 算梯度，W 的 `requires_grad=False`，跟凍結 backbone 是同一個開關；(3) B 初始化為 0，所以訓練起點 ΔW=0、模型行為與原模型完全相同（像 ResNet 殘差分支初始化為恆等）。
- **LoRA（Conceptual guide）** — Hugging Face PEFT 官方文件 — https://huggingface.co/docs/peft/main/en/conceptual_guides/lora （已核實 2026-11-12）
  - 適合程度：官方概念頁，短、附示意圖；明講 A 用 Kaiming-uniform、B 初始化為 0、縮放係數 = lora_alpha / r，以及可以只挑部分層（target_modules）。
  - 可借的圖解結構：凍結權重方塊（灰）+ 旁邊兩個小矩陣 A、B（彩色），訓練時分開、推理時可合併回 W。適合做成兩張動畫：訓練態（分離）→ 部署態（合併）。
  - 搭橋：Kaiming 初始化學生學過；alpha/r 可類比「旁路分支的固定學習率倍率」，r 調大時自動縮小每個方向的貢獻，避免換 r 就要重調學習率。
- **Practical Tips for Finetuning LLMs Using LoRA** — Sebastian Raschka — https://magazine.sebastianraschka.com/p/practical-tips-for-finetuning-llms （已核實 2026-11-12）
  - 適合程度：數百次實驗的「調參心得」，是給已經懂原理的人的經驗表，適合放在 LoRA 原理之後、Lab 之前。
  - 可借的圖解結構：「r / alpha 組合 vs 評測分數」的表格可改畫成熱力圖；另有「只對 q,v 投影加 LoRA（4.19M 參數）vs 全層加 LoRA（20.28M 參數）」的對比，可畫成 Transformer block 上標色的「LoRA 插在哪裡」示意圖。
  - 搭橋：超參數搜尋（grid search）；alpha=2r 的經驗法則類比「學習率的經驗起點」，不是定律（文中 r=256、alpha=128 反而更好）。

### 論點 3：QLoRA = 凍結的 W 存成 4-bit，再接 LoRA

- **Making LLMs even more accessible with bitsandbytes, 4-bit quantization and QLoRA** — Hugging Face Blog（Younes Belkada、Tim Dettmers 等）— https://huggingface.co/blog/4bit-transformers-bitsandbytes （已核實 2026-11-12）
  - 適合程度：QLoRA 原作者 Tim Dettmers 參與撰寫的官方入門文，附可執行程式碼；NF4、double quantization、paged optimizer 三個名詞在這裡一次介紹。
  - 可借的圖解結構：(1) FP8 位元配置圖（sign / exponent / mantissa 三段色塊）；(2) LoRA adapter 動畫：凍結權重（4-bit 存放）+ A、B（16-bit 訓練）。可重畫成「同一張 W 方塊，從 FP16 灰底縮成 4-bit 細格，旁邊的 A、B 仍是高精度」。
  - 搭橋：混合精度訓練（AMP/FP16）學生可能用過；QLoRA 是「凍結的部分可以壓得更狠，因為它不需要梯度」。
- **A Visual Guide to Quantization** — Maarten Grootendorst — https://newsletter.maartengrootendorst.com/p/a-visual-guide-to-quantization （已核實 2026-11-12）
  - 適合程度：50+ 張自繪圖解，從「浮點數怎麼存」講起，零 NLP 前置知識；是「量化是什麼」最好的視覺教材。注意：它不講 NF4/QLoRA，只負責打底。
  - 可借的圖解結構：數線映射圖——上方 FP32 的值域 [-max, max]，下方 INT8 的 [-127, 127]，用斜線把值對應過去；對稱 vs 非對稱（zero-point 偏移）並排；離群值被 clipping 的示意；以及「把照片降到 8 色」的直覺圖。
  - 搭橋：數值精度、bit 數 × 參數量 = 記憶體（7B × 2 bytes ≈ 14GB vs 7B × 0.5 byte ≈ 3.5GB），這個算式學生秒懂。
- **LLaMA-Factory README 硬體需求表** — hiyouga/LLaMA-Factory — https://github.com/hiyouga/LLaMA-Factory （已核實 2026-11-12）
  - 適合程度：一張表就回答「我的卡能不能跑」。
  - 可借的圖解結構：橫條圖：7B 模型 LoRA(16-bit) 16GB → QLoRA 8-bit 10GB → QLoRA 4-bit 6GB → 2-bit 4GB，旁邊畫一條 RTX 4090 = 24GB 的紅色虛線。
  - 搭橋：batch size 與顯存的取捨（學生 OOM 過就懂）。

### 論點 4：微調資料就是對話格式的監督標籤

- **LLaMA-Factory data/README** — hiyouga/LLaMA-Factory — https://github.com/hiyouga/LLaMA-Factory/blob/main/data/README.md （已核實 2026-11-12）
  - 適合程度：Lab 直接要用的格式規範，附 JSON 範例與 `dataset_info.json` 註冊方式；也涵蓋多模態 `images` 欄位（Qwen3-VL 微調會用到）。
  - 可借的圖解結構：左右並排兩個 JSON 卡片——Alpaca（instruction / input / output / system / history，單輪為主）vs ShareGPT（conversations 陣列，from/value，human 與 gpt 交替，可含 function_call / observation）；中間一個箭頭指向 `dataset_info.json` 的 `formatting` 欄位。
  - 搭橋：等同 CV 的 `ImageFolder` / COCO annotation 格式——不同存檔格式，最後都轉成 (x, y) 張量。
- **Chat templates** — Hugging Face Transformers 官方文件 — https://huggingface.co/docs/transformers/main/en/chat_templating （已核實 2026-11-12）
  - 適合程度：開宗明義「所有聊天模型本質上只是在接續 token 序列」，對沒學過 NLP 的人是最關鍵的一句；並用同一段對話在 Mistral（`[INST]`）與 Zephyr（`<|user|>`）兩種模板下的不同輸出作對照。
  - 可借的圖解結構：三段式轉換圖——(1) messages list `[{role, content}, ...]` → (2) 套模板後的字串（Qwen 系列為 `<|im_start|>user ... <|im_end|>`）→ (3) token id 序列。再加一張 `add_generation_prompt=True/False` 的差異圖：結尾多一行 `<|im_start|>assistant`。
  - 搭橋：特殊 token 類似 CV 中的「類別 one-hot 編碼規範」——訓練和推理必須用同一套，否則模型看到的是分布外輸入。
- **LLM Research Insights: Instruction Masking and New LoRA Finetuning Experiments** — Sebastian Raschka — https://magazine.sebastianraschka.com/p/llm-research-insights-instruction （已核實 2026-11-12）
  - 適合程度：解釋「loss 要算在哪些 token 上」，學生會自然問到。
  - 可借的圖解結構：同一條樣本的 token 列，問題部分灰色（不算 loss）、回答部分彩色（算 loss）；三種遮罩策略並排：不遮、遮指令、只遮固定樣板。
  - 搭橋：loss mask／sample weighting——就像語意分割裡忽略 ignore_index=255 的像素。

### 論點 5：訓練監控、過擬合與災難性遺忘

- **LoRA Fine-Tuning Hyperparameters Guide** — Unsloth 官方文件 — https://unsloth.ai/docs/get-started/fine-tuning-llms-guide/lora-hyperparameters-guide （已核實 2026-11-12；舊網址 docs.unsloth.ai 301 轉到此）
  - 適合程度：一張超參數總表 + 過擬合/欠擬合的「症狀→處方」清單，極實用；給出可量化的訊號（train loss < 0.2 多半已過擬合）。
  - 可借的圖解結構：(1) 雙欄處方表：左「過擬合」（降 LR、減 epoch、加 weight decay、早停、擴充資料、降 alpha）右「欠擬合」（升 LR、加 epoch、加大 r/alpha）；(2) 有效 batch = batch_size × grad_accum 的乘法方塊圖；(3) target modules 比較長條圖（All > FFN > Attention）。
  - 搭橋：完全是學生熟悉的 bias-variance 與早停；建議起點 LR 2e-4、1–3 epoch。
- **LoRA Without Regret** — John Schulman 等，Thinking Machines Lab — https://thinkingmachines.ai/blog/lora/ （已核實 2026-11-12）
  - 適合程度：2025 年最有份量的 LoRA 實證整理，圖表為主；回答「LoRA 到底能不能等於全量微調」。對入門者稍深，建議講師取其結論與圖，不要求學生讀全文。
  - 可借的圖解結構：(1) loss vs step（log 軸）多條曲線：Full FT 與高 rank LoRA 重疊，低 rank 在某一步「掉隊」（容量用完）；(2) 學習率 vs 最終 loss 的 U 形曲線，LoRA 的谷底在 Full FT 的約 10 倍處；(3) Attention-only vs MLP-only LoRA 對比。
  - 搭橋：模型容量 vs 資料量（小模型擬合大資料集會欠擬合）；「r 就是旁路的容量旋鈕」。
- **LLM Research Insights（同上，後半段 "LoRA Learns Less and Forgets Less"）** — Sebastian Raschka — https://magazine.sebastianraschka.com/p/llm-research-insights-instruction （已核實 2026-11-12）
  - 適合程度：把 Biderman et al. 2024 的結論濃縮成「學習 vs 遺忘」取捨，正好接災難性遺忘。
  - 可借的圖解結構：2×2 圖——X 軸「新領域表現（學得多少）」、Y 軸「原能力保留（忘得多少）」，Full FT 落在右下（學多忘多）、LoRA 落在左上（學少忘少），並分 code / math 兩組點。
  - 搭橋：遷移學習中「微調整個 backbone 會洗掉 ImageNet 特徵」的經驗；LoRA 本身就是一種正則化（限制更新的秩）。

### 論點 6：合併、匯出與本地多模態推理

- **模型保存、LoRA 合并与量化** — LLaMA-Factory 官方文件（簡中）— https://llamafactory.readthedocs.io/zh-cn/latest/getting_started/merge_lora.html （已核實 2026-11-12）
  - 適合程度：Lab 操作手冊；一個 yaml + `llamafactory-cli export` 就完成，並明確警告「不要合併到量化後的基座」。
  - 可借的圖解結構：流程圖——base model（FP16）+ adapter 資料夾 → export → merged model → （選配）GPTQ 量化 → 部署。用紅色叉號標出「4-bit 基座 + adapter → merge」這條錯誤路徑。
  - 搭橋：模型 checkpoint 儲存/載入（`state_dict`）；adapter 就是一個只含 A、B 的小 `state_dict`（幾十 MB）。
- **LoRA conceptual guide 的 Merge 段落** — Hugging Face PEFT — https://huggingface.co/docs/peft/main/en/conceptual_guides/lora （已核實 2026-11-12）
  - 適合程度：說明 `merge_and_unload()` 為何零推理延遲，以及 `merge_adapter / unmerge_adapter` 可以熱切換多個 adapter。
  - 可借的圖解結構：W' = W + (alpha/r)·B·A 的矩陣加法圖；再畫一個「一個基座 + 多個 adapter 插槽（客服版、醫療版、法律版）」的插拔示意。
  - 搭橋：矩陣乘法的結合律——(W + BA)x = Wx + B(Ax)，所以訓練時分開算、部署時先加好，結果完全相同。
- **Qwen3-VL GitHub README** — QwenLM 官方 — https://github.com/QwenLM/Qwen3-VL （已核實 2026-11-12）
  - 適合程度：官方尺寸表與部署選項（Transformers / vLLM / SGLang / Docker / Web demo），能力清單（OCR 32 語言、文件版面解析、2D/3D grounding、GUI agent）可直接做成「能做什麼」投影片。
  - 可借的圖解結構：尺寸階梯圖（2B → 4B → 8B → 32B dense；30B-A3B、235B-A22B MoE），每階標「建議顯卡」；能力卡片牆（每張卡一個 demo 截圖位置）。
  - 搭橋：視覺 encoder（學生熟的 ViT/CNN）把影像變成一串 embedding，接在文字 token 前面一起送進語言模型——「影像也被當成 token」。
- **qwen3-vl（Ollama Library）** — Ollama 官方 — https://ollama.com/library/qwen3-vl （已核實 2026-11-12）
  - 適合程度：一行 `ollama run qwen3-vl:8b` 即可本地跑，最低門檻的 demo 路線。
  - 可借的圖解結構：tag × 磁碟大小表（2b 1.9GB、4b 3.3GB、8b 6.2GB、30b 20GB、32b 21GB、235b 143GB），畫成和顯存對照的條狀圖。
  - 搭橋：模型檔大小 ≈ 參數量 × 每參數 bytes（呼應論點 3 的量化算式）。

## 事實核實

- **LoRA「不到 1% 參數達到全量微調效果」**：前半句準確、後半句過度概括。參數量：Raschka 實驗中 Llama 2 7B、r=8、只加 q/v 時可訓練 4.19M / 6.74B ≈ 0.06%，全層也才 20.28M ≈ 0.3%（https://magazine.sebastianraschka.com/p/practical-tips-for-finetuning-llms ）；原論文對 GPT-3 175B 是「可訓練參數少 10,000 倍、顯存少 3 倍」，並在 RoBERTa／DeBERTa／GPT-2／GPT-3 上「on-par or better」（https://arxiv.org/abs/2106.09685 ）。但「達到全量效果」有條件：Biderman et al. 2024 發現在 code、尤其是 continued pretraining 上 LoRA 明顯落後，且學得少也忘得少（https://magazine.sebastianraschka.com/p/llm-research-insights-instruction ）；Thinking Machines 2025 結論是「中小型指令/推理資料集、且 LoRA 加在所有層（含 MLP）時」才與全量微調相當，資料量超過容量時會落後（https://thinkingmachines.ai/blog/lora/ ）。**→ 與課綱不一致，建議改寫為「通常 <1% 參數，在中小型指令資料上可接近全量微調」。**
- **r=8 / alpha=16 是否常見預設**：是常見起點，但不是所有工具的預設。LLaMA-Factory：`lora_rank` 預設 8、`lora_alpha` 預設 None，文件註明「一般情況下為 lora_rank × 2」，即 16（https://llamafactory.readthedocs.io/zh-cn/latest/advanced/arguments.html ）；官方 Qwen3 範例 yaml 用 r=8、lr 1e-4、3 epoch（https://llamafactory.readthedocs.io/zh-cn/latest/getting_started/sft.html ）。HF PEFT `LoraConfig` 預設 r=8、**lora_alpha=8**（https://huggingface.co/docs/peft/main/en/package_reference/lora ）。Unsloth 建議 r=16 或 32、alpha=r 或 2r（https://unsloth.ai/docs/get-started/fine-tuning-llms-guide/lora-hyperparameters-guide ）。Raschka 稱 alpha=2r 為經驗法則（https://magazine.sebastianraschka.com/p/practical-tips-for-finetuning-llms ）。→ 與課綱一致（在 LLaMA-Factory 情境下）。
- **LLaMA-Factory 是否支援 Qwen3**：支援。README 列 Qwen3（0.6B–235B，template `qwen3` / `qwen3_nothink`）與 Qwen3-VL（2B–235B，template `qwen3_vl`）（https://github.com/hiyouga/LLaMA-Factory ）。v0.9.5（2026-05-30）再加入 Qwen3.5／Qwen3.6／Gemma4，並相容 Transformers v5（https://github.com/hiyouga/LlamaFactory/releases/tag/v0.9.5 ）。注意 repo 已顯示為 `hiyouga/LlamaFactory`，舊名網址仍可開。
- **Qwen3-VL 可用尺寸**：Dense 2B／4B／8B／32B，MoE 30B-A3B／235B-A22B，各有 Instruct 與 Thinking 版，30B-A3B 另有 FP8；2025-09-23 至 2025-10-21 陸續發布；需 transformers ≥ 4.57.0、vLLM ≥ 0.11.0（https://github.com/QwenLM/Qwen3-VL ）。Ollama 提供 2b／4b／8b／30b／32b／235b，需 Ollama ≥ 0.12.7（https://ollama.com/library/qwen3-vl ）。**補充：Qwen3.5（2026-02）已是原生多模態（內建 vision encoder、early fusion），Apache-2.0**（https://huggingface.co/Qwen/Qwen3.5-9B ）——課綱寫 Qwen3-VL 不算錯，但到 2026 下半年已非最新選擇。
- **QLoRA 記憶體**：LLaMA-Factory 估算 7B：LoRA 16-bit 16GB、QLoRA 8-bit 10GB、4-bit 6GB（https://github.com/hiyouga/LLaMA-Factory ）；Raschka 實測 QLoRA 省約 33% 顯存、訓練時間多約 39%（https://magazine.sebastianraschka.com/p/practical-tips-for-finetuning-llms ）。→ Lab 用 RTX 4090（24GB）跑 7B/8B LoRA 可行。
- **Alpaca / ShareGPT 格式**：與課綱一致；LLaMA-Factory 欄位規範見 https://github.com/hiyouga/LLaMA-Factory/blob/main/data/README.md 。
- **「Chat Template 不符導致訓練無法收斂」**：查無出處支持「無法收斂」。官方文件描述的後果是「控制 token 錯誤會讓模型表現大幅變差」（https://huggingface.co/docs/transformers/main/en/chat_templating ）；LLaMA-Factory 要求 `template` 與模型一致（https://llamafactory.readthedocs.io/zh-cn/latest/getting_started/sft.html ）。實務症狀通常是 loss 照樣下降，但推理時不會停、重複輸出或角色錯亂。**→ 與課綱描述不一致，建議改寫症狀。**
- **災難性遺忘「混入 15% 通用指令資料」**：本次未找到權威出處支持 15% 這個具體數字；混入通用資料（replay）是常見做法，但比例屬經驗值。**→ 建議投影片標明「經驗值，依任務調整」。**
- **過擬合訊號**：Unsloth 給出「train loss < 0.2 多半過擬合」與 1–3 epoch 建議（https://unsloth.ai/docs/get-started/fine-tuning-llms-guide/lora-hyperparameters-guide ）；Raschka 實驗中 Alpaca 50k 跑約 2 epoch 反而變差（https://magazine.sebastianraschka.com/p/practical-tips-for-finetuning-llms ）。
- **權重合併**：LLaMA-Factory 用 `llamafactory-cli export <yaml>`，且不可合併到量化基座（https://llamafactory.readthedocs.io/zh-cn/latest/getting_started/merge_lora.html ）。→ QLoRA 訓練完要拿 FP16/BF16 原基座來 merge，課綱未提，Lab 易踩坑。

## 投影片建議

1. **把「LoRA 不到 1% 參數達到全量效果」改成有條件的說法**，並用 Thinking Machines 的 loss 曲線圖示範「r 太小 = 容量不夠會掉隊」。這群學生懂容量和 bias-variance，給條件反而更好懂，也避免面試時被追問答不出來。
2. **在講 LoRA 前先補一張「LLM 微調 = 遷移學習」的對照投影片**（Raschka 三欄圖 + 第四欄 LoRA），再進 ΔW=BA。學生從 CV 遷移學習過來，這是最短的路；課綱「摒棄數學公式」可以保留，但 ΔW = B·A 和參數量算式（d×d vs 2×d×r）不要省，對這群人那是直覺而不是負擔。
3. **chat template 要獨立一頁，並從「LLM 只是在接 token」講起**。沒學過 NLP 的人不知道對話怎麼變成訓練資料；用 messages → 模板字串 → token id → loss mask 四格圖串起 Alpaca/ShareGPT、template、loss 計算三件事。同時把踩坑表的「無法收斂」改成實際症狀（推理不停、重複、角色錯亂）。
4. **QLoRA 加一個合併陷阱提醒**：QLoRA 訓練用 4-bit 基座，但 merge 必須用原精度基座（LLaMA-Factory 文件明確警告）。課綱的 Lab 步驟 4 只寫「加載權重對話驗證」，建議補「export 合併」一步。
5. **多模態段落補一句 Qwen3.5**：Qwen3-VL 仍可用（尺寸齊、Ollama 一行跑），但 2026-02 起 Qwen3.5 小模型已原生支援影像，且 LLaMA-Factory v0.9.5 已支援。建議 Lab 維持 Qwen3／Qwen3-VL（教材穩定），在投影片標註「新一代：Qwen3.5 原生多模態」，避免學生以為仍需獨立 VL 模型。

## 剔除清單

- Lightning AI「Parameter-Efficient LLM Finetuning With LoRA」（https://lightning.ai/pages/community/tutorial/lora-llm/ ）：302 轉至 platform.lightning.ai 後頁面只顯示載入中，無法取得內容，剔除。
- IBM 那篇保留，但它本身沒有圖，只當講稿比喻素材用。
- 影片類素材本次未核實（YouTube 頁面無法用 WebFetch 驗證內容），未列入。
