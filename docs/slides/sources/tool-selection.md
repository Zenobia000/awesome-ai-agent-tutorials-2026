# 技術選型素材（核實日 2026-11-17）

投影片 X40–X49「選型」頁的資料來源。四份查證各自獨立，每列都附實際開過的連結；版本與狀態變化快，引用前以連結頁為準。


---

## 技術選型素材 A：模型家族＋微調／本地推理工具（核實日 2026-11-17）

做法：每列都實際開過來源。GitHub 狀態（archived、license、最新 release、是否改名）用 `gh api repos/...` 查，時間 2026-11-17。授權欄寫的是 repo 或 HF 上 LICENSE 檔的實際內容，不是 HF 標籤的簡稱。不放 star 數和 benchmark。
與 `product-facts.md` 沒有衝突；本檔把 Claude 系列補成完整清單，並更新 Qwen 的最新世代。

---

### 表 1：LLM 模型家族（M1）

### 1a. 商業 API

| 家族 | 廠商 | 現行旗艦／常用（2026-11） | 定位（≤20 字） | 什麼時候選它 | 官方連結（已開過） |
|---|---|---|---|---|---|
| GPT | OpenAI | 文件「Flagship models」列 GPT-6 Astra（`gpt-6-astra`，官方寫「不確定就從它開始」）、GPT-6.1 Sol、GPT-6.1 Terra、GPT-6 Luna | 生態最大的通用 API | 要最多第三方整合、Responses API 生態 | https://developers.openai.com/api/docs/models |
| Claude | Anthropic | 官方建議預設 Claude Opus 5.5；Fable 5.2 給高難度推理和長時程 agent；Sonnet 5.5 兼顧速度與智力；Haiku 5.5 給大量、低延遲任務；全系列 1M context | 長時程 agent 與寫程式 | agent 和 coding 工作流、長文件 | https://platform.claude.com/docs/en/about-claude/models/overview |
| Gemini | Google | 旗艦 Gemini 4 Carbon（`gemini-4-carbon`）；Gemini 4 另有 Argon、Hydrogen；穩定版的 Flash 系列是 `gemini-3.8-flash` 等；2.5 Flash／Pro 已棄用 | 多模態、Google 生態 | 影音多模態、已在 GCP／Workspace 上 | https://aistudio.google.com/docs/models （舊網址 ai.google.dev/gemini-api/docs/models 會 301 轉到這裡） |
| Grok | xAI | 旗艦 `grok-4.7`（官方原文：“the most capable model we've built”） | xAI 自家通用模型 | 已在 X／xAI 生態上 | https://docs.x.ai/docs/models |
| DeepSeek API | DeepSeek | `deepseek-flash`（指向 V4.1-Flash-1017，含 vision）、`deepseek-v4-pro`（指向 V4-Pro-0813） | 便宜、相容 OpenAI 格式 | 成本敏感，也想要權重可下載的退路 | https://api-docs.deepseek.com/quick_start/pricing |

### 1b. 開源權重（open weights）

| 家族 | 廠商 | 最新世代（2026-11） | 授權（看 LICENSE 實文） | 定位（≤20 字） | 什麼時候選它 | 官方連結（已開過） |
|---|---|---|---|---|---|---|
| Qwen | 阿里巴巴 Qwen 團隊 | Qwen3.8（27B、2.4T-A95B）、Qwen3.8-Flash-Next、Qwen3.6（27B、35B-A3B）；Ollama 上的 Qwen3.5 依 product-facts 照樣可用 | **分尺寸不同**：Qwen3.8-27B、Qwen3.6 為 Apache-2.0；旗艦 Qwen3.8-2.4T-A95B 是自訂的「Qwen3.8-Max License」 | 尺寸最齊、中文強 | 本地小模型、中文任務、要微調（工具支援最廣） | https://huggingface.co/Qwen |
| DeepSeek | DeepSeek | V4.1-Flash（MoE，多模態，1M context）、V4-Pro | MIT（V4.1-Flash 的 model card：“licensed under the MIT License”） | 大型 MoE、授權寬 | 要寬鬆授權的前沿級權重（自架門檻很高） | https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash |
| Gemma | Google | Gemma 4（E2B、E4B、12B、26B-A4B、31B） | Apache-2.0（Gemma 4 的 HF 標籤和 header 都寫 Apache 2.0） | 手機到單卡的小模型 | 筆電、邊緣裝置、單張消費級 GPU | https://huggingface.co/google/gemma-4-31B-it |
| gpt-oss | OpenAI | gpt-oss-120b、gpt-oss-20b（2025-08）；另有 gpt-oss-safeguard 20b／120b | Apache-2.0 | OpenAI 的開源推理模型 | 要 OpenAI 系的開放權重做推理或 agent | https://huggingface.co/openai/gpt-oss-120b |
| Llama | Meta | Llama 4（Scout、Maverick），仍是最新一代 Llama | 自訂：Llama 4 Community License（700M MAU 門檻、須標「Built with Llama」、衍生模型名稱要以 Llama 開頭） | 舊生態大，已停更 | 既有 Llama 生態或教材相容 | https://huggingface.co/meta-llama/Llama-4-Scout-17B-16E-Instruct |
| Muse Glimmer | Meta | Muse Glimmer 30B（2026-08-10，dense，含 vision encoder） | Apache-2.0，另附 USAGE_POLICY.md | Meta 新一代開源小模型 | 想在單卡上跑 Meta 的 agent 模型 | https://huggingface.co/blog/muse-glimmer 、https://huggingface.co/meta-models/Muse-Glimmer-30B |
| Mistral | Mistral AI | Mistral Large 4（1T-A52B）、Mistral Small 4、Ministral 3（3B／8B／14B） | **分尺寸不同**：Small 4、Ministral 3 為 Apache-2.0；Large 4 是「Mistral Ecosystem Open-Weight License」（修改版 MIT，做 Model-as-a-Service 商用要另簽約） | 歐洲系，尺寸分層 | 小尺寸要 Apache；歐盟合規考量 | https://docs.mistral.ai/getting-started/models/models_overview/ |
| GLM | Z.ai（智譜） | GLM-5.3、GLM-5.3-Flash（2026-10） | 自訂「GLM-5.3 License」（MIT 式，但 MaaS 營收超過門檻要另取得授權） | 中國系 agent／coding | 長時程 agent、coding 的開源替代 | https://huggingface.co/zai-org/GLM-5.3 |
| Kimi | Moonshot AI | Kimi-K3（2.8T total／104B active）、Kimi-K3.1-Pro | 自訂「Kimi K3 License」（MIT 式，附 MaaS 營收門檻條款） | 超大 MoE agent 模型 | 要前沿級開源 agent 模型、有叢集可以跑 | https://huggingface.co/moonshotai/Kimi-K3 |

---

### 表 2：微調與本地推理工具（M6）

GitHub 狀態查詢時間 2026-11-17，用 `gh api`。

### 2a. 微調

| 工具 | 定位（≤20 字） | 什麼時候選它 | 授權 | 狀態 | 連結 |
|---|---|---|---|---|---|
| LLaMA-Factory | 零程式碼 YAML／WebUI 微調 | 教學、Lab、想快速換模型（支援 Qwen3.x） | Apache-2.0 | 活躍；**repo 已改名為 `hiyouga/LlamaFactory`**（舊網址會轉址）；最新 release v0.9.5（2026-05-30），main 分支持續有 commit | https://github.com/hiyouga/LlamaFactory |
| Unsloth | 單卡省顯存的快速微調 | 單張消費級 GPU、Colab，要 QLoRA 和 GGUF 匯出 | **雙授權**：核心套件 Apache-2.0，Studio UI 等選配元件 AGPL-3.0 | 活躍（v0.1.918-beta，2026-11-16）；已擴成 Desktop／Studio（web UI）／Core 三種用法，也能跑推理 | https://github.com/unslothai/unsloth |
| HF TRL ＋ PEFT | 官方底層訓練庫 | 要自己寫訓練迴圈，做 SFT／DPO／GRPO | 兩者都是 Apache-2.0 | 活躍（TRL v1.18.0、PEFT v0.21.3，都是 2026-11-13） | https://github.com/huggingface/trl 、https://github.com/huggingface/peft |
| Axolotl | YAML 驅動的多卡微調 | 多 GPU／多節點、要可重現的設定檔 | Apache-2.0 | 活躍（v0.21.1，2026-10-27） | https://github.com/axolotl-ai-cloud/axolotl |
| ms-swift | ModelScope 全流程訓練 | 中國模型、多模態，CPT／SFT／DPO／GRPO 全包 | Apache-2.0 | 活躍（v4.6.1，2026-11-13） | https://github.com/modelscope/ms-swift |
| torchtune（不推薦） | PyTorch 原生後訓練庫 | 不建議新專案採用 | BSD-3-Clause | **已停止積極維護**（README：“development wound down in 2025”）；repo 移到 `meta-pytorch/torchtune` | https://github.com/meta-pytorch/torchtune |

### 2b. 推理／服務

