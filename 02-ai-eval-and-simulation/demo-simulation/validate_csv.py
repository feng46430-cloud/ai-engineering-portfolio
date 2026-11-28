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


def main() -> None:
    sample_path = Path(__file__).with_name("sample_testcases.csv")
    assert sample_path.exists(), f"Checked-in fixture missing: {sample_path}"
    checked_in_bytes = sample_path.read_bytes()

    # 1. Positive gate check against existing checked-in read-only CSV fixture (no self-write!)
    errs = validate_csv_bytes(checked_in_bytes)
    assert not errs, f"Checked-in CSV fixture unexpectedly failed: {errs}"
    print(f"[PASS] Positive Gate: checked-in {sample_path.name} passed all 6 RFC-4180 & encoding checks.")

    # 2. Negative gate self-tests in memory (proving the validator catches real failure modes)
    no_bom = checked_in_bytes[3:]
    assert any("MISSING_BOM" in e for e in validate_csv_bytes(no_bom))

    dup_id = checked_in_bytes.decode("utf-8-sig").replace("TC-COMBAT-002", "TC-COMBAT-001").encode("utf-8-sig")
    assert any("DUPLICATE_ID" in e for e in validate_csv_bytes(dup_id))

    mojibake = (checked_in_bytes.decode("utf-8-sig") + "\ufffd").encode("utf-8-sig")
    assert any("MOJIBAKE_DETECTED" in e for e in validate_csv_bytes(mojibake))

    print("[PASS] Negative Self-Tests: MISSING_BOM, DUPLICATE_ID, and MOJIBAKE_DETECTED all caught.")


if __name__ == "__main__":
    main()
