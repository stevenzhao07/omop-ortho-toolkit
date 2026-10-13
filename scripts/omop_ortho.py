#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
omop_ortho.py — 骨科登记 → OMOP CDM 概念集映射（提案）
==========================================================
把骨科术式/植入物（源代码 CPT）映射到 OMOP vocabulary，
产出概念集 SQL 骨架。诚实标注两点：
  1) OMOP CDM v5.4（已一手核实 DDL，39 表）**没有** concept_set /
     concept_set_item 标准表——概念集（concept set）由 OHDSI WebAPI/Atlas
     应用层维护（注意：CDM 的 cohort 是**患者集合**，不是概念集）；
     本脚本输出面向**本地 ETL 辅助表**（concept_set_ortho /
     concept_set_item_ortho，两表拆分约定）。
  2) OMOP standard concept_id 以 (?) 占位，须以本地 vocabulary 复核。
CPT 描述已按 AMA CPT 官方措辞核实（2026-10-12）：27438=髌骨关节成形
（置假体），**不是**翻修代码；TKA 翻修=27486（单组件）/27487（股骨+
整个胫骨组件）；29862=**髋**关节镜手术，膝关节镜诊断=29870。
投 OHDSI CDM WG。零依赖（仅 Python 3.8+ 标准库）。
"""
from __future__ import annotations
import os
import sys
import argparse

# 源代码 -> (名称, 源 vocabulary, 建议 OMOP concept_id 占位)
# 注意：concept_id 以 (?) 占位，须以本地 OMOP vocabulary 复核，避免误导。
# CPT 标签经 web 一手核实（2026-10-12，ama-assn.org / CPT 官方描述）：
#   27447 TKA / 27130 THA / 27134 Revision THA
#   27438 = Arthroplasty, patella; with prosthesis（**髌骨**关节成形·置假体，
#           非髌股关节成形 PFJ——合并髌股病例应报未列码 27599，非 27438）
#   27486 = Revision of TKA, 1 component（单组件翻修）
#   27487 = Revision of TKA, femoral and entire tibial component（股骨+整个胫骨）
#   29870 = Arthroscopy, knee, diagnostic（膝关节镜诊断，±滑膜活检）
#   29862 = Arthroscopy, hip, surgical（髋关节镜手术：软骨成形/磨削/唇盂切除）
PROCEDURE_MAP = {
    "27447": ("Total knee arthroplasty (TKA)", "CPT4", "TO_BE_VALIDATED"),
    "27130": ("Total hip arthroplasty (THA)", "CPT4", "TO_BE_VALIDATED"),
    "27438": ("Patellar arthroplasty with prosthesis (patellar resurfacing)", "CPT4", "TO_BE_VALIDATED"),
    "27486": ("Revision TKA (1 component)", "CPT4", "TO_BE_VALIDATED"),
    "27487": ("Revision TKA (femoral + entire tibial component)", "CPT4", "TO_BE_VALIDATED"),
    "27134": ("Revision THA", "CPT4", "TO_BE_VALIDATED"),
    "29870": ("Diagnostic knee arthroscopy", "CPT4", "TO_BE_VALIDATED"),
    "29862": ("Arthroscopy, hip, surgical (chondroplasty/abrasion/labrum resection)", "CPT4", "TO_BE_VALIDATED"),
}

CONCEPT_SET_TABLE = "concept_set_ortho"
CONCEPT_SET_ITEM_TABLE = "concept_set_item_ortho"


def emit_sql() -> str:
    lines = [
        f"-- 骨科概念集（提案）：本地 ETL 辅助表 {CONCEPT_SET_TABLE} / {CONCEPT_SET_ITEM_TABLE}",
        "-- 已一手核实（2026-10-12，OHDSI CommonDataModel v5.4 DDL，共 39 表）：",
        "-- OMOP CDM v5.4 无 concept_set / concept_set_item 标准表；概念集由 OHDSI",
        "-- WebAPI/Atlas 应用层维护（CDM 的 cohort 是患者集合，非概念集）。下表为",
        "-- 本仓库自定义的两表拆分约定（非 CDM 标准表），仅供本地 ETL 暂存；",
        "-- concept_id 须以本地 OMOP vocabulary 复核后再填。",
        f"CREATE TABLE @target_database_schema.{CONCEPT_SET_TABLE} (concept_set_id INT, concept_set_name VARCHAR);",
        f"CREATE TABLE @target_database_schema.{CONCEPT_SET_ITEM_TABLE} (concept_set_id INT, concept_id INT);",
        f"INSERT INTO @target_database_schema.{CONCEPT_SET_TABLE} (concept_set_id, concept_set_name)",
        "VALUES (1, 'ortho_procedures_v1');",
        f"INSERT INTO @target_database_schema.{CONCEPT_SET_ITEM_TABLE} (concept_set_id, concept_id)",
        "VALUES",
    ]
    rows = []
    for code, (name, vocab, cid) in PROCEDURE_MAP.items():
        rows.append(f"  (1, {cid})  -- TODO: validate {cid} [{vocab}:{code} {name}]")
    return ",\n".join(lines + rows) + ";" + "\n"


def _demo() -> int:
    print("源代码 | 名称 | vocabulary | OMOP concept_id(待校验)")
    for code, (name, vocab, cid) in PROCEDURE_MAP.items():
        print(f"  {code} | {name} | {vocab} | {cid}")
    print("\n[demo] 概念集 SQL 骨架: python scripts/omop_ortho.py --emit-sql --out ortho_concept_set.sql")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="骨科 → OMOP 概念集映射")
    ap.add_argument("--demo", action="store_true", help="列出映射表")
    ap.add_argument("--list", action="store_true", help="列出映射表")
    ap.add_argument("--emit-sql", action="store_true", help="输出概念集 SQL 骨架")
    ap.add_argument("--out", help="SQL 输出文件")
    args = ap.parse_args()

    if args.demo:
        return _demo()

    if args.list or not (args.emit_sql or args.out):
        print("源代码 | 名称 | vocabulary | OMOP concept_id(待校验)")
        for code, (name, vocab, cid) in PROCEDURE_MAP.items():
            print(f"  {code} | {name} | {vocab} | {cid}")
    if args.emit_sql:
        sql = emit_sql()
        if args.out:
            # 自动创建父目录；失败给出友好错误而非裸 traceback（2026-10-12 压力测试修复）
            parent = os.path.dirname(os.path.abspath(args.out))
            try:
                os.makedirs(parent, exist_ok=True)
                with open(args.out, "w", encoding="utf-8") as f:
                    f.write(sql)
            except OSError as e:
                print(f"[error] 无法写入 {args.out}: {e}", file=sys.stderr)
                return 2
            print(f"[ok] 已写 {args.out}")
        else:
            print(sql)
    return 0


if __name__ == "__main__":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass
    raise SystemExit(main())
