# 测试素材说明

本目录存放评测用例所依赖的输入文件。

## `my-skill/`

一个**故意写坏**的技能样例，用于验证两类能力：

- 校验能否定位到真实错误（`scripts/validate.py`）
- 描述检查能否指出触发问题（`scripts/lint_description.py`）

它刻意包含三类问题：

| # | 问题 | 期望被检出的方式 |
|---|---|---|
| 1 | `name` 含大写、且与目录名不一致 | 校验报 "name must be lowercase" / "must match directory name" |
| 2 | 出现未定义字段 `version` | 校验报 "Unexpected frontmatter fields: version" |
| 3 | `description` 过于笼统 | 描述检查给出 warning |

> ⚠️ 注意：本目录下的 `SKILL.md` 是**测试素材，不是可安装的技能**。请勿把它复制进 `.agents/skills/` 等技能目录，否则会被扫描成一个名为 `my-skill` 的技能。
