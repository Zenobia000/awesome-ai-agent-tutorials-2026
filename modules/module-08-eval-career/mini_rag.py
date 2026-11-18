"""模組 8 的受測系統：bge-m3 ＋ numpy 的最小 RAG。

模組 3 已經一步一步手寫過 RAG；這裡把它縮成一個檔案，當作「要被評估的系統」。
模組之間不互相 import，所以這份是獨立的：

    from mini_rag import MiniRAG, load_faq, load_eval_set
    rag = MiniRAG(load_faq())
    result = rag.answer("特休要提前幾天申請？", top_k=3, prompt="v1")
"""

from __future__ import annotations

import json
import os
import time
from pathlib import Path

import numpy as np
from openai import OpenAI

from course_utils.llm import embed

DATA = Path(__file__).parent / "data"
MODEL = os.getenv("LOCAL_MODEL", "qwen2.5:3b")

# 兩個 prompt 版本：v1 是基準，v2 是「看起來更親切」的改版（模組 8-02 用來示範回歸）
PROMPTS = {
    "v1": (
        "你是山嵐雲端的內部助理。只根據下面的「資料」回答同仁的問題，"
        "用一到兩句繁體中文直接回答。資料裡沒有的內容，就回答「資料中沒有提到」，不要猜。"
    ),
    "v2": (
        "你是山嵐雲端熱情又貼心的內部助理。請盡量完整、詳細地幫同仁解答問題，"
        "可以補充你知道的一般公司慣例，讓同仁覺得被照顧。用繁體中文回答。"
    ),
}


def _read_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def load_faq() -> list[dict]:
    """20 份虛構公司 FAQ：id、title、text。"""
    return _read_jsonl(DATA / "faq.jsonl")


def load_eval_set() -> list[dict]:
    """40 題評估集：id、question、reference、doc_id、tags。"""
    return _read_jsonl(DATA / "eval_set.jsonl")


def client() -> OpenAI:
    base_url = os.getenv("LOCAL_BASE_URL", "http://localhost:11434/v1")
    return OpenAI(base_url=base_url, api_key="ollama", timeout=300, max_retries=2)


class MiniRAG:
    """檢索用 cosine similarity，生成用本地 qwen2.5:3b。"""

    def __init__(self, docs: list[dict]):
        self.docs = docs
        vecs = np.array(embed([f"{d['title']}：{d['text']}" for d in docs]))
        self.matrix = vecs / np.linalg.norm(vecs, axis=1, keepdims=True)

    def retrieve(self, question: str, top_k: int = 3) -> list[dict]:
        """回傳最相近的 top_k 份文件，附上分數。"""
        q = np.array(embed([question])[0])
        scores = self.matrix @ (q / np.linalg.norm(q))
        order = np.argsort(-scores)[:top_k]
        return [{**self.docs[i], "score": float(scores[i])} for i in order]

    def generate(self, question: str, hits: list[dict], prompt: str = "v1") -> dict:
        """把檢索結果塞進 prompt 讓模型回答；回傳答案、token 數與延遲。"""
        context = "\n".join(f"[{h['id']}] {h['title']}：{h['text']}" for h in hits)
        messages = [
            {"role": "system", "content": PROMPTS[prompt]},
            {"role": "user", "content": f"資料：\n{context}\n\n問題：{question}"},
        ]
        t0 = time.perf_counter()
        resp = client().chat.completions.create(model=MODEL, messages=messages, temperature=0)
        latency_ms = (time.perf_counter() - t0) * 1000
        return {
            "answer": (resp.choices[0].message.content or "").strip(),
            "prompt_tokens": resp.usage.prompt_tokens if resp.usage else 0,
            "completion_tokens": resp.usage.completion_tokens if resp.usage else 0,
            "latency_ms": latency_ms,
        }

    def answer(self, question: str, top_k: int = 3, prompt: str = "v1") -> dict:
        hits = self.retrieve(question, top_k)
        out = self.generate(question, hits, prompt)
        return {**out, "retrieved": [h["id"] for h in hits]}
