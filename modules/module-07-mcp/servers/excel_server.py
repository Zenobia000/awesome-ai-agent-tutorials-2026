"""Lab 7 的 Excel 分析 MCP Server：讓模型「看得到、算得到、畫得出」，但改不到檔案。

四個工具：list_sheets、describe、query、make_chart。全部唯讀：
- 只能讀 data/ 資料夾裡的 .xlsx（白名單路徑，擋掉 ../ 之類的路徑穿越）
- query 不接受任意 pandas 程式碼，只接受結構化參數（分組欄、彙總方式、篩選條件）
- 回傳列數有上限，避免一次把整張表塞進模型的 context
- make_chart 只寫進 outputs/charts/，不碰原始檔

啟動（通常由 Host 代勞）：

    uv run python modules/module-07-mcp/servers/excel_server.py

stdio Server 不能 print()；除錯訊息用 logging（寫 stderr）。
"""

from __future__ import annotations

import json
import logging
import re
import sys
from contextlib import redirect_stdout
from functools import lru_cache
from pathlib import Path
from typing import Annotated, Literal

import matplotlib

matplotlib.use("Agg")  # 伺服器沒有螢幕，只存檔
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.ticker import FuncFormatter  # noqa: E402
from mcp.server.fastmcp import FastMCP  # noqa: E402
from mcp.types import ToolAnnotations  # noqa: E402
from pydantic import Field  # noqa: E402

from course_utils.viz import setup_cjk  # noqa: E402

logging.basicConfig(level=logging.INFO, format="[excel-server] %(message)s")
log = logging.getLogger(__name__)

MODULE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = MODULE_DIR / "data"
CHART_DIR = MODULE_DIR / "outputs" / "charts"
MAX_ROWS = 20

mcp = FastMCP("excel-analyst", instructions="唯讀的 Excel 分析工具：列工作表、看欄位、彙總查詢、畫圖。")
logging.getLogger("mcp").setLevel(logging.WARNING)
READ_ONLY = ToolAnnotations(readOnlyHint=True, openWorldHint=False)

FileName = Annotated[str, Field(description="data/ 資料夾裡的檔名，例如 sales.xlsx")]
Agg = Annotated[
    Literal["sum", "mean", "count", "max", "min"],
    Field(description="sum＝總和（問「總共」「最多」「最好」用這個）、mean＝平均、count＝筆數、max／min＝單筆最大／最小"),
]


# ---------- 安全邊界：只讀白名單資料夾裡的 .xlsx ----------
def _safe_path(file: str) -> Path:
    path = (DATA_DIR / file).resolve()
    if not path.is_relative_to(DATA_DIR) or path.suffix != ".xlsx":
        raise ValueError(f"不允許讀取 {file!r}：只能讀 data/ 裡的 .xlsx 檔")
    if not path.exists():
        available = sorted(p.name for p in DATA_DIR.glob("*.xlsx"))
        raise ValueError(f"找不到 {file!r}，可用的檔案：{available}")
    return path


@lru_cache(maxsize=8)
def _read_book(path: Path, mtime: float) -> dict[str, pd.DataFrame]:
    """整本讀進記憶體；mtime 變了才重讀。"""
    log.info("讀取 %s", path.name)
    return pd.read_excel(path, sheet_name=None)


def _sheet(file: str, sheet: str) -> pd.DataFrame:
    path = _safe_path(file)
    book = _read_book(path, path.stat().st_mtime)
    if sheet not in book:
        raise ValueError(f"沒有工作表 {sheet!r}，可用的工作表：{list(book)}")
    return book[sheet]


def _check_columns(df: pd.DataFrame, *cols: str | None) -> None:
    for col in cols:
        if col is not None and col not in df.columns:
            raise ValueError(f"沒有欄位 {col!r}，可用的欄位：{list(df.columns)}")


def _filter(df: pd.DataFrame, where_column: str | None, where_value: str | None) -> pd.DataFrame:
    if where_column is None or where_value is None:
        return df
    _check_columns(df, where_column)
    return df[df[where_column].astype(str) == str(where_value)]


def _aggregate(df: pd.DataFrame, group_by: str, value_column: str, agg: str) -> pd.Series:
    _check_columns(df, group_by, value_column)
    if agg != "count" and not pd.api.types.is_numeric_dtype(df[value_column]):
        raise ValueError(f"欄位 {value_column!r} 不是數字，不能做 {agg}")
    return df.groupby(group_by)[value_column].agg(agg)


# ---------- 工具 ----------
@mcp.tool(annotations=READ_ONLY)
def list_sheets(file: FileName = "sales.xlsx") -> str:
    """列出 Excel 檔裡的所有工作表與各自的列數。"""
    path = _safe_path(file)
    book = _read_book(path, path.stat().st_mtime)
    return json.dumps({name: len(df) for name, df in book.items()}, ensure_ascii=False)


@mcp.tool(annotations=READ_ONLY)
def describe(sheet: str, file: FileName = "sales.xlsx") -> str:
    """看一張工作表的結構：欄位名稱、型別、前 3 列範例。分析前先呼叫這個。"""
    df = _sheet(file, sheet)
    cols = {c: str(t) for c, t in df.dtypes.items()}
    head = df.head(3).astype(str).to_dict(orient="records")
    return json.dumps({"rows": len(df), "columns": cols, "head": head}, ensure_ascii=False)


