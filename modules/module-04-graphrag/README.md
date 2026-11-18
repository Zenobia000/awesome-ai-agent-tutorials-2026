# 模組 4：GraphRAG

把海賊王劇情摘要抽成三元組、建成圖，先用 networkx 手寫多跳查詢，再換成 Neo4j 與 Cypher，
最後拿同一組題目跟向量檢索比一次。

| notebook | 做什麼 | 需要 |
|---|---|---|
| `01_extract_triples.ipynb` | LLM＋Pydantic 抽三元組，量 precision／recall，別名正規化、類型檢查、人工校對，存 `data/triples.json` | Ollama（`qwen2.5:3b`、`bge-m3`） |
| `02_graph_from_scratch.ipynb` | networkx 建圖、畫圖，手寫 BFS 多跳、超級節點剪枝，子圖轉文字交給 LLM 回答 | Ollama |
| `03_neo4j_cypher.ipynb` | MERGE 匯入 Neo4j、Cypher 多跳與 shortestPath、Text2Cypher（擋寫入、唯讀交易、錯誤回饋重試） | Docker 的 Neo4j；Ollama |
| `04_graph_vs_vector.ipynb` | 12 題同時考向量 RAG（bge-m3＋numpy）和圖檢索，分開量檢索命中與回答正確，討論何時用哪個 | Ollama |

## 準備

```bash
uv sync --group m4
cp .env.example .env
ollama pull qwen2.5:3b && ollama pull bge-m3

# 只有 03 需要：起一個 Neo4j 容器，並在 .env 加 NEO4J_PASSWORD=<同一個密碼>
docker run -d --name course-neo4j -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/<自己設一個密碼> neo4j:5

uv run jupyter lab modules/module-04-graphrag
```

notebook 從本資料夾開啟（讀的是相對路徑 `data/…`，04 會 import 同資料夾的 `graph_retrieval.py`）。

## 資料

| 檔案 | 內容 |
|---|---|
| `data/one_piece_summaries.md` | 課程自寫的 21 段人物與劇情摘要。同一人物刻意用不同稱呼（魯夫／蒙其·D·魯夫／草帽小子），事實刻意拆在不同段落 |
| `data/gold_triples.json` | 人工標註的 47 條標準三元組，用來量抽取品質，也代替人工校對 |
| `data/triples.json` | 01 的產出：節點（名字、類型、別名）＋三元組（`source` 標明是 LLM 抽到的或人工補的）。已附一份，可以直接從 02 開始 |
| `data/questions.json` | 04 用的 12 題（4 題單跳、8 題多跳）與答案關鍵字 |

圖譜 schema（投影片「Lab 4 圖譜長相」的擴充版）：

```
(:Person)-[:CAPTAIN_OF | MEMBER_OF]->(:Crew)
(:Person)-[:OWNS]->(:Treasure)
(:Person)-[:DREAMS_OF]->(:Dream)
(:Person)-[:FROM]->(:Place)
(:Person)-[:HAS_FATHER | BROTHER_OF | DEFEATED]->(:Person)
```

## 注意事項

- 語料是自寫摘要，練習時以本資料夾的內容為準，不是原作設定集。
- `qwen2.5:3b` 抽三元組的 precision 大約四到五成，方向反、關係標錯都很常見；01 就是要你看到這些錯。每次執行數字會有些不同。
- 03 會在 Neo4j 建唯一性約束並匯入節點；請用課程專用的容器，不要連到放其他資料的資料庫。
- 沒設 `NEO4J_PASSWORD` 時，03 會印「跳過」並略過所有讀寫資料庫的步驟，LLM 產生 Cypher 的部分照常執行。
- 04 的評分是「回答裡有沒有答案關鍵字」，很粗：模型把答案講錯但提到關鍵字也會算對。模組 8 會換成 LLM-as-a-judge。

## 已存的輸出

notebook 裡保留了一次執行結果。那次的 04：單跳題向量 4/4、圖 3/4（圖沒有「職位」關係）；
多跳題檢索命中向量 3/8、圖 8/8，回答正確向量 3/8、圖 7/8。
