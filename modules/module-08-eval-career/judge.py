"""Lab 8-01 的 judge 最終版：LLM 評審（參考答案＋評分量表＋範例＋結構化輸出）＋數字規則。

    from judge import judge
    v = judge(question, reference, answer)
    v["score"], v["numbers_ok"], v["passed"], v["reason"]

8-02 回歸評估、8-03 Langfuse、8-04 Opik、8-05 面試沙盤都用這一份。
"""

from __future__ import annotations

import re
import time

from pydantic import BaseModel, Field

from mini_rag import MODEL, client

PASS_SCORE = 4  # 4 分以上算通過

JUDGE_PROMPT = """你是評審，檢查內部助理的回答和參考答案的關鍵事實是否一致。

評分量表：
5 = 關鍵事實全對。簡短、換句話說、多寫了正確的補充，都算 5 分。
4 = 關鍵事實對，但漏了次要細節。
3 = 關鍵事實只對一半。
2 = 主要結論或數字錯。
1 = 完全答非所問，或編造參考答案沒有的內容。

規則：
- 只比對關鍵事實：數字、期限、單位、對象、可不可以。
- 回答的長短和語氣不影響分數。
- 參考答案是「資料中沒有提到」時：回答也說沒有資料 → 5 分；回答給出具體內容 → 1 分。

範例：
問題：補休要多久內用完？ 參考答案：6 個月內。 待評回答：半年內要用掉。
{"reason": "半年就是 6 個月，關鍵事實一致", "score": 5}
問題：P1 事故多久內要開單？ 參考答案：15 分鐘內在 #incident 開單。 待評回答：發生 P1 事故時，請依照公司事故管理流程，在 30 分鐘內通知值班工程師並開單，確保服務盡快恢復。
{"reason": "期限應為 15 分鐘，回答寫 30 分鐘，數字錯", "score": 2}

只輸出 JSON：{"reason": "一句話理由", "score": 1到5的整數}"""


class Verdict(BaseModel):
    reason: str
    score: int = Field(ge=1, le=5)


def numbers_in(text: str) -> set[str]:
    """抽出文字裡的數字（去掉千分位逗號），例如 "2,600 元、18:00" → {"2600", "18:00"}。"""
    return {n.replace(",", "") for n in re.findall(r"\d[\d,]*(?::\d+)?", text)}


def numbers_match(reference: str, answer: str) -> bool:
    """程式規則：參考答案裡的每個數字，回答都要出現。參考答案沒有數字就不檢查。"""
    return numbers_in(reference) <= numbers_in(answer)


def judge(question: str, reference: str, answer: str) -> dict:
    """LLM 評審 ≥ PASS_SCORE，而且數字規則通過，才算 pass。"""
    v = llm_judge(question, reference, answer)
    ok = numbers_match(reference, answer)
    return {**v, "numbers_ok": ok, "passed": v["score"] >= PASS_SCORE and ok}


def llm_judge(question: str, reference: str, answer: str, retries: int = 2) -> dict:
    """只有 LLM 的部分：回傳 score、reason、token 數與延遲。解析失敗就重試。"""
    user = f"問題：{question}\n參考答案：{reference}\n待評回答：{answer}"
    messages = [
        {"role": "system", "content": JUDGE_PROMPT},
        {"role": "user", "content": user},
    ]
    last_error = ""
    for _ in range(retries + 1):
        t0 = time.perf_counter()
        # 結構化輸出：直接把 Pydantic 模型交給 SDK，Ollama 會照 JSON Schema 產生
        resp = client().chat.completions.parse(
            model=MODEL, messages=messages, temperature=0, response_format=Verdict,
        )
        latency_ms = (time.perf_counter() - t0) * 1000
        v = resp.choices[0].message.parsed
        if v is None:
            last_error = (resp.choices[0].message.content or "")[:80]
            continue
        return {
            "score": v.score,
            "reason": v.reason,
            "prompt_tokens": resp.usage.prompt_tokens if resp.usage else 0,
            "completion_tokens": resp.usage.completion_tokens if resp.usage else 0,
            "latency_ms": latency_ms,
        }
    raise RuntimeError(f"judge 輸出連續 {retries + 1} 次不合格：{last_error}")
