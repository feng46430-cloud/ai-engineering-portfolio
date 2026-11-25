#!/usr/bin/env python3
"""
Gate-5 Deterministic CSV & Encoding Validator Demo (RFC-4180 + UTF-8 BOM)
-------------------------------------------------------------------------
Demonstrates the deterministic output gate from the 5-Gate AI QA Testcase SOP:
  1. UTF-8 with BOM presence (prevents Excel/Feishu Chinese mojibake on Windows)
  2. Strict RFC-4180 parsing & uniform column count per row
  3. Zero duplicate testcase IDs
  4. Zero empty required execution columns
  5. Zero U+FFFD replacement characters
  6. Valid QA Test Gym station anchor naming (`TP_QA_* | QA_*`)

Zero external dependencies. Run directly with:
    python 02-ai-eval-and-simulation/demo-simulation/validate_csv.py
"""

import csv
import io
import re
from pathlib import Path
from typing import List

REQUIRED_HEADERS = [
    "用例ID",
    "所属模块",
    "测试维度",
    "用例标题",
    "现网去哪测（前置）",
    "操作步骤",
    "预期结果",
    "测试场站点映射",
    "排查参考（提单定责用）",
]

REQUIRED_NON_EMPTY = ["用例ID", "所属模块", "用例标题", "操作步骤", "预期结果"]
STATION_RE = re.compile(r"^TP_QA_[A-Za-z0-9_]+\s*\|\s*QA_[A-Za-z0-9_]+$")


def validate_csv_bytes(raw: bytes) -> List[str]:
    errors: List[str] = []

    if not raw.startswith(b"\xef\xbb\xbf"):
        errors.append("MISSING_BOM: File must be encoded as UTF-8 with BOM (0xEF 0xBB 0xBF).")

    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        return [f"DECODE_ERROR: Invalid UTF-8 bytes ({exc})."]

    if "\ufffd" in text:
        errors.append("MOJIBAKE_DETECTED: Found Unicode replacement character U+FFFD.")

    reader = csv.reader(io.StringIO(text, newline=""))
    rows = list(reader)
    if len(rows) < 2:
        return errors + ["EMPTY_SUITE: CSV must contain a header row and at least 1 testcase row."]

    header = rows[0]
    if header != REQUIRED_HEADERS:
        errors.append(f"HEADER_MISMATCH: Expected {REQUIRED_HEADERS}, got {header}.")
        return errors

    expected_cols = len(header)
    seen_ids = set()

    for line_no, row in enumerate(rows[1:], start=2):
        if len(row) != expected_cols:
            errors.append(f"ROW_{line_no}_COL_COUNT: Expected {expected_cols} columns, got {len(row)}.")
            continue

        record = dict(zip(header, row))
        tc_id = record["用例ID"].strip()
        if tc_id in seen_ids:
            errors.append(f"ROW_{line_no}_DUPLICATE_ID: Duplicate testcase ID '{tc_id}'.")
        else:
            seen_ids.add(tc_id)

        for col in REQUIRED_NON_EMPTY:
            if not record[col].strip():
                errors.append(f"ROW_{line_no}_EMPTY_FIELD: Required column '{col}' is empty.")

        station = record["测试场站点映射"].strip()
        if station and not STATION_RE.match(station):
            errors.append(f"ROW_{line_no}_BAD_STATION: Invalid Test Gym anchor '{station}'.")

    return errors


def build_clean_sample_bytes() -> bytes:
    buf = io.StringIO(newline="")
    writer = csv.writer(buf, lineterminator="\r\n")
    writer.writerow(REQUIRED_HEADERS)
    writer.writerows(
        [
            [
                "TC-COMBAT-001",
                "战斗交互",
                "核心主路径",
                "格挡状态下受轻击触发弹反并返还耐力",
                "进入测试场战斗区，角色满耐力并装备近战武器",
                "1. 在敌方前摇窗口按下格挡键\n2. 观察受击反馈与耐力条变化",
                "角色触发弹反硬直反制，耐力返还且无额外扣血",
                "TP_QA_Combat | QA_Combat_Parry",
                "RPC_CombatParry / CVar combat.parryWindowMs / LogTag:[CombatParry]",
            ],
            [
                "TC-COMBAT-002",
                "战斗交互",
                "异常与打断",
                "弱网断线重连后状态机不残留永久霸体标记",
                "在测试场触发霸体技能后立即模拟断网 5 秒并恢复",
                "1. 释放带霸体前摇的技能\n2. 断网 5 秒后重连\n3. 让普通怪物攻击角色",
                "重连后霸体状态正确过期，受击正常产生硬直，无状态残留",
                "TP_QA_Combat | QA_Combat_StateSync",
                "StateFlag.SuperArmor / ReconcileTick / LogTag:[NetStateSync]",
            ],
            [
                "TC-INV-003",
                "背包与持久化",
                "边界与数值",
                "堆叠上限 999 时再拾取 1 个物品自动拆格且不丢件",
                "角色背包第 1 格持有 999 个可堆叠消耗品，第 2 格为空",
                "1. 拾取同 ID 消耗品 1 个\n2. 退出重登后检查背包",
                "第 1 格保持 999，第 2 格新增 1 个；重登后数量一致",
                "TP_QA_Inventory | QA_Inv_StackCap",
                "Cfg.MaxStack=999 / SaveChunk.Inventory / LogTag:[InvPersist]",
            ],
        ]
    )
    return buf.getvalue().encode("utf-8-sig")


def main() -> None:
    sample_path = Path(__file__).with_name("sample_testcases.csv")
    clean_bytes = build_clean_sample_bytes()
    sample_path.write_bytes(clean_bytes)

    # 1. Positive gate check
    errs = validate_csv_bytes(sample_path.read_bytes())
    assert not errs, f"Clean sample unexpectedly failed: {errs}"
    print(f"[PASS] Positive Gate: {sample_path.name} passed all 6 RFC-4180 & encoding checks (3 cases).")

    # 2. Negative gate self-tests (proving the validator catches real failure modes)
    no_bom = clean_bytes[3:]
    assert any("MISSING_BOM" in e for e in validate_csv_bytes(no_bom))

    dup_id = clean_bytes.decode("utf-8-sig").replace("TC-COMBAT-002", "TC-COMBAT-001").encode("utf-8-sig")
    assert any("DUPLICATE_ID" in e for e in validate_csv_bytes(dup_id))

    mojibake = (clean_bytes.decode("utf-8-sig") + "\ufffd").encode("utf-8-sig")
    assert any("MOJIBAKE_DETECTED" in e for e in validate_csv_bytes(mojibake))

    print("[PASS] Negative Self-Tests: MISSING_BOM, DUPLICATE_ID, and MOJIBAKE_DETECTED all caught.")


if __name__ == "__main__":
    main()
