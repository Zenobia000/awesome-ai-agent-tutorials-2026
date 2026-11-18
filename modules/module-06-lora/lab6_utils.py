"""Lab 6-01 寫過的小工具，收在這裡給 02、03 重用。

    from lab6_utils import load_jsonl, check_answer, generate_batch, ADAPTER_DIR
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import torch

MODEL = "Qwen/Qwen2.5-0.5B-Instruct"
ADAPTER_DIR = Path("/tmp/m6_lora_adapter")  # Lab 6-01 訓練完存在這裡

# 固定格式：兩行，第二行的指令用反引號包起來
ANSWER_RE = re.compile(r"^可能原因：[^\n]+\n第一步檢查：`([^`\n]+)`$")


def load_jsonl(path: str | Path) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def extract_command(text: str) -> str | None:
    """格式正確才取出指令；格式錯就回傳 None。"""
    m = ANSWER_RE.match(text.strip())
    return m.group(1) if m else None


def normalize_command(cmd: str) -> str:
    """比對指令前先去掉 sudo 與多餘空白，避免為了小差異扣分。"""
    cmd = re.sub(r"^sudo\s+", "", cmd.strip())
    return re.sub(r"\s+", " ", cmd)


def check_answer(output: str, expected: str) -> dict[str, bool]:
    """回傳兩個分數：格式對不對、指令跟標準答案一不一樣。"""
    got = extract_command(output)
    want = extract_command(expected)
    return {
        "format_ok": got is not None,
        "cmd_ok": got is not None and want is not None
        and normalize_command(got) == normalize_command(want),
    }


def generate_batch(model, tok, user_texts: list[str], system: str | None = None,
                   max_new_tokens: int = 80, batch_size: int = 10) -> list[str]:
    """greedy 生成；左側補齊才能一次生成一批。"""
    tok.padding_side = "left"
    outputs: list[str] = []
    for i in range(0, len(user_texts), batch_size):
        prompts = []
        for text in user_texts[i:i + batch_size]:
            msgs = ([{"role": "system", "content": system}] if system else []) + [
                {"role": "user", "content": text}]
            prompts.append(tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True))
        batch = tok(prompts, return_tensors="pt", padding=True).to(model.device)
        with torch.no_grad():
            out = model.generate(**batch, max_new_tokens=max_new_tokens, do_sample=False)
        new_tokens = out[:, batch.input_ids.shape[1]:]
        outputs += [t.strip() for t in tok.batch_decode(new_tokens, skip_special_tokens=True)]
    return outputs
