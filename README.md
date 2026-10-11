# Agent Skill 目录结构规范

> 一份面向中文读者的 **Agent Skill** 撰写规范站点，外加一个可直接使用的技能包 [`skill-authoring`](skill-authoring/)。
>
> A Chinese-language specification site for authoring Agent Skills, bundled with a ready-to-use `skill-authoring` skill.

Agent Skill 是用于扩展 AI agent 能力的轻量开放格式：把「程序性知识」与「团队 / 项目专有上下文」打包成可移植、可版本化的文件夹，agent 按需加载。

本项目回答一个问题：**一个合规、好用、能被稳定触发的 Skill，到底该怎么写。**

---

## 项目包含两部分

| 部分 | 形态 | 用途 |
|---|---|---|
| **规范站点** | 10 个静态 HTML 页面 + 1 个 CSS | 给人阅读的撰写指南，从目录结构讲到每个子目录的写法 |
| **技能包** | [`skill-authoring/`](skill-authoring/) | 给 agent 用的技能：新建 / 校验 / 优化 Skill，可安装到任意支持 Skill 的 agent |

站点里的 [`examples.html`](examples.html) 正是以 `skill-authoring` 为**贯穿示例**——它按五个阶段从最小版生长为完整版，所以这两部分是同一份内容的两种形态。

---

## 目录结构

```
.
├── index.html                  # 首页 · 总览入口（GitHub Pages 入口）
├── structure-detail.html       # 目录结构详解
├── skill-md.html               # SKILL.md 撰写指南
├── description.html            # 描述与触发优化
├── design.html                 # 目录取舍与设计流程
├── references.html             # references/ 撰写指南
├── scripts.html                # scripts/ 撰写指南
├── assets.html                 # assets/ 撰写指南
├── evals.html                  # evals/ 撰写指南
├── examples.html               # 完整示例（贯穿 skill-authoring）
├── skill-spec.css              # 全站共用样式
│
└── skill-authoring/            # 可直接使用的技能包
    ├── SKILL.md                # 入口 + 资源路由表
    ├── references/             # 格式细则、描述写法、报错对照
    ├── scripts/                # scaffold / validate / lint_description
    ├── assets/                 # 模板、schema、字段速查表
    └── evals/                  # 评测用例与测试素材
```

---

## 规范站点 · 页面导航

| 页面 | 主题 | 主要内容 |
|---|---|---|
| [`index.html`](index.html) | **首页 · 总览** | 什么是 Agent Skill、渐进式加载、目录结构总览图 |
| [`structure-detail.html`](structure-detail.html) | 目录结构详解 | 每个目录的职责与边界 |
| [`skill-md.html`](skill-md.html) | **SKILL.md 撰写指南** | frontmatter 详解、正文结构、写作原则、自检清单、常见错误速查 |
| [`description.html`](description.html) | 描述与触发优化 | `description` 为何决定一切、五条写作原则、触发优化闭环 |
| [`references.html`](references.html) | `references/` 撰写指南 | 何时才需要、主参考 / 领域知识 / 条件触发文档的划分、反模式 |
| [`scripts.html`](scripts.html) | `scripts/` 撰写指南 | 自包含、禁止交互式提示、错误自纠、stdout/stderr 分流、完整骨架 |
| [`assets.html`](assets.html) | `assets/` 撰写指南 | templates / schemas / data 三类静态资源 |
| [`evals.html`](evals.html) | `evals/` 撰写指南 | 用例设计、断言写法、运行与判分迭代 |
| [`design.html`](design.html) | 目录取舍与设计流程 | 六步演进路径、三个判断问题、常见反模式 |
| [`examples.html`](examples.html) | **完整示例** | `skill-authoring` 的五个阶段演进与最终总览 |

> 页面之间通过相对路径互相链接，请在**同一目录**下整体浏览，勿单独移动单个 HTML 文件。

**推荐阅读顺序**：首页 → `structure-detail` → `skill-md` → `description` → 四个子目录页 → `design` → `examples`。

---

## skill-authoring 技能包

一个用来**新建 / 校验 / 优化 Agent Skill** 的技能。

**它做什么**

- **新建** — `scripts/scaffold.py` 生成合规的技能骨架
- **校验** — `scripts/validate.py` 对照官方格式规范检查（优先调用官方 `skills-ref`）
- **优化描述** — `scripts/lint_description.py` 检查 `description` 的触发质量

**目录**

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
    ├── evals.json               # 3 条评测用例
    └── files/                   # 测试素材（含一个故意写坏的样例）
```

**快速使用**

```bash
cd skill-authoring

# 1) 生成一个技能骨架
python3 scripts/scaffold.py pdf-processing --out ./skills

# 2) 校验是否符合格式规范
python3 scripts/validate.py ./skills/pdf-processing

# 3) 检查 description 的触发质量
python3 scripts/lint_description.py ./skills/pdf-processing
```

---

## 在线预览

本项目已启用 **GitHub Pages**（纯静态托管，无需构建）：

**<https://duxinstart.github.io/skill-authoring/>**

推送到 `main` 分支后会自动重新构建部署，通常 1–2 分钟生效。

## 本地预览

HTML 页面是纯静态的，直接双击打开即可。若要一次性起个本地站点：

```bash
# 在项目根目录执行
python3 -m http.server 8000
# 然后浏览器打开 http://localhost:8000/
```

---

## 环境要求

| 依赖 | 版本 | 说明 |
|---|---|---|
| Python | 3.10+ | 运行 `skill-authoring/scripts/` 下的脚本 |
| [`skills-ref`](https://github.com/agentskills/agentskills/tree/main/skills-ref) | 可选 | 官方校验库。安装后 `validate.py` 会优先调用它；未安装时自动退化为内置的**格式检查**，输出中的 `engine` 字段会标明用的是哪套 |

安装官方校验库（可选）：

```bash
# 需先取得 agentskills 仓库（见下方「与上游的关系」）
cd <agentskills>/skills-ref
python3 -m venv .venv && source .venv/bin/activate && pip install -e .
```

---

## 内容口径（阅读时请注意）

文档对每一条规则都区分了**来源**，不要把它们当成同一等级的约束：

| 标记 | 含义 |
|---|---|
| **硬性要求** | 来自官方格式规范，违反即校验失败 |
| **建议** | 官方推荐做法，不是强制 |
| **实践经验** | 本项目的归纳，供参考，可依场景取舍 |

典型例子：**硬性要求**只覆盖 frontmatter 字段、命名与必需文件（见官方 specification）——违反会被校验器拒绝。而「调度信息必须完整清晰、冗余必须剔除」属于**实践经验**层面的原则，不进校验器，违反了也不会报错。

---

## 与上游的关系

本项目的格式规范以 **[agentskills/agentskills](https://github.com/agentskills/agentskills)** 为准，`skill-authoring` 的校验也优先复用其官方库 `skills-ref`。

上游仓库**不包含在本仓库中**（已在 [`.gitignore`](.gitignore) 中排除）。如需完整校验能力，请单独克隆：

```bash
git clone https://github.com/agentskills/agentskills.git
```

---

## 许可

本项目采用 **Apache-2.0**，完整条款见 [LICENSE](LICENSE)。