| 工具 | 定位（≤20 字） | 什麼時候選它 | 授權 | 狀態 | 連結 |
|---|---|---|---|---|---|
| Ollama | 一行指令跑本地模型 | 課堂 demo、個人開發、OpenAI 相容 `/v1` | MIT | 活躍（v0.40.16，2026-11-09） | https://github.com/ollama/ollama |
| llama.cpp | C/C++ 推理、GGUF 量化 | CPU、Mac、邊緣裝置，要細調量化（Ollama 和 LM Studio 底層都用它） | MIT | 活躍；**2026-11-13 發布 v1.0.0**（移除已棄用的舊 public API）；repo 在 `ggml-org` 下（舊 `ggerganov/llama.cpp` 會轉址） | https://github.com/ggml-org/llama.cpp |
| vLLM | 高吞吐 GPU 服務引擎 | 生產環境多人併發、OpenAI 相容 server（PagedAttention） | Apache-2.0 | 活躍（v0.34.0，2026-11-16） | https://github.com/vllm-project/vllm |
| SGLang | 高效能 LLM／多模態服務 | 多輪、前綴共用多（RadixAttention）、大型 MoE 部署 | Apache-2.0 | 活躍（v0.5.23，2026-11-02）；文件寫由 LMSYS 託管 | https://github.com/sgl-project/sglang |
| LM Studio | 圖形介面的本地模型 App | 不想碰命令列、Mac（MLX）／Windows 桌機 | **App 為閉源**（app-terms：限個人／內部業務使用，禁止轉授權和 SaaS）；CLI `lms` 為 MIT | 活躍；2026-07 推出獨立的 agent App「Bionic」，官網首頁改主推 Bionic，但官方文件寫明是「separate app」，LM Studio 本體照常可用 | https://lmstudio.ai/docs-md/bionic 、https://lmstudio.ai/app-terms 、https://github.com/lmstudio-ai/lms |
| TGI（不推薦） | HF 舊推理伺服器 | 不建議新專案；只在維護既有部署時碰 | Apache-2.0 | **已進入維護模式，GitHub repo 已封存（archived=true）**；README 要大家改用 vLLM、SGLang、llama.cpp、MLX | https://github.com/huggingface/text-generation-inference |

---

### Notes / gotchas

1. **「開源」不等於 Apache。同一家族旗艦和小尺寸授權不同**，簡報授權欄要寫到尺寸層級：
   - Qwen3.8-2.4T-A95B：自訂「Qwen3.8-Max License」，產品月活超過 1 億或月營收超過 2,000 萬美元要在 UI 標示模型名；做 MaaS 或 AI 工作助理業務、年營收超過 5,000 萬美元要另取授權。Qwen3.8-27B 和 Qwen3.6 照樣是 Apache-2.0。來源：https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B/raw/main/LICENSE 、https://huggingface.co/Qwen/Qwen3.8-27B
   - Mistral Large 4：「Mistral Ecosystem Open-Weight License」（修改版 MIT），MaaS 業者商用要另簽約；Small 4 和 Ministral 3 是 Apache-2.0。來源：https://huggingface.co/mistralai/Mistral-Large-4-1T-A52B/raw/main/LICENSE
   - GLM-5.3、Kimi-K3 都是「MIT 樣式＋MaaS 營收門檻」的自訂授權，HF 標籤顯示 `license:other`。**注意 Mistral 文件把 GLM 5.3 標成 MIT，跟 Z.ai repo 的 LICENSE 實文不一致，以 repo 為準。** 來源：https://huggingface.co/zai-org/GLM-5.3/raw/main/LICENSE 、https://huggingface.co/moonshotai/Kimi-K3/raw/main/LICENSE 、https://docs.mistral.ai/getting-started/models/models_overview/
   - Llama 4：自訂 Community License，有 700M MAU 門檻，必須標「Built with Llama」，用 Llama 產出訓練並散布的模型，名稱要以「Llama」開頭。來源：https://huggingface.co/meta-llama/Llama-4-Scout-17B-16E-Instruct
2. **Meta 的開源路線換品牌**：2026 年沒有官方的 Llama 5。新的開源模型叫 Muse Glimmer（30B，Apache-2.0，2026-08-10），旗艦 Muse Spark 是閉源；Meta 宣布會開放 Muse Spark 1.2 的權重，但目前只是計畫。網路上「Llama 5 600B 已發布」的說法只出自低品質網站，未核實，不要上投影片。來源：https://huggingface.co/blog/muse-glimmer 、https://fortune.com/2026/08/10/meta-brandishes-open-source-ai-models-again-as-zuckerberg-media-blitz-emphasizes-battle-against-chinese-rivals/
3. **Gemma 4 改成 Apache-2.0**：舊的 Gemma 1–3 用自訂的 Gemma Terms of Use（舊代授權這次沒有重新開頁核實）；Gemma 4 的 HF 標籤寫 apache-2.0。如果簡報有「Gemma 授權有限制」的舊說法要改。來源：https://huggingface.co/google/gemma-4-31B-it
4. **TGI 已封存**：維護模式加上 repo archived。舊教學出現 TGI 一律換成 vLLM 或 SGLang。來源：https://github.com/huggingface/text-generation-inference
5. **torchtune 停止維護**（2025 年收尾），repo 移到 `meta-pytorch`。不要列成推薦選項。來源：https://github.com/meta-pytorch/torchtune
6. **LLaMA-Factory 改名**：repo 名稱是 `hiyouga/LlamaFactory`，舊的 `LLaMA-Factory` 網址會轉址，CLI 照樣是 `llamafactory-cli`（見 M6 素材）。最新正式 release 停在 v0.9.5（2026-05-30），已經半年沒有新 release，但 main 分支持續有 commit。來源：https://github.com/hiyouga/LlamaFactory/releases/tag/v0.9.5
7. **Unsloth 授權陷阱**：`pip install unsloth` 核心是 Apache-2.0，但 Studio UI 是 AGPL-3.0。拿 Studio 改版對外提供服務要注意 copyleft。來源：https://github.com/unslothai/unsloth （README 的 License 節、COPYING 檔）
8. **LM Studio 不是開源軟體**：App 是閉源專有授權（只有 CLI `lms` 是 MIT）。官網首頁現在主推 Bionic（另一個 agent App），學生可能找不到原本的 LM Studio 下載點。來源：https://lmstudio.ai/app-terms 、https://lmstudio.ai/docs-md/bionic
9. **llama.cpp v1.0.0（2026-11-13）移除了已棄用的 public API**：直接綁 C API 的舊範例或 binding 可能會壞；只透過 Ollama 或 `llama-server` 使用的話不受影響。來源：https://github.com/ggml-org/llama.cpp/releases/tag/v1.0.0
10. **Gemini 文件搬家**：`ai.google.dev/gemini-api/docs/models` 會 301 轉到 `aistudio.google.com/docs/models`；Gemini 2.5 Flash／Pro 已棄用。來源：https://aistudio.google.com/docs/models
11. **DeepSeek API**：舊名 `deepseek-v4-flash` 仍可呼叫，但會被導到 V4.1-Flash-1017；`deepseek-chat` 和 `deepseek-reasoner` 定價頁都沒提到，**仍未核實**（與 product-facts 一致）。來源：https://api-docs.deepseek.com/quick_start/pricing
12. **gpt-oss 必須用 harmony 格式**，model card 原文：“will not work correctly otherwise”。用 Ollama／vLLM 時框架會處理；自己拼 prompt 會出錯。來源：https://huggingface.co/openai/gpt-oss-120b
13. 商業 API 型號約每季更新，**投影片寫家族名，不寫死型號**（與 product-facts 的 GPT-4o 教訓一致）。

### UNVERIFIED／刻意省略

- OpenAI GPT-6 各型號（Astra／Sol／Terra／Luna）之間的定位差異：models 頁只列名稱，沒有逐一核對，表內只寫官方「從 Astra 開始」那句。
- Grok 沒有開源權重的現行版本：沒查。
- Muse Glimmer 的 USAGE_POLICY.md 內容沒細讀，只確認有這份檔案和「未滿 18 歲不得使用」聲明。
- 沒有放任何 star 數、benchmark、參數效能比較。

---

## 選型比較表 B：RAG 與 GraphRAG（M3／M4）

查核日期：2026-11-17。授權、封存狀態、最新版本來自 GitHub repo API（`/repos/{r}`、`/releases/latest`、`/license`）、PyPI JSON API、Hugging Face model API，再加上下表列出、實際打開過的官方頁面。「狀態」欄寫的是最新 release 標籤與日期。

---

### 表 1：向量庫（M3）

