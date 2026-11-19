"""模組 3 共用的小工具：前幾本 notebook 做過的步驟，整理成函式給後面的 notebook 用。

    from rag_utils import load_docs, load_qa, chunk_docs, build_collection, ...

每個函式都很短，打開來讀就知道在做什麼；這裡沒有任何新觀念。
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from pathlib import Path

DATA = Path(__file__).parent / "data"
OLLAMA_URL = os.getenv("LOCAL_BASE_URL", "http://localhost:11434/v1").removesuffix("/v1")
EMBED_MODEL = os.getenv("EMBED_MODEL", "bge-m3")


# ---------- 讀資料 ----------

@dataclass(frozen=True)
class Doc:
    doc_id: str          # 檔名去掉 .md，例如 svc-tidepay
    title: str           # 第一行的 # 標題
    meta: dict           # 第二行 > 服務：…｜類型：… 解析出來的欄位，外加 status
    text: str            # 全文


@dataclass(frozen=True)
class Chunk:
    chunk_id: str        # 例如 svc-tidepay#3
    doc_id: str
    text: str
    meta: dict = field(default_factory=dict)


_META_KEYS = {"服務": "service", "類型": "type", "版本": "version", "負責團隊": "team", "更新": "updated"}


def _parse_meta(line: str) -> dict:
    meta = {}
    for part in line.lstrip("> ").split("｜"):
        key, _, value = part.partition("：")
        if key in _META_KEYS:
            meta[_META_KEYS[key]] = value.strip()
    return meta


def load_docs(folder: Path = DATA / "docs") -> list[Doc]:
    docs = []
    for path in sorted(folder.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        title = lines[0].lstrip("# ").strip()
        meta = _parse_meta(next((l for l in lines if l.startswith("> ")), ""))
        meta["status"] = "archived" if "已封存" in title else "current"
        docs.append(Doc(path.stem, title, meta, text))
    return docs


def load_qa(path: Path = DATA / "qa.jsonl") -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


# ---------- 分塊（Lab 3-03） ----------

def chunk_docs(docs: list[Doc], contextual: bool = True) -> list[Chunk]:
    """用 LlamaIndex 的 MarkdownNodeParser 依標題切；contextual=True 時每塊前面補上文件標題。"""
    from llama_index.core import Document
    from llama_index.core.node_parser import MarkdownNodeParser

    parser = MarkdownNodeParser()
    chunks = []
    for d in docs:
        nodes = parser.get_nodes_from_documents([Document(text=d.text, id_=d.doc_id)])
        for n, node in enumerate(nodes[1:]):  # 第 0 塊是標題與 metadata 行，跳過
            text = f"《{d.title}》\n{node.text}" if contextual else node.text
            section = node.text.splitlines()[0].lstrip("# ").strip()
            chunks.append(Chunk(f"{d.doc_id}#{n}", d.doc_id, text, {**d.meta, "section": section}))
    return chunks


# ---------- 向量庫（Lab 3-02） ----------

def build_collection(chunks: list[Chunk], name: str, batch: int = 32):
    """建一個 in-memory 的 Chroma collection（不寫進硬碟），embedding 交給 Ollama 的 bge-m3。"""
    import chromadb
    from chromadb.utils.embedding_functions import OllamaEmbeddingFunction

    client = chromadb.EphemeralClient()
    if name in [c.name for c in client.list_collections()]:
        client.delete_collection(name)
    col = client.create_collection(
        name,
        embedding_function=OllamaEmbeddingFunction(url=OLLAMA_URL, model_name=EMBED_MODEL, timeout=180),
        configuration={"hnsw": {"space": "cosine"}},
    )
    for i in range(0, len(chunks), batch):
        part = chunks[i:i + batch]
        col.add(ids=[c.chunk_id for c in part], documents=[c.text for c in part],
                metadatas=[{**c.meta, "doc_id": c.doc_id} for c in part])
    return col


def vector_search(col, query: str, k: int = 10, where: dict | None = None) -> list[str]:
    """回傳前 k 名的 chunk id。"""
    res = col.query(query_texts=[query], n_results=k, where=where)
    return res["ids"][0]


# ---------- BM25 與 RRF（Lab 3-04） ----------

_TOKEN_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.\-]*[A-Za-z0-9]|[A-Za-z0-9]|[一-鿿]+")


def tokenize(text: str) -> list[str]:
    """jieba 切中文；錯誤碼（TP-4021）、指令、版本號整個保留成一個 token。"""
    import jieba

    tokens = []
    for piece in _TOKEN_RE.findall(text):
        if re.match(r"[一-鿿]", piece):
            tokens.extend(t for t in jieba.lcut(piece) if t.strip())
        else:
            tokens.append(piece.lower())
    return tokens


class BM25Index:
    """rank_bm25 包一層：建索引時斷詞，查詢時回傳前 k 名的 chunk id。"""

    def __init__(self, chunks: list[Chunk]):
        from rank_bm25 import BM25Okapi

        self.ids = [c.chunk_id for c in chunks]
        self.bm25 = BM25Okapi([tokenize(c.text) for c in chunks])

    def search(self, query: str, k: int = 10, allowed: set[str] | None = None) -> list[str]:
        scores = self.bm25.get_scores(tokenize(query))
        order = sorted(range(len(scores)), key=lambda i: -scores[i])
        hits = [self.ids[i] for i in order if allowed is None or self.ids[i] in allowed]
        return hits[:k]


def rrf(rankings: list[list[str]], k: int = 60) -> list[str]:
    """Reciprocal Rank Fusion：每一路的第 r 名貢獻 1/(k+r)，加總後排序。"""
    scores: dict[str, float] = {}
    for ranking in rankings:
        for rank, cid in enumerate(ranking, start=1):
            scores[cid] = scores.get(cid, 0.0) + 1.0 / (k + rank)
    return sorted(scores, key=lambda c: -scores[c])


# ---------- 評估（Lab 3-06） ----------

def dedup_docs(chunk_ids: list[str]) -> list[str]:
    """把 chunk 排名轉成文件排名（同一份文件只算第一次出現）。"""
    seen, out = set(), []
    for cid in chunk_ids:
        d = cid.split("#")[0]
        if d not in seen:
            seen.add(d)
            out.append(d)
    return out


def hit_at_k(ranked_docs: list[str], gold: list[str], k: int) -> float:
    return float(any(d in gold for d in ranked_docs[:k]))


def reciprocal_rank(ranked_docs: list[str], gold: list[str]) -> float:
    for r, d in enumerate(ranked_docs, start=1):
        if d in gold:
            return 1.0 / r
    return 0.0


# ---------- LLM 呼叫（共用 Ollama 時比較耐操） ----------

def ask(messages: list[dict], tries: int = 3, timeout: float = 180, **kwargs) -> str:
    """course_utils.llm.chat 加上較長逾時與重試：Ollama 同時被很多人用時，單次請求偶爾會逾時。"""
    import time

    from course_utils.llm import chat

    for n in range(tries):
        try:
            return chat(messages, timeout=timeout, **kwargs)
        except RuntimeError as exc:
            if n == tries - 1:
                raise
            print(f"（第 {n + 1} 次呼叫失敗，5 秒後重試：{str(exc)[:50]}）")
            time.sleep(5)
    return ""
