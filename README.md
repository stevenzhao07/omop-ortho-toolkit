# omop-ortho-toolkit

> **Contributed by [@stevenzhao07](https://github.com/stevenzhao07) · Affiliation: MedXpert (medical-device RA & regulatory consultancy) · Pure technical input, no commercial promotion.**

把骨科手术登记（关节置换 TKA/THA、植入物）映射到 OHDSI OMOP CDM 的 ETL 提案与示例：源代码（CPT/SNOMED）→ OMOP 概念集，产出概念集 SQL 骨架。投 OHDSI CDM WG。

这是 MedXpert 把"医疗 AI 信任"方法论工程化落地的可插拔模块之一——把抽象的合规要求变成一条可重复运行的命令或参考实现。方法论四要素（白话版）：**治理守护者 XCGS** ＝ 为 AI 留下可核验的治理证据；**立法者 A³ Laws** ＝ 给自主系统划权限 / 监督 / 追责三条硬边界；**护照官 AI 护照** ＝ 为模型签发可追溯的身份凭证；**人机共存** ＝ 明确人类与 AI 的分工与兜底。

---

## 可插拔模块契约（lgd-skeleton/1.0）

本仓库是一个 **`lgd-skeleton/1.0` 可插拔模块**：

- **一切即插件**：仅依赖声明式 `module.json`，零配置；
- **按需装（lazy）**：仅 triggers 命中时加载；
- **可嵌套（nested）**：可被 `medical-ai-toolkit` 总入口路由发现；
- **扩展点**：`plugins/`(新增术式：在 `PROCEDURE_MAP` 加源代码→名称，SQL 骨架自动扩。)。

机器可发现入口：`AGENTS.md` · `CLAUDE.md` · `llms.txt`。

## 特性

- 概念集：TKA(CPT 27447) / THA(CPT 27130) / 植入物 等源代码 → OMOP vocabulary 映射
- ETL 骨架：`--emit-sql` 产出 concept_set 的 INSERT 骨架（concept_id 标注待 vocab 校验）
- 诚实标注：OMOP standard concept_id 须以本地 vocab 复核，脚本显式标记待校验项
- 零依赖 + CLI

**上游投稿目标**：OHDSI CDM WG

## 内容说明

本仓是提案（proposal）而非已验证的 vocab：concept_id 以 `(27447 -> ?)` 待复核条目标注『需以本地 OMOP vocabulary 复核』，避免误导。投 OHDSI CDM WG，以个人专家 Xinghua Zhao 名义提交社区评审。

## 免责声明

本工具仅提供结构化模板与计算能力，**不构成法规建议、临床建议或产品合规结论**。具体产品的注册、临床评价、灭菌验证、风险分析、软件分级等决策，须由合资格人员依据目标辖区（NMPA / FDA / EU MDR / PMDA）最新法规文本作出；条款与限值以官方发布文本为准。使用本工具产生的一切后果由使用者自行承担。

## 使用

```bash
python scripts/omop_ortho.py --list
python scripts/omop_ortho.py --emit-sql --out ortho_concept_set.sql
```

## 快速开始（30 秒）

```bash
git clone https://github.com/stevenzhao07/omop-ortho-toolkit.git && cd omop-ortho-toolkit
python scripts/omop_ortho.py --demo
```

> 想参与或遇到问题？[提 Issue](https://github.com/stevenzhao07/omop-ortho-toolkit/issues) · 完整《AI 参与指南》见 [medical-ai-toolkit](https://github.com/stevenzhao07/medical-ai-toolkit)。

## 路由（总入口）

本模块由 **[medical-ai-toolkit](https://github.com/stevenzhao07/medical-ai-toolkit)** 作为 `lgd-skeleton/1.0` 总入口自动路由发现。

## 关联模块

- [fhir-ortho-toolkit](https://github.com/stevenzhao07/fhir-ortho-toolkit)
- [medical-ai-toolkit](https://github.com/stevenzhao07/medical-ai-toolkit)

## 许可

Apache-2.0 — 见 [LICENSE](./LICENSE)。

## 关联（方法论来源）

- 理念溯源：个人专家关于医疗 AI 信任与治理的公开方法论（个人观点，不构成标准）
- 同账号系列：见 `medical-ai-toolkit` 导航