| 名稱 | 類型 | 原生混合檢索（BM25＋向量） | 定位（≤20 字） | 什麼時候選它 | 授權 | 狀態（2026-11） | 官方連結 |
|---|---|---|---|---|---|---|---|
| Chroma | 嵌入式 lib／可自架 server／Cloud | **本地版：否**；Chroma Cloud：是（Search API，BM25／SPLADE＋RRF） | 上手最快的 AI 向量庫 | 教學、原型、單機 Lab（本課 Lab3） | Apache-2.0 | 運作中；最新 release 1.5.9（2026-05-05），repo 持續有 commit | https://docs.trychroma.com/cloud/search-api/overview |
| Qdrant | Server（Rust）／Cloud | 是：Query API 的 prefetch＋`rrf` 由 server 端融合；server 端可用 `qdrant/bm25` 從文字產生 BM25 稀疏向量 | 高效能、過濾強的向量庫 | 要正式上線，又要重度 metadata 過濾 | Apache-2.0 | 運作中；v1.20.2（2026-11-16） | https://qdrant.tech/documentation/concepts/hybrid-queries/ |
| Milvus | 分散式 server／Lite／Zilliz Cloud | 是：內建 BM25 全文檢索（server 端從原文產生稀疏向量）＋RRFRanker（k 預設 60） | 億級規模的分散式向量庫 | 資料量極大，要水平擴展 | Apache-2.0 | 運作中；v3.0.6（2026-11-11），已進 3.x 大版 | https://milvus.io/docs/full-text-search.md |
| pgvector | Postgres 擴充 | **否**（官方 README 建議搭配 Postgres 全文檢索，自己用 RRF 或 cross-encoder 合併；`ts_rank` 不是 BM25） | 讓 Postgres 直接存向量 | 已經在用 Postgres，不想多維運一套 DB | PostgreSQL License（BSD 類寬鬆授權） | 運作中；README 安裝指令寫 v0.8.7 | https://github.com/pgvector/pgvector |
| FAISS | 函式庫（C++／Python） | 否（只做 ANN 索引，沒有 BM25、沒有 DB 功能） | Meta 的 ANN 演算法函式庫 | 研究、離線批次、要自己控制索引 | MIT | 運作中；v1.16.0（2026-11-10） | https://github.com/facebookresearch/faiss |
| Weaviate | Server（Go）／Cloud | 是：`hybrid` 查詢＝BM25F＋向量，用 `alpha` 調權重；預設融合是 relativeScoreFusion（v1.24 起），也可選 rankedFusion | 內建混合檢索的向量 DB | 想要開箱即用的混合檢索與模組 | BSD-3-Clause；**但 repo 內 `wl/` 目錄是 Weaviate 企業授權**（2026 新增） | 運作中；v1.40.5（2026-11-10） | https://docs.weaviate.io/weaviate/search/hybrid |
| Elasticsearch | 搜尋引擎 | BM25＋kNN 可以一起查；**RRF retriever 需要 Enterprise 授權**（官方人員 2025-06 回覆） | 老牌全文搜尋加向量 | 公司已經在用 ES，且有 Enterprise 授權 | AGPLv3／SSPL／ELv2 三擇一（預設） | 運作中；v9.5.6（2026-11-02） | https://www.elastic.co/docs/reference/elasticsearch/rest-apis/reciprocal-rank-fusion |
| OpenSearch | 搜尋引擎 | 是：`hybrid` 查詢＋normalization processor；score-ranker processor（RRF）從 2.19 起提供 | 開源版 ES 加混合檢索 | 要 ES 生態又要免費 RRF | Apache-2.0 | 運作中；3.9.0（2026-09-29） | https://docs.opensearch.org/latest/search-plugins/search-pipelines/score-ranker-processor/ |
| LanceDB | 嵌入式 lib（Lance 欄式格式）／Enterprise | 是：OSS 嵌入式就能做 FTS＋向量，預設 RRF（rerank 在應用端執行） | 檔案型、多模態向量庫 | 嵌入式又要混合檢索，或是多模態資料湖 | Apache-2.0 | 運作中；v0.41.0（2026-10-29） | https://docs.lancedb.com/search/hybrid-search |

---

### 表 2：Embedding 與 Reranker 模型（M3）

| 模型 | 類型 | 開放權重／API | 多語／中文 | 什麼時候選它 | 授權 | 連結 |
|---|---|---|---|---|---|---|
| BAAI/bge-m3 | Embedding（dense＋sparse＋multi-vector） | 開放權重 | 100+ 語言，中文強 | 本地、多語，或想用一個模型同時產出稀疏與稠密向量（本課 Lab） | MIT | https://huggingface.co/BAAI/bge-m3 |
| BAAI/bge-reranker-v2-m3 | Reranker（cross-encoder） | 開放權重 | 多語（base／large 只支援中英） | 本地、多語精排（本課 Lab） | Apache-2.0 | https://huggingface.co/BAAI/bge-reranker-v2-m3 |
| Qwen3-Embedding（0.6B／4B／8B） | Embedding | 開放權重 | 100+ 語言（含程式語言），有報 C-MTEB 成績 | 要比 bge-m3 新、支援長文（32K）與自訂維度（MRL）；需要 transformers ≥ 4.51 | Apache-2.0 | https://huggingface.co/Qwen/Qwen3-Embedding-0.6B |
| Qwen3-Reranker（0.6B／4B／8B） | Reranker | 開放權重 | 多語（同系列） | 有 GPU，想要比 bge-reranker 更強的 LLM 型精排 | Apache-2.0 | https://huggingface.co/Qwen/Qwen3-Reranker-0.6B |
| nomic-embed-text v1.5 | Embedding | 開放權重（Ollama 可直接拉） | **只有英文**；多語要用 v2-moe | 用 Ollama 跑英文語料的最省事選擇；**必須加 `search_query:`／`search_document:` 前綴** | Apache-2.0 | https://huggingface.co/nomic-ai/nomic-embed-text-v1.5 |
| OpenAI text-embedding-3-small／-large | Embedding | API | 多語（官方指南頁沒寫語言數） | 已經在用 OpenAI，不想自己架模型；預設 1536／3072 維，可用 `dimensions` 截短 | 商用 API | https://developers.openai.com/api/docs/guides/embeddings |
| Cohere embed-v5.0-pro／-fast（另有 v4.0） | Embedding（文字＋圖片） | API | 100+ 語言（Embed 5） | 要託管的多模態 embedding | 商用 API | https://docs.cohere.com/docs/cohere-embed |
| Cohere rerank-v5.0-pro／-fast | Reranker | API | 多語 | 不想自架 reranker（官方建議新專案用 v5.0-pro） | 商用 API | https://docs.cohere.com/docs/models |
| Jina embeddings v3／v5-text；jina-reranker-v3 | Embedding／Reranker | 開放權重＋API | 多語（v4：30+ 語言） | 只做研究或非商用；商用要走 API 或另外取得授權 | **CC-BY-NC-4.0**（v4 是 Qwen Research License） | https://huggingface.co/jinaai/jina-embeddings-v4 |
| Voyage voyage-4／-4-large／-4-lite（＋開放權重 voyage-4-nano） | Embedding | API；nano 開放權重 | 多語（4-large、4 有標） | 要託管且頂級檢索品質，或要領域模型（code／finance／law） | API 商用；voyage-4-nano 是 Apache-2.0 | https://docs.voyageai.com/docs/embeddings |
| google/embeddinggemma-300m | Embedding | 開放權重（HF 需同意條款） | 多語（UNVERIFIED，未開模型卡確認語言數） | 要極小、可上裝置的 embedding | Gemma 授權（不是 OSI 開源） | https://huggingface.co/google/embeddinggemma-300m |

---

### 表 3：RAG 框架（M3）

| 框架 | 定位（≤20 字） | 什麼時候選它 | 授權 | 狀態（2026-11） | 連結 |
|---|---|---|---|---|---|
| LangChain | Agent 外殼與整合生態 | 要大量整合（模型、向量庫、工具），之後還要接 LangGraph Agent（本課主線） | MIT | 運作中；`langchain` 1.5.0（2026-11-11）。1.x 的核心是 `create_agent`，底層跑在 LangGraph 上；舊 retriever 移到 `langchain_classic` | https://docs.langchain.com/oss/python/langchain/overview |
| LlamaIndex | 以資料與索引為中心的 RAG | 重點在文件解析、切塊、索引策略（例如 `SemanticSplitterNodeParser`） | MIT | 運作中；v0.14.26（2026-11-13）。**README 說公司主力已轉向 LlamaParse，OSS 框架保留為 open toolkit** | https://github.com/run-llama/llama_index |
| Haystack | 明確可控的生產級管線 | 要元件化、型別清楚、好測試的 pipeline，部署到正式環境 | Apache-2.0 | 運作中；已進入 3.x（v3.5.0，2026-11-10） | https://github.com/deepset-ai/haystack |
| RAGFlow | 開箱即用的 RAG 平台 | 不想寫程式，要 Web UI、深度文件解析與 Agent；用 Docker 部署 | Apache-2.0 | 運作中；**v1.0.0（2026-11-06）**。建議 4 核、16 GB RAM、50 GB 硬碟起跳 | https://github.com/infiniflow/ragflow |

---

### 表 4：Graph／GraphRAG 工具（M4）

