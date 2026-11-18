"""回歸閘門的 pytest 版（Lab 8-02 Step 8）。

先在 8-02 跑出 runs/baseline.json 和候選版的結果，再：

    CANDIDATE=runs/prompt_v2.json uv run pytest -q test_regression.py

任何一條 assert 失敗，CI 就會擋下這次改動。
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

HERE = Path(__file__).parent
TOLERANCE = 0.025  # 40 題裡最多容許掉 1 題（judge 本身有雜訊）


def _load(path: str) -> list[dict]:
    p = HERE / path
    if not p.exists():
        pytest.skip(f"找不到 {p}，請先跑 08-02 notebook")
    return json.loads(p.read_text(encoding="utf-8"))["rows"]


def _pass_rate(rows: list[dict], tag: str | None = None) -> float:
    picked = [r for r in rows if tag is None or tag in r["tags"]]
    return sum(r["passed"] for r in picked) / len(picked)


@pytest.fixture(scope="module")
def baseline() -> list[dict]:
    return _load("runs/baseline.json")


@pytest.fixture(scope="module")
def candidate() -> list[dict]:
    return _load(os.getenv("CANDIDATE", "runs/candidate.json"))


def test_same_question_set(baseline, candidate):
    assert [r["id"] for r in baseline] == [r["id"] for r in candidate], "題庫不同，不能比"


def test_overall_pass_rate_not_worse(baseline, candidate):
    base, cand = _pass_rate(baseline), _pass_rate(candidate)
    assert cand >= base - TOLERANCE, f"整體通過率 {base:.0%} → {cand:.0%}"


def test_no_answer_questions_not_worse(baseline, candidate):
    """資料裡沒有的題目要回答「沒有提到」；這類題一題都不准退步。"""
    base, cand = _pass_rate(baseline, "無答案"), _pass_rate(candidate, "無答案")
    assert cand >= base, f"無答案題通過率 {base:.0%} → {cand:.0%}"
