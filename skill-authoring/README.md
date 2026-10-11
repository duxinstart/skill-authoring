# skill-authoring

一个用来**新建 / 校验 / 优化 Agent Skill** 的技能。

本目录同时是《Agent Skill 目录结构规范》站点里 `examples.html` 的**贯穿示例**——它按阶段从最小版生长为完整版，可作为真实技能使用。

## 它做什么

- **新建**：用 `scripts/scaffold.py` 生成合规的技能骨架
- **校验**：用 `scripts/validate.py` 对照格式规范检查（优先调用 `skills-ref`）
- **优化描述**：用 `scripts/lint_description.py` 检查 `description` 的触发质量

## 目录

```
skill-authoring/
├── SKILL.md                     # 入口 + 资源路由表
├── references/
│   ├── REFERENCE.md             # 格式规范细则
│   ├── description-guide.md     # 描述写法与触发优化
│   └── validation-errors.md     # 条件触发：校验失败时读
├── scripts/
│   ├── scaffold.py              # 生成技能骨架
│   ├── validate.py              # 校验技能（包装 skills-ref）
│   └── lint_description.py      # 检查描述质量
├── assets/
│   ├── templates/SKILL.md.template
│   ├── schemas/frontmatter.schema.json
│   └── data/field-catalog.json
└── evals/
    ├── evals.json
    └── files/                   # 测试素材（含一个故意写坏的样例）
```

## 安装与使用

```bash
# 1) 安装校验库（可选，装了 validate.py 会用它）
cd <agentskills>/skills-ref
python3 -m venv .venv && source .venv/bin/activate && pip install -e .

# 2) 生成一个技能骨架
python3 scripts/scaffold.py pdf-processing --out ./skills

# 3) 校验
python3 scripts/validate.py ./skills/pdf-processing

# 4) 检查描述质量
python3 scripts/lint_description.py ./skills/pdf-processing
```

## 环境要求

- Python 3.10+
- 完整校验需 `skills-ref`；未安装时 `validate.py` 会退化为内置的**格式检查**（输出中的 `engine` 字段会标明）

## 许可

Apache-2.0