| 名稱 | 是什麼 | 什麼時候選它 | 授權 | 狀態（2026-11） | 連結 |
|---|---|---|---|---|---|
| Neo4j | LPG 圖資料庫，用 Cypher 查詢 | 要成熟的圖資料庫、豐富教材與 GDS 演算法（本課 Lab4） | **Community：GPLv3**（官方授權頁定位為免費、主要供內部非正式環境使用）；Enterprise：閉源元件，需商業合約；另有 AuraDB Free 雲端免費層 | 運作中；年月版號 2026.xx，2026.02 起新資料庫預設 Cypher 25 | https://neo4j.com/licensing/ |
| Microsoft GraphRAG | 社群摘要式 GraphRAG 研究實作 | 要研究或重現 Global／Local／DRIFT 查詢；索引成本高，建議從小資料開始 | MIT | **大致進入維護模式**：不收新 PR、不加新功能，只修 bug、更新相依套件；v3.3.0（2026-10-08） | https://github.com/microsoft/graphrag |
| LightRAG | 輕量 KG-RAG，Microsoft GraphRAG 的替代方案 | 要比 MS GraphRAG 便宜又有 local／global／hybrid／naive／mix 五種模式，後端可接 PG／Neo4j 等 | MIT | 很活躍；PyPI 1.5.7（2026-09-02），GitHub 有 v1.5.8rc1（2026-11-15）。注意：server 預設綁定所有網卡且不開認證 | https://github.com/HKUDS/LightRAG |
| neo4j-graphrag-python | Neo4j 官方的建圖＋檢索套件 | 在 Neo4j 上建圖（`SimpleKGPipeline`）、做實體消歧、Vector／Hybrid／Text2Cypher 檢索 | Apache-2.0（部分程式碼是 PSF 授權） | 運作中；1.24.0（2026-11-10）；`SimpleKGPipeline` 仍標 experimental | https://neo4j.com/docs/neo4j-graphrag-python/current/user_guide_kg_builder.html |
| LangChain `LLMGraphTransformer`（langchain-neo4j） | 用 LLM 從文字抽出節點與關係 | 已經在用 LangChain，想快速把文件轉成圖寫進 Neo4j | MIT | 運作中；`langchain-neo4j` 0.11.0（2026-10-09）。import 要從 `langchain_neo4j`；舊的 `langchain_experimental` 路徑已在 sunset | https://github.com/langchain-ai/langchain-neo4j |
| Memgraph | 記憶體內圖資料庫，相容 Cypher／Bolt | 要低延遲的即時圖查詢，又想沿用 Neo4j 驅動 | **BSL 1.1**（社群版）＋Memgraph Enterprise License；不是 OSI 開源 | 運作中；v3.14.0（2026-10-21）；官方自稱 GraphRAG／AI memory 的圖引擎 | https://memgraph.com/docs |
| FalkorDB | 以稀疏矩陣（GraphBLAS）實作的圖資料庫，是 Redis 模組 | 要低延遲的 GraphRAG 或多租戶圖，已經在用 Redis | **SSPLv1**（不是 OSI 開源） | 運作中；v6.0.4（2026-11-05） | https://github.com/FalkorDB/FalkorDB |

---

### Notes / gotchas

1. **Chroma 首頁寫「dense, sparse, and hybrid search」，但 Search API（BM25／SPLADE＋RRF）只在 Chroma Cloud 提供**，原文是「Search API is available in Chroma Cloud only」，並說本地版之後會支援。所以 Lab3 仍要自己做 BM25 和 RRF，跟 product-facts 一致。來源：https://docs.trychroma.com/docs/overview/introduction 、https://docs.trychroma.com/cloud/search-api/overview
2. **Chroma 最新 GitHub release 停在 1.5.9（2026-05-05）**，半年沒有新 release，但 repo 在 2026-11-13 仍有 commit。目前判斷是「運作中、release 節奏慢」，不算停更。來源：GitHub API `chroma-core/chroma`、PyPI `chromadb`。
3. **Elasticsearch 的 RRF 需要付費 Enterprise 授權**。免費（Basic）自架版呼叫 RRF 會收到 403「license non-compliant」。投影片若寫「ES 原生支援 RRF 混合檢索」，要補「需付費授權」；免費替代是 OpenSearch（Apache-2.0，2.19 起有 RRF）。來源：https://discuss.elastic.co/t/use-of-retrievers-in-the-search-api/379145 （Elastic 員工，2025-06-13）、https://docs.opensearch.org/latest/search-plugins/search-pipelines/score-ranker-processor/
4. **Weaviate 授權有變化**：repo LICENSE 現在寫明 `wl/` 目錄是「Copyright Weaviate BV 2026-present, all rights reserved」，只能透過企業授權使用，其他部分仍是 BSD-3。課堂上寫「BSD-3（部分企業功能另授權）」最精確。來源：GitHub API `/repos/weaviate/weaviate/license`。
5. **Weaviate 混合檢索的預設融合不是 RRF**，從 v1.24 起預設是 relativeScoreFusion。拿它對照 RRF 時要講清楚。來源：https://docs.weaviate.io/weaviate/search/hybrid
6. **pgvector 本身沒有 BM25**。官方建議是 Postgres 全文檢索（`ts_rank_cd`）加上 RRF 或 cross-encoder 合併，而 `ts_rank` 不是 BM25。來源：https://github.com/pgvector/pgvector
7. **Qdrant 可以在 server 端從文字產生 BM25**（`qdrant/bm25`）。至於「從哪一版開始」「OSS 自架版能不能用」，官方頁沒寫；1.15.2 這個版本號只出現在課程頁和第三方套件說明，屬於 UNVERIFIED，投影片不要寫版本號。來源：https://qdrant.tech/documentation/inference/inference-bm25/
8. **Kùzu（嵌入式圖資料庫）已在 2025-10-10 封存**（README：「Kuzu is working on something new!」）。若有舊教材推薦 Kùzu 當輕量 GraphRAG 後端，要拿掉。來源：https://github.com/kuzudb/kuzu
9. **Microsoft GraphRAG 維護模式已再確認**。README 原文：「This project is largely in maintenance mode, and won't be accepting new PRs or implementing new features. We'll perform bug fixes and dependency updates as appropriate…」，最新版仍是 v3.3.0（2026-10-08）。跟 product-facts 一致。來源：https://github.com/microsoft/graphrag （README raw）
10. **LlamaIndex 的定位變了**：README 說公司重心轉向 LlamaParse（agentic OCR／解析），OSS 框架保留為「open toolkit」。它還在更新（v0.14.26，2026-11-13），但不再是公司主力。來源：https://github.com/run-llama/llama_index
11. **Jina 與 Voyage 都已被收購**。Elastic 在 2025-10-09 完成收購 Jina AI；Voyage 的 HF repo 目前放在 MongoDB 組織底下（模型卡沒寫收購，「MongoDB 收購 Voyage」這句本次 UNVERIFIED）。Jina 開放權重多數是 **CC-BY-NC-4.0，不能商用**；jina-embeddings-v4 的模型卡更正為 Qwen Research License。來源：https://ir.elastic.co/News--Events/news/news-details/2025/Elastic-Completes-Acquisition-of-Jina-AI-a-Leader-in-Frontier-Models-for-Multimodal-and-Multilingual-Search/default.aspx 、https://huggingface.co/jinaai/jina-embeddings-v4 、https://huggingface.co/voyageai/voyage-4-nano
12. **Cohere 已推出 Embed 5 與 Rerank 5**（`embed-v5.0-pro/fast`、`rerank-v5.0-pro/fast`），官方建議新專案用 rerank-v5.0-pro。舊教材常寫的 `rerank-v3.5`、`embed-v3` 都已過時。來源：https://docs.cohere.com/docs/models
13. **OpenAI 沒有比 text-embedding-3 更新的 embedding 模型**，指南頁仍然只列 3-small／3-large（還有 ada-002 做對照）。來源：https://developers.openai.com/api/docs/guides/embeddings
14. **nomic-embed-text v1.5 只支援英文，而且必須加前綴**。課程若用 Ollama `nomic-embed-text` 處理中文語料，效果會差，中文請改用 bge-m3 或 Qwen3-Embedding。來源：https://huggingface.co/nomic-ai/nomic-embed-text-v1.5
15. **授權不是 OSI 開源的圖資料庫**：Memgraph（BSL 1.1）、FalkorDB（SSPLv1）、Neo4j Enterprise（商業）。Neo4j Community 是 GPLv3，官方授權頁把它歸在「開發者方案、主要供內部非正式環境使用」。來源：GitHub API LICENSE（memgraph、FalkorDB）、https://neo4j.com/licensing/
16. **Milvus 已進入 3.x**（server v3.0.6、pymilvus 3.0.3）。舊教材寫的 2.x 語法要確認還能不能用（本次沒有逐項檢查 API 相容性）。BM25 全文檢索在 v3 文件裡是內建功能，起始版本本次沒有查證。來源：https://milvus.io/docs/full-text-search.md
17. **Haystack 已到 3.x，RAGFlow 剛發 1.0**。如果舊教材寫的是 Haystack 2.x 的 API，要對照 3.x 文件（本次沒有逐項檢查）。
18. 沒有寫進表格的數字：各家 benchmark 分數、價格、星數。全部刻意省略。

---

## 技術選型表 C：Agent 設計模式／框架／結構化輸出（核實日 2026-11-17）

