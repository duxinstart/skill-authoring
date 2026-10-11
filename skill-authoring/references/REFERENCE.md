# Agent Skill 技术参考

本文件是 `skill-authoring` 的详细规范参考。`SKILL.md` 讲「怎么开始」，这里讲「每个细节到底是什么」。

## 1. 目录结构

一个技能是一个目录，至少包含一个 `SKILL.md`：

```
skill-name/
├── SKILL.md          # 必需：元数据 + 指令
├── references/       # 可选：按需加载的文档
├── scripts/          # 可选：可执行代码
├── assets/           # 可选：模板、schema、数据
└── ...               # 允许任意其他文件
```

**硬性要求**：`SKILL.md` 必须存在，且文件名大小写为 `SKILL.md`（解析器通常也接受 `skill.md`）。

## 2. frontmatter 字段

`SKILL.md` 必须以 YAML frontmatter 开头，后接 Markdown 正文。

| 字段 | 必需 | 约束 |
|---|---|---|
| `name` | 是 | 1–64 字符；仅小写字母、数字、连字符；不可首尾或连续连字符；**必须等于父目录名** |
| `description` | 是 | 1–1024 字符；非空；说明「做什么」与「何时用」 |
| `license` | 否 | 许可证名，或指向随附许可证文件 |
| `compatibility` | 否 | ≤500 字符；环境要求 |
| `metadata` | 否 | string → string 的键值对 |
| `allowed-tools` | 否 | 空格分隔的预授权工具（实验性） |

**硬性要求**：字段是**封闭集合**。出现上表之外的字段即校验失败。需要自定义信息时，放进 `metadata`。

### 最小示例

```yaml
---
name: skill-name
description: A description of what this skill does and when to use it.
---
```

### 含可选字段的示例

```yaml
---
name: pdf-processing
description: Extract PDF text, fill forms, merge files. Use when handling PDFs.
license: Apache-2.0
metadata:
  author: example-org
  version: "1.0"
---
```

## 3. name 规则

**硬性要求**：

- 1–64 字符
- 仅小写字母、数字、连字符
- 不可首尾为连字符
- 不可含连续连字符（`--`）
- **必须与父目录名一致**

| 合法 | 非法 | 原因 |
|---|---|---|
| `pdf-processing` | `PDF-Processing` | 含大写 |
| `data-analysis` | `-pdf` | 以连字符开头 |
| `code-review` | `pdf--processing` | 连续连字符 |

> 校验前会对名称做 NFKC 规范化。中文等非 ASCII 字符**不在允许集合内**——技能名请用 ASCII 小写。

## 4. description 规则

**硬性要求**：1–1024 字符，非空。

**建议**：同时描述「做什么」与「何时用」，并带上便于检索的关键词。写法详见 `description-guide.md`。

## 5. 渐进式加载

技能分三层加载，这决定了内容该放在哪：

| 层级 | 加载内容 | 时机 | 预算 |
|---|---|---|---|
| 元数据 | `name` + `description` | 会话启动 | 约 50–100 tokens / 个 |
| 指令 | 整篇 `SKILL.md` 正文 | 技能被激活 | 每次激活都完整占用 |
| 资源 | `scripts/` `references/` `assets/` | 被引用且需要时 | 视情况 |

**建议**：`SKILL.md` 只放每次运行都要用的调度信息；"偶尔才用"的细节移入 `references/`，并在流程中写明何时加载。

## 6. 文件引用

**建议**：使用相对技能根目录的路径，且只引用**一层深**。

```markdown
详见 [参考](references/REFERENCE.md)。

运行脚本：
scripts/extract.py
```

避免深层嵌套引用链（如 `references/a/b/c.md`）。

## 7. 校验

官方参考库：

```bash
skills-ref validate ./my-skill
```

它会检查 frontmatter 是否合法、命名是否符合约定。常见报错与修复见 `validation-errors.md`。
