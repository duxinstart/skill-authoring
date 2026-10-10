---
name: skill-authoring
description: >
  创建、校验与优化 Agent Skill——生成合规的技能目录骨架、对照官方格式规范做校验、
  并打磨 description 让技能能被稳定触发。当用户想新建一个 skill、校验或调试已有 skill、
  修复校验不通过的 skill、或改进一个总是不被触发的 skill 时使用，即使用户没有明确说"技能"。
license: Apache-2.0
compatibility: Requires Python 3.10+. Full validation additionally needs the skills-ref library (pip install -e <agentskills>/skills-ref); without it, scripts/validate.py falls back to a built-in format-only check.
metadata:
  author: skill-spec-project
  version: "1.0"
---

# Skill Authoring

帮用户**新建 / 校验 / 优化** Agent Skill。

## 何时使用

当用户想要：

- **新建**一个 skill（从零搭出目录与 `SKILL.md`）
- **校验**现有 skill 是否符合官方格式规范
- **修复**一个"校验不通过"的 skill
- **优化**一个"总是不被触发"的 skill

**不适用**于：单纯阅读规范文档（那不需要本技能）。

## 快速开始

1. 确认技能名（kebab-case，**必须与目录名一致**）
2. 生成骨架：`python3 scripts/scaffold.py <name> --out <dir>`
3. 按 `assets/templates/SKILL.md` 填写正文
4. 校验：`python3 scripts/validate.py <skill-dir>`

## 核心流程

1. 明确技能**做什么**、**何时触发**
2. 用 `scripts/scaffold.py` 生成目录骨架
3. 写 frontmatter（`name` / `description` 必需）
4. 写正文：何时使用 → 快速开始 → 核心流程 → 资源路由表 → Gotchas
5. 校验：`python3 scripts/validate.py <skill-dir>`
6. 若校验失败，查 `references/validation-errors.md`
7. 检查描述质量：`python3 scripts/lint_description.py <skill-dir>`

## 资源路由表

| 当任务涉及… | 读取 |
|---|---|
| frontmatter 字段、命名、目录约定 | `references/REFERENCE.md` |
| description 怎么写、如何提高触发率 | `references/description-guide.md` |
| 校验报错、不知道错在哪 | `references/validation-errors.md` |
| 生成技能骨架 | `scripts/scaffold.py` + `assets/templates/SKILL.md` |
| 校验技能是否合规 | `scripts/validate.py` |
| 检查描述质量 | `scripts/lint_description.py` |
| frontmatter 结构定义 | `assets/schemas/frontmatter.schema.json` |
| 字段速查 | `assets/data/field-catalog.json` |

## Gotchas

- `name` 必须**等于父目录名**，否则校验失败——这是最常见的错误。
- frontmatter 是**封闭白名单**：出现未定义字段会被直接拒绝，别自创字段。
- `description` 决定技能能否被触发。只写"做什么"、不写"何时用"，会导致**永不触发**。
- `skills-ref` 未安装时，`scripts/validate.py` 会退化为**内置检查**（只验格式，不验全部规则），输出里的 `engine` 字段会标明用的是哪套。