> 每列的連結都在 2026-11-17 實際開啟過（WebFetch、GitHub API 或 PyPI JSON API）。版本號與日期來自 PyPI JSON API 與 GitHub API。
> 跟 `product-facts.md`、`M5-agent-langgraph.md`、`M2-prompt-structured-output.md` 沒有衝突，只有更新：langgraph 1.2.20 → 1.2.22、deepagents 0.7.35 → 0.7.39。

---

### 表 1：Agent 設計模式（M5）

「誰決定下一步」欄：**程式**＝寫死的路徑；**模型**＝LLM 在執行時決定；**混合**＝模型挑選，程式負責分派或收斂。

| 模式 | 誰決定下一步 | 一句話 | 什麼時候選 | 成本／風險 | 參考實作 |
|---|---|---|---|---|---|
| Prompt chaining（提示鏈） | 程式 | 固定步驟串接，中間設檢查閘 | 能拆成固定子任務 | 延遲疊加；前一步錯，後面跟著錯 | [Anthropic](https://www.anthropic.com/engineering/building-effective-agents)／[LangGraph](https://docs.langchain.com/oss/python/langgraph/workflows-agents) |
| Routing／Router（路由） | 混合：模型分類，程式分派 | 先分類，再交給專責流程或 agent | 類別清楚、各類別要不同處理 | 分錯類全盤皆錯；多輪對話用起來不順 | [Anthropic](https://www.anthropic.com/engineering/building-effective-agents)／[LangChain Router](https://docs.langchain.com/oss/python/langchain/multi-agent/router) |
| Parallelization（平行：分段／投票） | 程式 | 子任務同時跑，或同一題跑多次再投票 | 子任務彼此獨立、要求速度或信心 | token 隨分支數倍增；最後要合併結果 | [Anthropic](https://www.anthropic.com/engineering/building-effective-agents)／[LangGraph](https://docs.langchain.com/oss/python/langgraph/workflows-agents) |
| Orchestrator-workers（指揮者－工人） | 混合：模型拆任務，程式用 `Send` 扇出 | 中央 LLM 拆任務、派工、彙整 | 事先不知道要拆成哪些子任務 | 拆題品質決定成敗；token 多 | [Anthropic](https://www.anthropic.com/engineering/building-effective-agents)／[LangGraph](https://docs.langchain.com/oss/python/langgraph/workflows-agents) |
| Evaluator-optimizer／Reflection（評估－改寫） | 混合：程式管迴圈，模型判斷是否通過 | 一個生成、一個評分，迴圈改到通過 | 評分標準明確，且多改幾輪確實會更好 | 每輪多一次推論；沒有外部依據的自評可能改不出更好的結果 | [Anthropic](https://www.anthropic.com/engineering/building-effective-agents)／[LangGraph](https://docs.langchain.com/oss/python/langgraph/workflows-agents)／[LangChain 部落格](https://www.langchain.com/blog/reflection-agents) |
| ReAct／工具呼叫迴圈（自主 agent） | 模型 | 想、呼叫工具、看結果，重複到完成 | 開放式問題，步數無法預估 | 錯誤會累積；成本與延遲不可控，要設上限 | [Anthropic](https://www.anthropic.com/engineering/building-effective-agents)／[create_agent](https://docs.langchain.com/oss/python/langchain/agents)／[論文](https://arxiv.org/abs/2210.03629) |
| Plan-and-execute（先規劃再執行） | 模型（規劃者） | 先列計畫，再逐步執行，必要時重新規劃 | 長任務，要讓人看得到進度 | 計畫可能過時；舊版 LangGraph 範例已封存 | [LangChain 部落格](https://www.langchain.com/blog/planning-agents)；現行做法見 [TodoListMiddleware](https://docs.langchain.com/oss/python/langchain/middleware/built-in) |
| Subagents／Supervisor（子 agent 包成工具） | 模型（主 agent） | 主 agent 把子 agent 當工具呼叫，子 agent 只回摘要 | 多個領域、可平行處理、需要集中控管 | 每次都要經主 agent 轉手，模型呼叫次數多 | [LangChain Subagents](https://docs.langchain.com/oss/python/langchain/multi-agent/subagents)／[Supervisor 教學](https://docs.langchain.com/oss/python/langchain/supervisor) |
| Handoffs（交棒，swarm 屬此類） | 模型（以工具呼叫改 state） | 現任 agent 用工具把控制權交給下一位 | 使用者要直接和專員對話、流程有先後 | 交棒時訊息歷史容易壞掉或膨脹 | [LangChain Handoffs](https://docs.langchain.com/oss/python/langchain/multi-agent/handoffs)／[OpenAI SDK](https://openai.github.io/openai-agents-python/multi_agent/) |
| Skills（按需載入專業知識） | 模型 | 單一 agent 需要時才載入專業提示與知識 | 任務單純、同類請求會重複出現 | 載入的內容會留在 context 裡越積越多 | [LangChain Skills](https://docs.langchain.com/oss/python/langchain/multi-agent/skills)／[Anthropic](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) |
| Custom workflow（自訂圖） | 混合 | 確定性節點和 agent 節點混在一張圖 | 要精準控制，其他模式當節點用 | 開發與維護成本最高 | [LangChain Custom workflow](https://docs.langchain.com/oss/python/langchain/multi-agent/custom-workflow) |

**佐證數字（LangChain 多智能體頁的比較表，2026-11-17）**：同一個「買咖啡」單次請求，Subagents 要 4 次模型呼叫，Handoffs、Skills、Router 各 3 次；三個語言領域的多領域任務，Subagents 約 9K token、Handoffs 7+ 次呼叫、約 14K+ token、Skills 約 15K token。出處：https://docs.langchain.com/oss/python/langchain/multi-agent

---

### 表 2：Agent 框架／SDK（M5）

| 框架 | 開發者 | 抽象層級 | 可換模型？ | 什麼時候選 | 授權 | 狀態（2026-11-17） | 連結 |
|---|---|---|---|---|---|---|---|
| LangGraph | LangChain | 低階：圖／狀態機 | 是 | 確定性步驟與 agent 步驟混合的流程 | MIT | 1.2.22（2026-11-14），穩定版 | [docs](https://docs.langchain.com/oss/python/langgraph/overview)／[GitHub](https://github.com/langchain-ai/langgraph) |
| LangChain `create_agent` | LangChain | 高階：單一 agent＋middleware | 是 | 要能高度客製的 agent 外殼（harness） | MIT | 1.5.0（2026-11-11），跑在 LangGraph 上 | [docs](https://docs.langchain.com/oss/python/langchain/overview) |
| Deep Agents | LangChain | 高階 harness：規劃＋子 agent＋檔案系統 | 是 | 長任務、要開箱即用的 harness | MIT | 0.7.39（2026-11-16），標示為 Beta | [docs](https://docs.langchain.com/oss/python/deepagents/overview)／[GitHub](https://github.com/langchain-ai/deepagents) |
| OpenAI Agents SDK | OpenAI | 高階：agent＋handoffs＋guardrails | 部分（預設 OpenAI；透過 LiteLLM／Any-LLM 接其他家） | 用 OpenAI 生態，或需要語音、沙箱 | MIT | 0.24.0（2026-10-15），版本號仍是 0.x | [docs](https://openai.github.io/openai-agents-python/)／[GitHub](https://github.com/openai/openai-agents-python) |
| Claude Agent SDK | Anthropic | 高階 harness：把 Claude Code 當函式庫用 | 否：只能用 Claude（可經 Bedrock／Vertex／Foundry） | 要現成的檔案、終端機工具與權限控管 | repo 是 MIT；使用受 Anthropic 商業條款規範 | 0.2.183（2026-11-16），標示為 Alpha | [docs](https://code.claude.com/docs/en/agent-sdk/overview)／[GitHub](https://github.com/anthropics/claude-agent-sdk-python) |
| Google ADK | Google | 中高階：LLM agent＋流程 agent＋圖 | 是（官方：「almost any model」） | 用 Gemini／GCP，或需要多種程式語言 | Apache-2.0 | 2.14.1（2026-11-12）；2.0 起支援圖形流程 | [docs](https://adk.dev/)／[GitHub](https://github.com/google/adk-python) |
| CrewAI | CrewAI Inc. | 多 agent 角色：Crew＋Flow | 是（預設 OpenAI，可接 Ollama 等） | 想用角色分工快速做出原型 | MIT | 1.15.41（2026-11-12）；不依賴 LangChain | [docs](https://docs.crewai.com/en/introduction)／[GitHub](https://github.com/crewAIInc/crewAI) |
| Microsoft Agent Framework | Microsoft | 高階 agent＋圖形流程 | 是（Foundry、OpenAI、Anthropic、Ollama 等） | .NET／Azure 企業環境 | MIT | Python 1.26.0（2026-11-12），1.0 起提供長期支援；AutoGen 與 Semantic Kernel 的後繼者 | [docs](https://learn.microsoft.com/en-us/agent-framework/overview/)／[GitHub](https://github.com/microsoft/agent-framework) |
| ↳ AutoGen | Microsoft | 多 agent 對話 | — | 新專案不要用 | — | README 標示已封存、不再修安全漏洞；官方建議遷移到 MAF | [GitHub](https://github.com/microsoft/autogen) |
| ↳ Semantic Kernel | Microsoft | — | — | 新專案改用 MAF | MIT | README 寫「SK is now MAF」，仍有發版（1.47.0，2026-11-05） | [GitHub](https://github.com/microsoft/semantic-kernel) |
| AG2 | AG2 社群（從 AutoGen 分出） | 多 agent（Network） | 是 | 原本就在用 AutoGen 0.2 風格的團隊 | Apache-2.0 | 1.3.2（2026-11-15）；舊 API 拆到 ag2-classic | [GitHub](https://github.com/ag2ai/ag2) |
| Pydantic AI | Pydantic 團隊 | 高階：有型別的 agent 迴圈 | 是（換個字串就能換模型，可設備援模型） | 重視型別、結構化輸出與 durable execution | MIT | 2.69.0（2026-11-17），穩定版 | [docs](https://pydantic.dev/docs/ai/overview/)／[GitHub](https://github.com/pydantic/pydantic-ai) |
| smolagents | Hugging Face | 極簡：CodeAgent 用程式碼當動作 | 是 | 教學、讀原始碼、做 code-as-action 實驗 | Apache-2.0 | 最後一次發版 1.26.0（2026-05-29）；repo 仍有提交 | [GitHub](https://github.com/huggingface/smolagents) |
| LlamaIndex Agents／Workflows | LlamaIndex | 事件驅動流程＋預建 agent | 是 | 以文件與 RAG 為核心的 agent | MIT | llama-index 0.14.26；Workflows 2.26.1；定位轉向「文件 agent」 | [docs](https://developers.llamaindex.ai/python/framework/understanding/agent/)／[GitHub](https://github.com/run-llama/llama-agents) |

---

### 表 3：結構化輸出工具（M2）

機制分三類：**提示＋驗證**（事後檢查，失敗就重試）／**原生 JSON Schema**（服務商在伺服器端約束）／**約束解碼**（在本機逐 token 遮罩）。

| 工具 | 機制 | 什麼時候選 | 連結 |
|---|---|---|---|
| Pydantic（2.14.3） | 只負責定義 schema 與驗證，不負責生成 | 所有方案的共同底層 | [GitHub](https://github.com/pydantic/pydantic) |
| OpenAI Structured Outputs | 原生 JSON Schema（`strict: true`） | 用 OpenAI 模型 | [docs](https://developers.openai.com/api/docs/guides/structured-outputs) |
| Anthropic Structured Outputs | 原生（`output_config.format`），伺服器端約束解碼 | 用 Claude 模型 | [docs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) |
| Gemini Structured Output | 原生（`response_json_schema`），只支援 JSON Schema 子集 | 用 Gemini 模型 | [docs](https://aistudio.google.com/docs/structured-output?generate-content=true&hl=en) |
| Ollama `format` | 原生 API 直接吃 JSON Schema | 本機 Lab | [docs](https://docs.ollama.com/capabilities/structured-outputs) |
| LangChain `with_structured_output` | 包一層：`json_schema`／`function_calling`／`json_mode` 三種 | 不用 agent 的鏈，換模型不必改程式 | [docs](https://docs.langchain.com/oss/python/langchain/models) |
| LangChain `create_agent(response_format=)` | 支援原生就走 ProviderStrategy，否則退回 ToolStrategy | agent 最後要回傳型別化結果 | [docs](https://docs.langchain.com/oss/python/langchain/structured-output) |
| Instructor（1.17.0） | 提示＋Pydantic 驗證＋失敗重試 | 只做資料萃取、需要跨服務商 | [docs](https://python.useinstructor.com/) |
| Pydantic AI `output_type` | 用 Pydantic 驗證，失敗就請模型重試 | 已經用 Pydantic AI 寫 agent | [docs](https://pydantic.dev/docs/ai/overview/) |
| Outlines（1.3.3） | 約束解碼：JSON Schema、regex、CFG | 自架模型，要保證格式 | [docs](https://dottxt-ai.github.io/outlines/latest/) |
| vLLM structured outputs | 約束解碼（xgrammar／guidance） | 自架推論服務 | [docs](https://docs.vllm.ai/en/latest/features/structured_outputs.html) |
| llama.cpp GBNF | 約束解碼：文法，或由 JSON Schema 轉成文法 | 在 CPU 或邊緣裝置跑 GGUF 模型 | [docs](https://github.com/ggml-org/llama.cpp/blob/master/grammars/README.md) |
| BAML | 事後解析（SAP），不做約束解碼 | 跨語言、要先寫 prompt 再測試的團隊 | [docs](https://docs.boundaryml.com/home)／[blog](https://boundaryml.com/blog/sota-function-calling) |

---

### Notes／注意事項

1. **AutoGen 已封存（README 層級）。** `microsoft/autogen` 的 README 寫「Project archived and no longer maintained … not providing bug fixes, security fixes」，並建議改用 Microsoft Agent Framework。但 GitHub API 回傳 `archived: false`，repo 仍可寫入，最後 push 是 2026-11-12。投影片寫「官方宣告停止維護」，不要寫「GitHub 唯讀」。PyPI `autogen-agentchat` 最後版本 0.7.5（2025-09-30）。出處：https://github.com/microsoft/autogen
2. **Semantic Kernel 不算封存。** README 寫「Semantic Kernel is now Microsoft Agent Framework」，MAF 1.0 是「production-ready … long-term support」。SK 仍在發版（1.47.0，2026-11-05）。MAF 官方文件稱它「direct successor」，由同一批團隊開發，結合 AutoGen 的抽象與 SK 的企業功能，另外支援 Go（public preview）。出處：https://github.com/microsoft/semantic-kernel 、https://learn.microsoft.com/en-us/agent-framework/overview/
3. **AG2 與 AutoGen 要分開講。** AG2 是 AutoGen 0.2 的社群分支，v1.0 起改用 `import ag2`。原本的 `import autogen`、`ConversableAgent`、`GroupChat`、swarm 都搬到 `ag2ai/ag2-classic`，`pip install ag2` 已經不含 `autogen` 這個 import 名稱。出處：https://github.com/ag2ai/ag2
4. **Plan-and-execute 和 Reflection 沒有現行官方教學頁。** LangGraph repo 的 `examples/` README 寫「retained purely for archival purposes and is no longer updated」，plan-and-execute、reflection、reflexion 三個 notebook 只剩一句「This file has been moved」。2024 年的 LangChain 部落格仍可讀，概念可以引用，但程式碼別照抄。現行的對應做法：規劃用 `TodoListMiddleware`（`write_todos`），自評迴圈用 Deep Agents 的 `RubricMiddleware`（agent 依評分標準自評，滿意前持續修改）。出處：https://github.com/langchain-ai/langgraph/tree/main/examples 、https://docs.langchain.com/oss/python/langchain/middleware/built-in
5. **舊網址會轉址，投影片直接放新網址。** `langchain-ai.github.io/langgraph/tutorials/...` 打開只剩「Redirecting...」。`google.github.io/adk-docs` 已 301 轉到 `adk.dev`，`ai.pydantic.dev` 轉到 `pydantic.dev/docs/ai/overview/`，`ai.google.dev/gemini-api/docs/structured-output` 轉到 `aistudio.google.com/docs/structured-output`。
6. **`langgraph-swarm` 沒有封存，但官方文件已經不提它。** GitHub `archived: false`，PyPI 最後版本 0.1.0（2025-12-04）。LangChain 的 Handoffs 頁完全沒出現 swarm，主推「單一 agent＋middleware 依 state 換 prompt 和工具」。`langgraph-supervisor` 仍是封存狀態（0.0.31）。投影片把 swarm 歸在 handoffs 底下即可，不要教人裝這個套件。出處：https://github.com/langchain-ai/langgraph-swarm-py 、https://docs.langchain.com/oss/python/langchain/multi-agent/handoffs
7. **Router 和 Subagents 的差別。** Router 通常是單一分類步驟，不保留對話狀態；Subagents 由主 agent 動態決定要叫誰，並保留 context。多輪對話官方建議改用 handoffs 或 subagents。出處：https://docs.langchain.com/oss/python/langchain/multi-agent/router
8. **OpenAI 的分法可以拿來搭橋。** OpenAI 把協調方式分成「LLM-driven」和「code-driven」兩類，正好對應表 1 的「誰決定下一步」欄。Agents-as-tools（manager）對應 Subagents，Handoffs 則是「routing itself is part of the workflow」。出處：https://openai.github.io/openai-agents-python/multi_agent/
9. **Anthropic〈Building effective agents〉頁首加了更新說明。** 原文寫工具生態自 2024-12 以來變化很大，並導向「how we built Claude Managed Agents」。五個 workflow 模式和 agent 的取捨（用延遲與成本換表現、錯誤會累積）仍是原文內容，可以照引。
10. **Claude Agent SDK 授權有兩層。** GitHub repo 的 LICENSE 是 MIT，但官方文件寫 SDK 的使用受 Anthropic Commercial Terms 規範，而且 SDK 底下跑的是 Claude Code 執行檔。只能用 Claude 模型，可經 Bedrock、Vertex、Foundry 或 Claude Platform on AWS 存取。第三方產品不得提供 claude.ai 登入。出處：https://code.claude.com/docs/en/agent-sdk/overview 、https://code.claude.com/docs/en/agent-sdk/quickstart.md
11. **LlamaIndex 定位改變。** Workflows 的 repo 改名為 `run-llama/llama-agents`（`run-llama/workflows-py` 會轉到這裡），README 第一句是「framework for building and shipping document-centric agents」，`llama_index` repo 的描述也改成「document processing platform」。出處：https://github.com/run-llama/llama-agents
12. **smolagents 發版放緩。** PyPI 最後一版是 2026-05-29，但 repo 今天仍有 push。可以稱「維護中」，不建議當主力框架。
13. **Gemini 結構化輸出的但書。** 官方寫「syntactically valid JSON string matching the schema」，同時要求在應用程式端驗證數值是否合理。JSON Schema 只支援子集，`minLength`、`maxLength`、`uniqueItems` 等會被直接拿掉、不會報錯，schema 太複雜則回 400。Gemini 2.0 需要明確給 `propertyOrdering`。另有新的 Interactions API 寫法（`response_format`）。這和 M2 的「格式保證，內容不保證」一致。
14. **vLLM 舊參數已移除。** `guided_json`、`guided_regex` 等在 v0.12.0 移除，現在用 `structured_outputs`（放在 `extra_body`）或 `response_format`。lm-format-enforcer 後端自 v0.33.0 起棄用。網路上的舊教程多半還在用 `guided_*`。
15. **llama.cpp 的 JSON Schema 不會放進 prompt。** 轉成文法只約束輸出，模型本身看不到 schema，所以 prompt 裡要另外描述格式（工具呼叫例外）。巢狀 `$ref` 壞掉、`patternProperties` 不支援，遇到不支援的寫法會直接略過。
16. **BAML 走另一條路。** BAML 不做約束解碼，改用事後解析（Schema-Aligned Parsing）修補輸出，原文寫「without using JSON-mode or any kind of constrained generation」（2024-08-13）。它宣稱的準確度優勢是廠商自己的數字，未獨立驗證。另外現有文件站寫的是 BAML v0（legacy），v1 是另一套語言、仍在 public beta。
17. **Instructor 官方自己畫了分工線。** README 寫「Use Instructor for fast extraction, reach for PydanticAI when you need agents」，正好可以當表 3 的選擇規則。
18. **LangChain 結構化輸出的細節。** `create_agent` 直接給 schema 時，會依模型 profile 自動選 Provider 或 Tool 策略，但 JSON Schema dict 不會自動判斷，必須明確包成某個 strategy。遇到拒答時 ProviderStrategy 會拋錯，ToolStrategy 則不回傳 `structured_response`，可以加 `ModelRefusalMiddleware` 讓兩者行為一致。
19. **UNVERIFIED：** Pydantic AI 的 output 預設是走 tool 還是 native，本次沒有查證。（「CrewAI 預設使用 OpenAI」有出處，是 README 的「By default your agents will use the OpenAI API」，只是文件首頁沒寫。）

---

## 技術選型對照表 D：低代碼平台／MCP 積木／可觀測與評測（核實日 2026-11-17）

> 每列來源皆於 2026-11-17 以 WebFetch 實際開啟。標 **UNVERIFIED** 者為查不到一手來源。
> 與 `product-facts.md`（2026-11-12）衝突處見文末 Notes。

---

### 表 1　低代碼／視覺化 Agent 與工作流平台（M7）

| 平台 | 定位 | 自架／開源 | MCP 支援 | 什麼時候選它 | 授權 | 狀態（2026-11） | 連結 |
|---|---|---|---|---|---|---|---|
| **Dify** | LLM 應用＋工作流畫布 | 可自架；原始碼公開 | 雙向：Client 只接 HTTP（不接 stdio）；App 可發布成 MCP Server | 快速做 RAG／Chatflow 交付 | Dify Open Source License（Apache 2.0＋附加條件）：多租戶 SaaS 需書面授權、前端須保留 logo | 活躍，最新 1.19.0（2026-11-04） | https://github.com/langgenius/dify |
| **n8n** | 整合／排程優先的自動化，AI 是節點 | 可自架；source-available | 雙向：MCP Client Tool＋MCP Server Trigger（SSE／Streamable HTTP，不支援 stdio） | 要串大量 SaaS、排程、Webhook | Sustainable Use License（限內部／非商業用）＋ `.ee` 檔走 Enterprise License；**非 OSI 開源**（官方稱 fair-code） | 活躍，最新 n8n@2.48.4（2026-11-13） | https://github.com/n8n-io/n8n |
| **Coze Studio**（扣子開源版） | 字節跳動 Coze 的開源 Agent 開發平台 | 可自架；開源（2025-07 開源） | **UNVERIFIED**（README 與近版 release notes 未提 MCP） | 熟 Coze 生態、要 Go 後端 | Apache 2.0（OSI） | 最新 v0.5.1（Feb，推定 2026）；開源版僅 PAT 認證 | https://github.com/coze-dev/coze-studio |
| **Langflow** | Python 視覺化流程，偏開發者 | 可自架；開源 | 雙向：Client 支援 stdio／HTTP-SSE；Server 為 Streamable HTTP（SSE 備援） | 要視覺化又要能改 Python 元件 | MIT（OSI） | 活躍，最新 1.13.2（Nov 10）；母公司 DataStax 已被 IBM 收購（2025-05 完成） | https://docs.langflow.org/mcp-client |
| **RAGFlow** | 深度文件解析 RAG 引擎＋Agent | 可自架；開源 | 雙向：內建 MCP Server 端點＋可接外部 MCP（傳輸未載明） | 文件（PDF／表格）解析品質優先 | Apache 2.0（OSI） | 活躍，1.0.0（2026-11-06） | https://github.com/infiniflow/ragflow |
| ~~**Flowise**~~ | 視覺化 Agent 建構器 | 程式碼仍可 fork | —（已停止開發） | **新專案不要選** | Apache 2.0 | **已停止維護**：2026-07-29 凍結，repo 2026-08-13 封存，2026-08-31 EOL；2025-08 被 Workday 收購 | https://flowiseai.com/sunset |

---

### 表 2　MCP 積木（M7）

| 項目 | 是什麼 | 什麼時候用 | 連結 |
|---|---|---|---|
| **治理：Agentic AI Foundation（AAIF）** | Linux Foundation 旗下基金；2025-12-09 成立，MCP 為創始專案（另有 goose、AGENTS.md） | 講「MCP 是中立標準」時引用 | https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation |
| **官方 Python SDK `mcp`** | 官方 SDK，最新 2.3.0；v2 起 `FastMCP` 類別改名 `MCPServer`；1.x 為維護線（1.30.0） | 本課 Lab 預設；Python 3.11+ | https://github.com/modelcontextprotocol/python-sdk/releases |
| **官方 TypeScript SDK** | v2 拆成 `@modelcontextprotocol/server`／`client`，實作 2026-07-28 spec；v1 仍為 `@modelcontextprotocol/sdk`（1.32.2） | Node／前端團隊寫 Server／Client | https://github.com/modelcontextprotocol/typescript-sdk |
| **FastMCP（獨立版 `fastmcp`）** | Prefect 維護的高階框架，最新 **4.2.0**（不是 2.x）；官方 SDK 2024 年採用其高階 API | 要 Client、代理、MCP Apps 等進階功能 | https://gofastmcp.com/getting-started/welcome |
| **MCP Inspector** | 官方除錯工具，`npx @modelcontextprotocol/inspector`；v2 有 Web／CLI／TUI | 寫完 Server 先在這裡測工具 | https://github.com/modelcontextprotocol/inspector |
| **官方 MCP Registry** | 只存 Server 中繼資料（`server.json`），不存程式碼；**仍是 preview** | 發布自己的公開 Server（`mcp-publisher`） | https://modelcontextprotocol.io/registry/about |
| **Claude Desktop** | 官方教學示範 Host；macOS／Windows／Linux | 本機 stdio Server 入門 | https://modelcontextprotocol.io/docs/develop/connect-local-servers |
| **Claude Code** | CLI Host；`claude mcp add`；stdio／http（SSE 已棄用）；`.mcp.json` 專案共享 | 開發時讓 coding agent 用工具 | https://code.claude.com/docs/en/mcp |
| **Cursor** | IDE Host；`.cursor/mcp.json`；stdio／SSE／Streamable HTTP；支援 Tools／Prompts／Resources／Roots／Elicitation | IDE 內用 MCP 工具 | https://cursor.com/docs/context/mcp |
| **VS Code（Copilot）** | IDE Host；stdio 與 HTTP（含 SSE）；工作區 `.mcp.json` | 團隊共用 IDE 設定 | https://code.visualstudio.com/docs/copilot/customization/mcp-servers |
| **ChatGPT／OpenAI API** | 只接遠端 URL（未見 stdio）；ChatGPT 以 Plugins／Developer mode 加；API 用 `type:"mcp"` 工具 | 要給 ChatGPT 使用者用 | https://developers.openai.com/api/docs/mcp/ |
| **Cherry Studio** | 桌面 LLM 客戶端；stdio＋SSE／Streamable HTTP；需綁定到 Agent | 本課 Lab7 本機 stdio 跑通 | https://cherryai.com/docs/en/advanced-basic/extensions/mcp/ |

Cherry Studio 授權：AGPL-3.0，另售商業授權（https://github.com/CherryHQ/cherry-studio）。

---

### 表 3　LLM 可觀測性與評測（M8）

| 工具 | 追蹤／評測 | 開源／自架 | 框架無關？ | 什麼時候選它 | 授權 | 狀態（2025–2026 變動） | 連結 |
|---|---|---|---|---|---|---|---|
| **LangSmith** | 兩者 | 閉源 SaaS；自架限 Enterprise 加購 | 是（支援 OTel 匯入 `/otel`） | 用 LangChain／LangGraph | 商業授權 | 活躍 | https://docs.langchain.com/langsmith/self-hosted |
| **Langfuse** | 兩者（＋prompt 管理） | 開源，可自架 | 是（建在 OTel 上） | 要開源自架的 LangSmith 替代 | MIT（`ee/` 除外） | **2026-01 被 ClickHouse 收購**，承諾維持 MIT | https://github.com/langfuse/langfuse |
| **Arize Phoenix** | 兩者 | 可自架（`pip install arize-phoenix`） | 是（OTel＋OpenInference） | 本機一行起、notebook 除錯 | **Elastic License 2.0**（source-available，非 OSI） | 活躍，未見收購 | https://github.com/Arize-ai/phoenix |
| **Helicone** | 追蹤（Gateway／proxy 式） | 開源，Docker 自架 | 是（改 base URL 即可） | 只想看成本／延遲 | Apache 2.0 | **2026-03-03 被 Mintlify 收購，進入維護模式**（不再加新功能） | https://www.developersdigest.tech/blog/llm-observability-acquisitions-2026 |
| **MLflow Tracing** | 兩者 | 開源，自架 | 是（相容 OTel GenAI semconv） | 團隊已在用 MLflow 管模型 | Apache 2.0 | 活躍 | https://mlflow.org/docs/latest/genai/tracing/ |
| **OTel GenAI semconv** | 標準（非產品） | — | 是（定義本身） | 不想綁單一廠商 | Apache 2.0（OTel） | **Status: Development**；已搬到獨立 repo `semantic-conventions-genai`，含 MCP 章節 | https://github.com/open-telemetry/semantic-conventions-genai |
| **OpenLLMetry** | 追蹤（OTel instrumentation） | 開源 | 是 | 想用 OTel 匯出到任何後端 | Apache 2.0 | **Traceloop 2026-03 宣布加入 ServiceNow**；承諾維持開源 | https://www.traceloop.com/blog/traceloop-is-joining-servicenow |
| **Ragas** | 評測（RAG 指標） | 開源 | 是 | 評 RAG：faithfulness 等 | Apache 2.0 | 活躍；GitHub 改到 `vibrantlabsai/ragas` | https://github.com/vibrantlabsai/ragas |
| **DeepEval** | 評測（＋tracing） | 開源 | 是 | 想用 pytest 風格寫 LLM 單元測試 | Apache 2.0 | 活躍；配套 SaaS 為 Confident AI | https://github.com/confident-ai/deepeval |
| **promptfoo** | 評測＋紅隊 | 開源 CLI | 是 | CI 裡比 prompt／模型、做紅隊 | MIT | **2026-03-09 OpenAI 宣布收購**；README 寫仍 MIT 開源 | https://github.com/promptfoo/promptfoo |
| **OpenAI Evals** | 評測 | 開源 repo | 偏 OpenAI | 只用 OpenAI 模型 | MIT | README 導向 OpenAI Dashboard 的 Evals | https://github.com/openai/evals |
| **Inspect（UK AISI）** | 評測（模型／agent 基準） | 開源 | 是 | 做模型能力／安全基準 | MIT | 活躍；200+ 現成評測 | https://github.com/UKGovernmentBEIS/inspect_ai |
| **LangSmith Evals** | 評測 | 同 LangSmith | 是 | 已用 LangSmith 追蹤 | 商業授權 | 活躍 | https://docs.langchain.com/langsmith/evaluation-concepts |

---

### Notes / gotchas

1. **Flowise 已停止維護。** 2026-07-29 凍結、repo 2026-08-13 封存（GitHub API `archived: true`）、2026-08-31 EOL。官方理由是開發者轉向 Claude Code 等 coding agent。官方日程表寫 2026-08-10 封存，GitHub banner 寫 08-13，以 GitHub 為準。投影片不要把它列成選項，只能當「低代碼工具也會消失」的例子。來源：https://flowiseai.com/sunset 、https://api.github.com/repos/FlowiseAI/Flowise
2. **「開源」要分 OSI 與 source-available。** n8n（Sustainable Use License）、Arize Phoenix（ELv2）不是 OSI 開源。Dify 是 Apache 2.0 加條件（多租戶、logo），也不算純 Apache。來源：https://raw.githubusercontent.com/n8n-io/n8n/master/LICENSE.md 、https://raw.githubusercontent.com/langgenius/dify/main/LICENSE 、https://github.com/Arize-ai/phoenix
3. **FastMCP 版本與 brief 不同。** 獨立版 `fastmcp` 現在是 4.2.0（product-facts 11-12 記 4.1.8，期間已有新版）。沒有「FastMCP 2.x」這條現行線。官方 SDK v2.0.0 的 release note 寫明 `FastMCP` 已改名 `MCPServer`，decorator API 不變。v1.30.0 是維護線。來源：https://pypi.org/pypi/fastmcp/json 、https://github.com/modelcontextprotocol/python-sdk/releases
4. **TS SDK v2 改了套件名**（`@modelcontextprotocol/server`／`client`，v2 於 2026-07-27 發布）。npm 上 `@modelcontextprotocol/sdk` 仍是 v1（1.32.2），舊教學的 import 寫法會對不上。來源：https://github.com/modelcontextprotocol/typescript-sdk
5. **AAIF 日期核實相符**：2025-12-09。有一個網站（Business Tech Navigator）寫 2026-05-19，是錯的。來源：Linux Foundation 新聞稿（見表 2）。
6. **MCP Registry 仍是 preview**（2025-09-08 上線、API 凍結在 v0.1），官方也明說程式碼不適合拿去自架。寫成「官方 app store 已 GA」是錯的。
7. **2026 年可觀測／評測工具大量被收購。** Langfuse 被 ClickHouse 收購（2026-01；Orrick 公告 01-26，Langfuse README 寫「Since January 2026」；ClickHouse 部落格頁顯示 2026-07-14，推測是改版日期）。Helicone 被 Mintlify 收購並進入維護模式（2026-03-03）。promptfoo 被 OpenAI 收購（2026-03-09）。Traceloop 加入 ServiceNow（2026-03）。教學重點應放在「用 OTel 保持可攜」。
   - Helicone 官方公告頁（helicone.ai/blog/joining-mintlify）回 404，收購資訊來自二手彙整與搜尋摘要，**一手來源未打開**。
   - OpenAI 官方收購公告頁回 403；改以 promptfoo README「now part of OpenAI」和 TechCrunch／Bloomberg 標題佐證。
   - developersdigest 另列 Galileo→Cisco（2026-05-22）、W&B→CoreWeave（2025-05-05）、Humanloop 關站（2025-09-08）。這三筆不在表內，也**未逐一核實一手來源**。
8. **OTel GenAI semconv 仍是 Development**，並已從主 repo 搬到 `semantic-conventions-genai`（opentelemetry.io 頁面寫「have moved」）。舊連結 `opentelemetry.io/docs/specs/semconv/gen-ai/` 只剩搬家公告。屬性名稱可能還會變。
9. **Langflow 母公司歸屬**：IBM 收購 DataStax，2025-05-28 公告完成（DBTA）。IBM 社群有一篇 2025-10 的文章寫「11/1 完成」，推測指的是業務轉移。來源：https://www.dbta.com/Editorial/News-Flashes/IBM-Officially-Closes-Acquisition-of-DataStax-169711.aspx
10. **Coze Studio 的 MCP 支援未證實**：README 與近版 release notes 都沒提到。字節另有一個獨立的 `coze-mcp-server`，是讓外部呼叫 Coze 用的，跟 Studio 本身能不能當 MCP Client 是兩回事。v0.5.1 頁面沒標年份。GitHub API 回 403，查不到 pushed_at。
11. **ChatGPT 的 MCP 入口名稱一直在變。** 官方文件現在寫「ChatGPT Plugins」；第三方教學多寫 Developer mode（2025-09-09 推出），各方案的可用範圍說法也互相矛盾。投影片只寫「ChatGPT 只接遠端 HTTPS MCP」，不要寫選單路徑。
12. **OpenAI Evals repo 沒有封存**，但 README 第一行就導向 Dashboard 的 Evals，代表重心已移到平台。
13. 各 repo 的 release 日期如果頁面沒顯示年份，就標「推定」：Langflow 1.13.2（Nov 10）、Coze Studio v0.5.1（Feb）。有年份的是 Dify、n8n（GitHub API）和 RAGFlow（README）。
