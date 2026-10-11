# 校验报错与修复

**条件触发文档**：只在 `scripts/validate.py` 报错、或 `skills-ref validate` 失败时才需要读。

## 1. 先看引擎

`scripts/validate.py` 的输出里有一个 `engine` 字段：

- `"skills-ref"` —— 用的是参考库，结论权威
- `"builtin"` —— 参考库未安装，用的是内置格式检查（**只验格式，不验全部规则**）

若看到 `builtin`，且结果通过但你仍不确定，请安装参考库后重跑：

```bash
cd <agentskills>/skills-ref
python3 -m venv .venv && source .venv/bin/activate && pip install -e .
```

## 2. 常见错误对照表

| 报错信息（大意） | 原因 | 修复 |
|---|---|---|
| `Missing required file: SKILL.md` | 目录里没有 `SKILL.md` | 新建该文件（大小写必须是 `SKILL.md`） |
| `must start with YAML frontmatter (---)` | 文件开头不是 `---` | 在文件**第一行**加 `---`，并在 frontmatter 后再加一行 `---` |
| `frontmatter not closed with ---` | 缺少闭合的 `---` | 补上第二处 `---` |
| `Missing required field: name` | frontmatter 里没有 `name` | 添加 `name:`，值须等于目录名 |
| `Missing required field: description` | 没有 `description` | 添加 `description:`，说明做什么与何时用 |
| `name ... must match directory name` | 名称与目录名不一致 | 二者改为完全一致 |
| `name ... must be lowercase` | 含大写字母 | 改为全小写 |
| `name may only contain ...` | 含非法字符（空格、下划线、中文等） | 只保留小写字母、数字、单个连字符 |
| `cannot start or end with a hyphen` | 首尾有连字符 | 去掉 |
| `cannot contain consecutive hyphens` | 出现 `--` | 合并为单个连字符 |
| `exceeds 64 characters` | 名称过长 | 缩短到 ≤64 |
| `description exceeds 1024 characters` | 描述过长 | 精简到 ≤1024 |
| `Unexpected frontmatter fields: ...` | 出现未定义字段 | 删除该字段；自定义信息放进 `metadata` |
| `Invalid YAML in frontmatter` | YAML 语法错误 | 常见于值里含未加引号的冒号，用引号包住或改用 `>` 折叠块 |

## 3. 最容易踩的三个坑

1. **`name` 与目录名不一致**——改名时只改了目录或只改了字段。
2. **自创 frontmatter 字段**——frontmatter 是封闭白名单，多一个就失败。
3. **值里有冒号却没加引号**：

   ```yaml
   # 非法
   description: Use this skill when: the user asks about PDFs

   # 合法（加引号）
   description: "Use this skill when: the user asks about PDFs"

   # 合法（折叠块）
   description: >
     Use this skill when the user asks about PDFs
   ```

## 4. 校验通过 ≠ 技能可用

`skills-ref validate` 只检查**格式合规**（frontmatter、命名、必需文件）。它**不检查**：

- 脚本能否运行
- 技能是否真的会被触发（那是 `description` 的问题，见 `description-guide.md`）
- 正文指令是否有效

格式过了，仍需用真实任务试跑。