@mcp.tool(annotations=READ_ONLY)
def query(
    sheet: str,
    group_by: Annotated[str | None, Field(description="依哪個欄位分組，例如 區域、產品、月份；不填＝整張表算一個數")] = None,
    value_column: Annotated[str, Field(description="要彙總的數字欄位，例如 金額、數量")] = "金額",
    agg: Agg = "sum",
    where_column: Annotated[str | None, Field(description="篩選欄位（選填），例如 區域")] = None,
    where_value: Annotated[str | None, Field(description="篩選值（選填），例如 北區")] = None,
    limit: Annotated[int, Field(ge=1, le=MAX_ROWS, description=f"最多回傳幾列，上限 {MAX_ROWS}")] = 10,
    file: FileName = "sales.xlsx",
) -> str:
    """彙總查詢（唯讀）：先依 where 篩選，再依 group_by 分組，對 value_column 做 agg，由大到小排序。
    問「總共幾筆」就不填 group_by、agg 用 count。"""
    log.info("query(%s, %s, %s, %s, %s=%s)", sheet, group_by, value_column, agg, where_column, where_value)
    df = _filter(_sheet(file, sheet), where_column, where_value)
    if group_by is None:  # 不分組：整張表（篩選後）算一個數
        _check_columns(df, value_column)
        value = df[value_column].agg(agg)
        return json.dumps({f"{value_column}_{agg}": f"{value:,.0f}", "rows_used": len(df)}, ensure_ascii=False)
    result = _aggregate(df, group_by, value_column, agg).sort_values(ascending=False)
    total = len(result)
    result = result.head(limit).round(1)
    # 數字先排好千分位：小模型自己加逗號常常加錯
    rows = [{group_by: k, f"{value_column}_{agg}": f"{v:,.0f}" if abs(v) >= 1000 else v} for k, v in result.items()]
    return json.dumps({"rows": rows, "shown": len(rows), "total_groups": total}, ensure_ascii=False)


@mcp.tool(annotations=READ_ONLY)
def make_chart(
    sheet: str,
    x: Annotated[str, Field(description="橫軸：分組欄位，例如 月份、區域")],
    y: Annotated[str, Field(description="縱軸：要彙總的數字欄位，例如 金額")],
    kind: Literal["bar", "line"] = "bar",
    agg: Agg = "sum",
    where_column: str | None = None,
    where_value: str | None = None,
    title: str = "",
    file: FileName = "sales.xlsx",
) -> str:
    """畫圖並存成 PNG（不改原始檔）。line 適合時間趨勢（x 用 月份），bar 適合類別比較。回傳圖檔路徑、最大值與每個點的數字。"""
    log.info("make_chart(%s, %s, %s, %s)", sheet, x, y, kind)
    df = _filter(_sheet(file, sheet), where_column, where_value)
    series = _aggregate(df, x, y, agg)
    series = series.sort_index() if kind == "line" else series.sort_values(ascending=False)

    with redirect_stdout(sys.stderr):  # setup_cjk 找不到字型會 print，不能讓它碰到 stdout
        setup_cjk()
    fig, ax = plt.subplots(figsize=(8, 4))
    style = {"marker": "o"} if kind == "line" else {}
    series.plot(kind=kind, ax=ax, color="#3b5b92", **style)
    ax.set_title(title or f"{y}（{agg}）依 {x}")
    ax.set_xlabel(x)
    ax.set_ylabel(f"{y}（{agg}）")
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:,.0f}"))
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()

    CHART_DIR.mkdir(parents=True, exist_ok=True)
    name = re.sub(r"[^\w]+", "_", f"{sheet}_{x}_{y}_{kind}_{where_value or 'all'}") + ".png"
    out = CHART_DIR / name
    fig.savefig(out, dpi=110)
    plt.close(fig)
    top = series.idxmax()
    data = {str(k): f"{v:,.0f}" for k, v in series.items()}
    # 回傳相對於模組資料夾的路徑（不洩漏本機的家目錄）
    return json.dumps({"chart": str(out.relative_to(MODULE_DIR)), "max": {x: str(top), y: f"{series[top]:,.0f}"}, "data": data},
                      ensure_ascii=False)


@mcp.resource("excel://schema", name="schema", description="data/ 裡每個 Excel 檔的工作表、欄位與類別欄位的可能值", mime_type="text/markdown")
def schema() -> str:
    """給應用程式讀的資料地圖：放進 system prompt，模型就不用猜工作表和欄位名稱。"""
    lines = []
    for path in sorted(DATA_DIR.glob("*.xlsx")):
        lines.append(f"# 檔案 {path.name}")
        for name, df in _read_book(path, path.stat().st_mtime).items():
            lines.append(f"## 工作表「{name}」（{len(df)} 列）")
            for col in df.columns:
                values = df[col].dropna().unique()
                hint = f"，可能值：{'、'.join(map(str, values[:8]))}" if df[col].dtype == object and len(values) <= 8 else ""
                lines.append(f"- {col}（{df[col].dtype}{hint}）")
    return "\n".join(lines)


if __name__ == "__main__":
    mcp.run(transport="stdio")
