# 模組 4：GraphRAG

原理（三元組、實體正規化、多跳、超級節點、Cypher、何時用圖）寫在 `00_concepts.md`；notebook 把海賊王劇情摘要抽成三元組、建成圖，
用 networkx 內建的走訪做多跳查詢，再換成 Neo4j 與 Cypher，最後拿同一組題目跟向量檢索比一次。

| notebook／檔案 | 做什麼 | 需要 |
|---|---|---|
| `00_concepts.md`（先讀） | 原理紀要：知識圖譜與三元組、實體正規化與命名陷阱、多跳與超級節點、Cypher、GraphRAG vs 向量 RAG 何時用、常見坑 | — |
| `01_extract_triples.ipynb` | LLM＋Pydantic 對 7 段子集抽三元組，量 precision／recall，別名正規化（含「人人果實」與「尼卡」不能合併的陷阱）、類型檢查；最後載入全量人工校對三元組，存 `data/triples.json` | Ollama（`qwen2.5:3b`、`bge-m3`） |
| `02_graph_networkx.ipynb` | networkx 建圖、畫圖，用 `ego_graph`、`shortest_path`、`bfs_layers` 做多跳，超級節點展開規則，子圖轉文字交給 LLM 回答 | Ollama |
| `03_neo4j_cypher.ipynb` | MERGE 匯入 Neo4j、Cypher 多跳與 shortestPath、Text2Cypher（擋寫入、唯讀交易、錯誤回饋重試） | Docker 的 Neo4j；Ollama |
| `04_graph_vs_vector.ipynb` | 14 題同時考向量 RAG（bge-m3＋Chroma）和圖檢索，分開量檢索命中與回答正確，討論何時用哪個 | Ollama；Chroma（m3 群組） |
| `graph_retrieval.py` | 02 的圖檢索函式（找實體、`bfs_layers` 走訪＋展開規則、子圖念成句子），給 04 import | `networkx` |

## 準備

```bash
uv sync --group m3 --group m4   # 04 用到 m3 群組的 Chroma
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
| `data/one_piece_summaries.md` | 課程自寫的 34 段人物與劇情摘要（約 3.2 萬 token）。同一人物刻意用不同稱呼（魯夫／蒙其·D·魯夫／草帽小子），事實刻意拆在不同段落；也埋了名字相近的陷阱（人人果實 vs 人人果實．幻獸種．模型「尼卡」、巨兵海賊團 vs 新巨兵海賊團、艾斯與薩波先後擁有燒燒果實） |
| `data/gold_triples.json` | 人工標註的 210 條標準三元組（8 種關係，每條記出處段落），用來量抽取品質，也代替人工校對 |
| `data/triples.json` | 01 的產出：187 個節點（名字、類型、別名）＋182 條三元組（標準答案套用別名表並去掉跨段重複）。`source` 標明來源：`llm`（子集內模型抽對的）、`manual`（子集內人工補的）、`reviewed`（子集外，模擬離線批次抽取＋人工校對）。已附一份，可以直接從 02 開始 |
| `data/questions.json` | 04 用的 14 題（4 題單跳、10 題多跳）與答案關鍵字；q13、q14 是第 34 段艾爾巴夫的題目 |

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
- 01 只對 7 段子集即時抽取（3B 模型抽全量 34 段太慢）；真實專案是離線批次抽取再人工校對，01 的最後一步用 `gold_triples.json` 模擬這個結果。
- `qwen2.5:3b` 抽三元組錯誤很多：方向反、關係標錯、長名字被截短；01 就是要你看到這些錯。每次執行數字會有些不同。
- schema 只有 8 種關係，有些細節被壓縮：波妮與大熊是養父女仍記成 `HAS_FATHER`、東利與布洛基是前代船長仍記成 `CAPTAIN_OF`（見 `00_concepts.md`「常見坑」）。
- `03` 已存的輸出是用舊版語料（21 段、47 條）跑的，重跑後數量會不同。
- 03 會在 Neo4j 建唯一性約束並匯入節點；請用課程專用的容器，不要連到放其他資料的資料庫。
- 沒設 `NEO4J_PASSWORD` 時，03 會印「跳過」並略過所有讀寫資料庫的步驟，LLM 產生 Cypher 的部分照常執行。
- 04 的評分是「回答裡有沒有答案關鍵字」，很粗：模型把答案講錯但提到關鍵字也會算對。模組 8 會換成 LLM-as-a-judge。

## 已存的輸出

notebook 裡保留了一次執行結果（03 除外，見上方注意事項）。那次的 01：7 段子集原始輸出 precision 20%、recall 27%，正規化後 25%／33%；
第 32 段把「人人果實．幻獸種．模型『尼卡』」拆成三樣寶物，正好踩中命名陷阱。
04：單跳題檢索命中向量 4/4、圖 3/4（圖沒有「職位」關係），回答正確向量 4/4、圖 3/4；
多跳題檢索命中向量 3/10、圖 10/10，回答正確向量 2/10、圖 6/10（其中 q11 是關鍵字評分誤判，q13 是 `BROTHER_OF` 被念成「結拜哥哥」誤導了模型）。
