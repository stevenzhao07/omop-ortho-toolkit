# AGENTS.md · omop-ortho-toolkit

> 机器可发现入口（AI 编码代理 / Codex / Claude / Cursor）。单一事实源：本文件。

## 这是什么
把骨科手术登记（关节置换 TKA/THA、植入物）映射到 OHDSI OMOP CDM 的 ETL 提案与示例：源代码（CPT/SNOMED）→ OMOP 概念集，产出概念集 SQL 骨架。投 OHDSI CDM WG。

## 运行
```bash
python scripts/omop_ortho.py --demo
python scripts/omop_ortho.py --help
```

## 扩展契约（lgd-skeleton/1.0）
- **一切即插件**：仅依赖声明式 `module.json`，零配置。
- **按需装（lazy）**：仅 triggers 命中时加载。
- **可嵌套（nested）**：可被 `medical-ai-toolkit` 总入口路由。
- **扩展点**：`plugins/`(新增术式：在 `PROCEDURE_MAP` 加源代码→名称，SQL 骨架自动扩。)

## 红线
纯技术贡献，不含商业营销；MedXpert 仅作为贡献者署名（@stevenzhao07）。
