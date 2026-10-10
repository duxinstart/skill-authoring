---
name: My-Skill
description: Helps with stuff.
version: "1.0"
---

# My Skill

这是一个**故意写坏的**技能样例，用于测试校验与描述检查流程。

它同时包含三类典型错误：

1. `name` 含大写字母，且与目录名 `my-skill` 不一致
2. 出现了未定义的 frontmatter 字段 `version`（应放进 `metadata`）
3. `description` 过于笼统，既没说"做什么"，也没说"何时用"
