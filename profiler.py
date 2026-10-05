"""data-profiler-lite — 数据画像。

对 CSV 做类型推断、缺失率、唯一值数、数值分布、top 频次。零第三方依赖。
"""
from __future__ import annotations

import csv
import io
from collections import Counter


def _infer_type(values: list[str]) -> str:
    non_empty = [v for v in values if v != ""]
    if not non_empty:
        return "empty"
    for v in non_empty:
        try:
            float(v)
        except ValueError:
            return "string"
    return "number"


def _mean(vals: list[float]) -> float:
    return sum(vals) / len(vals) if vals else 0.0


def profile_csv(text: str) -> dict:
    reader = csv.reader(io.StringIO(text))
    rows = list(reader)
    if not rows:
        return {"columns": [], "row_count": 0}
    header = rows[0]
    data = rows[1:]
    cols: dict[str, list[str]] = {h: [] for h in header}
    for r in data:
        for i, h in enumerate(header):
            cols[h].append(r[i] if i < len(r) else "")

    out_cols = []
    for h in header:
        vals = cols[h]
        n = len(vals)
        missing = sum(1 for v in vals if v.strip() == "")
        ctype = _infer_type(vals)
        non_empty = [v for v in vals if v != ""]
        unique = len(set(non_empty))
        col = {"name": h, "type": ctype, "missing": missing,
               "missing_rate": round(missing / n, 3) if n else 0.0,
               "unique": unique,
               "top": Counter(non_empty).most_common(3)}
        if ctype == "number":
            nums = [float(v) for v in non_empty]
            col["min"] = min(nums)
            col["max"] = max(nums)
            col["mean"] = round(_mean(nums), 2)
        out_cols.append(col)
    return {"row_count": len(data), "columns": out_cols}


def report(text: str) -> str:
    p = profile_csv(text)
    lines = [f"=== 数据画像（{p['row_count']} 行）==="]
    for c in p["columns"]:
        lines.append(f"- {c['name']}（{c['type']}）：缺失 {c['missing']}({c['missing_rate']*100:.0f}%)，"
                     f"唯一值 {c['unique']}")
        if "mean" in c:
            lines.append(f"    数值：min={c['min']} max={c['max']} mean={c['mean']}")
        top = "，".join(f"{k}×{v}" for k, v in c["top"])
        if top:
            lines.append(f"    top：{top}")
    return "\n".join(lines)
