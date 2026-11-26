"""課程共用的模型客戶端：雲端優先，失敗或沒填金鑰時切到本地 Ollama。

這個檔案就是 Lab 1-05 一步一步寫出來的成品，其他模組直接 import：

    from course_utils.llm import chat, stream, embed

要自己建 client（工具呼叫、LangChain、Agents SDK）時，用 primary_endpoint()
拿到這次該連的端點，就不用在每本 notebook 重複判斷雲端還是本地：

    from course_utils.llm import make_client, primary_endpoint

    ep = primary_endpoint()
    client = make_client(ep, timeout=300)
    client.chat.completions.create(model=ep.model, ...)
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


def local_endpoint() -> Endpoint:
    """本機 Ollama；一定存在，當作最後的備援。"""
    return Endpoint(
        name="local",
        base_url=os.getenv("LOCAL_BASE_URL", "http://localhost:11434/v1"),
        model=os.getenv("LOCAL_MODEL", "qwen2.5:3b"),
        api_key="ollama",  # Ollama 不檢查金鑰，但 SDK 要求非空字串
    )


def endpoints() -> list[Endpoint]:
    """依優先順序回傳端點：有雲端金鑰就雲端在前，本地永遠墊底。"""
    cloud_key = os.getenv("CLOUD_API_KEY", "")
    if not cloud_key:
        return [local_endpoint()]
    cloud = Endpoint(
        name="cloud",
        base_url=os.getenv("CLOUD_BASE_URL", "https://api.deepseek.com/v1"),
        model=os.getenv("CLOUD_MODEL", "deepseek-chat"),
        api_key=cloud_key,
    )
    return [cloud, local_endpoint()]


def primary_endpoint() -> Endpoint:
    """這次優先使用的端點：有金鑰就是雲端，否則是本地。"""
    return endpoints()[0]


def make_client(ep: Endpoint | None = None, timeout: float = 60, max_retries: int = 0) -> OpenAI:
    """替端點建一個 OpenAI SDK client；不給端點就用 primary_endpoint()。"""
    ep = ep or primary_endpoint()
    return OpenAI(base_url=ep.base_url, api_key=ep.api_key, timeout=timeout, max_retries=max_retries)


def chat(messages: Messages, temperature: float = 0.0, **kwargs) -> str:
    """送出一輪對話，回傳模型的文字。雲端失敗就換下一個端點。"""
    errors: list[str] = []
    for ep in endpoints():
        try:
            resp = make_client(ep).chat.completions.create(
                model=ep.model, messages=messages, temperature=temperature, **kwargs
            )
            return resp.choices[0].message.content or ""
        except OpenAIError as exc:
            errors.append(f"{ep.name}: {exc}")
    raise RuntimeError("所有端點都失敗：\n" + "\n".join(errors))


def stream(messages: Messages, temperature: float = 0.0) -> Iterator[str]:
    """串流版：一邊生成一邊 yield 文字片段。"""
    errors: list[str] = []
    for ep in endpoints():
        started = False
        try:
            chunks = make_client(ep).chat.completions.create(
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
    """把一批文字轉成向量；只走本地 embedding 模型（雲端聊天服務多半沒有 embedding）。"""
    resp = make_client(local_endpoint()).embeddings.create(
        model=os.getenv("EMBED_MODEL", "bge-m3"), input=texts
    )
    return [d.embedding for d in resp.data]
