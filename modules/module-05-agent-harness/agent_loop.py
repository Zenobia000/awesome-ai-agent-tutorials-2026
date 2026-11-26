"""02 本 notebook 手寫的 function calling 迴圈，整理成可以重用的版本。

    from agent_loop import Tool, run_agent

    tools = [Tool("read_logs", ot.read_logs, ot.ReadLogsArgs, "讀日誌")]
    answer, messages, stats = run_agent("下單 502", tools, system="你是值班助理")
"""

from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass

from openai import OpenAI
from pydantic import BaseModel, ValidationError

from course_utils.llm import make_client as _make_client
from course_utils.llm import primary_endpoint

_EP = primary_endpoint()  # 有 CLOUD_API_KEY 走雲端，否則本機 Ollama
MODEL = _EP.model


def make_client() -> OpenAI:
    return _make_client(_EP, timeout=120)


@dataclass(frozen=True)
class Tool:
    name: str
    fn: Callable[..., str]
    args_model: type[BaseModel]
    description: str

    def schema(self) -> dict:
        return {"type": "function", "function": {
            "name": self.name, "description": self.description,
            "parameters": self.args_model.model_json_schema()}}


def execute(tool_by_name: dict[str, Tool], name: str, arguments: str) -> str:
    """執行一個工具呼叫；未知工具、參數錯誤、工具例外都變成文字回給模型。"""
    tool = tool_by_name.get(name)
    if tool is None:
        return f"錯誤：沒有 {name} 這個工具"
    try:
        args = tool.args_model.model_validate_json(arguments or "{}")
    except ValidationError as exc:
        err = exc.errors()[0]
        return f"參數錯誤，請修正後重試：{err['loc']} {err['msg']}"
    try:
        return str(tool.fn(**args.model_dump()))
    except Exception as exc:  # 工具出錯也要讓模型看到
        return f"工具執行失敗：{type(exc).__name__}: {exc}"


def run_agent(question: str | list[dict], tools: list[Tool], system: str = "", max_steps: int = 6,
              client: OpenAI | None = None, verbose: bool = True, indent: str = ""
              ) -> tuple[str | None, list[dict], list[dict]]:
    """模型＋迴圈＝agent。回傳（答案或 None、完整 messages、每輪統計）。"""
    client = client or make_client()
    tool_by_name = {t.name: t for t in tools}
    if isinstance(question, str):
        messages = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": question}]
    else:
        messages = list(question)
    stats: list[dict] = []
    for step in range(1, max_steps + 1):
        t0 = time.time()
        kwargs = {"tools": [t.schema() for t in tools]} if tools else {}
        resp = client.chat.completions.create(model=MODEL, messages=messages, temperature=0, **kwargs)
        msg = resp.choices[0].message
        messages.append(msg.model_dump(exclude_none=True))
        calls = msg.tool_calls or []
        stats.append({"step": step, "prompt": resp.usage.prompt_tokens, "completion": resp.usage.completion_tokens,
                      "seconds": time.time() - t0, "tools": [c.function.name for c in calls]})
        if not calls:
            if verbose:
                print(f"{indent}── 第 {step} 輪：回答")
            return msg.content, messages, stats
        for call in calls:
            result = execute(tool_by_name, call.function.name, call.function.arguments)
            messages.append({"role": "tool", "tool_call_id": call.id, "content": result})
            if verbose:
                print(f"{indent}── 第 {step} 輪：{call.function.name}({call.function.arguments}) → {result[:80]!r}")
    return None, messages, stats
