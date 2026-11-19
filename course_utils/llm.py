"""課程共用的模型客戶端：本地 Ollama 優先，失敗時切到雲端。

這個檔案就是 Lab 1-05 一步一步寫出來的成品，其他模組直接 import：

    from course_utils.llm import chat, stream, embed
"""

from __future__ import annotations

import os
from collections.abc import Iterator
from dataclasses import dataclass

from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

load_dotenv()

Messages = list[dict[str, str]]


@dataclass(frozen=True)
class Endpoint:
    name: str
    base_url: str
    model: str
    api_key: str


def _endpoints() -> list[Endpoint]:
    """依序回傳可用端點：本地一定有，雲端要有金鑰才加。"""
    local = Endpoint(
        name="local",
        base_url=os.getenv("LOCAL_BASE_URL", "http://localhost:11434/v1"),
        model=os.getenv("LOCAL_MODEL", "qwen2.5:3b"),
        api_key="ollama",  # Ollama 不檢查金鑰，但 SDK 要求非空字串
    )
    cloud_key = os.getenv("CLOUD_API_KEY", "")
    if not cloud_key:
        return [local]
    cloud = Endpoint(
        name="cloud",
        base_url=os.getenv("CLOUD_BASE_URL", "https://api.deepseek.com/v1"),
        model=os.getenv("CLOUD_MODEL", "deepseek-chat"),
        api_key=cloud_key,
    )
    return [local, cloud]


def _client(ep: Endpoint) -> OpenAI:
    return OpenAI(base_url=ep.base_url, api_key=ep.api_key, timeout=60, max_retries=0)


def chat(messages: Messages, temperature: float = 0.0, **kwargs) -> str:
    """送出一輪對話，回傳模型的文字。本地失敗就換下一個端點。"""
    errors: list[str] = []
    for ep in _endpoints():
        try:
            resp = _client(ep).chat.completions.create(
                model=ep.model, messages=messages, temperature=temperature, **kwargs
            )
            return resp.choices[0].message.content or ""
        except OpenAIError as exc:
            errors.append(f"{ep.name}: {exc}")
    raise RuntimeError("所有端點都失敗：\n" + "\n".join(errors))


def stream(messages: Messages, temperature: float = 0.0) -> Iterator[str]:
    """串流版：一邊生成一邊 yield 文字片段。"""
    errors: list[str] = []
    for ep in _endpoints():
        started = False
        try:
            chunks = _client(ep).chat.completions.create(
                model=ep.model, messages=messages, temperature=temperature, stream=True
            )
            for chunk in chunks:
                if chunk.choices and chunk.choices[0].delta.content:
                    started = True
                    yield chunk.choices[0].delta.content
            return
        except OpenAIError as exc:
            if started:  # 已經吐出字了，不能再換端點
                raise
            errors.append(f"{ep.name}: {exc}")
    raise RuntimeError("所有端點都失敗：\n" + "\n".join(errors))


def embed(texts: list[str]) -> list[list[float]]:
    """把一批文字轉成向量；只走本地 embedding 模型。"""
    ep = _endpoints()[0]
    resp = _client(ep).embeddings.create(
        model=os.getenv("EMBED_MODEL", "bge-m3"), input=texts
    )
    return [d.embedding for d in resp.data]
