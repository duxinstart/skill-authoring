# Agent Skill 目录结构规范

> 一份面向中文读者的 **Agent Skill** 撰写规范站点。
>
> A Chinese-language specification site for authoring Agent Skills.

Agent Skill 是用于扩展 AI agent 能力的轻量开放格式：把「程序性知识」与「团队 / 项目专有上下文」打包成可移植、可版本化的文件夹，agent 按需加载。

本项目回答一个问题：**一个合规、好用、能被稳定触发的 Skill，到底该怎么写。**

---

## 项目包含

| 部分 | 形态 | 用途 |
|---|---|---|
| **规范站点** | 10 个静态 HTML 页面 + 1 个 CSS | 给人阅读的撰写指南，从目录结构讲到每个子目录的写法 |

> **示例与技能包待重建。** 原示例技能 `skill-authoring` 的内容已移除——它由单方面完成，**未经「示例要求说明书」定义与验收**，不具备作为示例的资格。目录位置已保留（[`skill-authoring/`](skill-authoring/)），待要求确定后重建。

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
├── examples.html               # 完整示例（待重建）
├── skill-spec.css              # 全站共用样式
├── 文档定位说明.md             # 全站撰写准绳
│
└── skill-authoring/            # 示例技能位置（内容待重建）
    └── README.md               # 说明：为何移除、重建前提
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
| [`examples.html`](examples.html) | **完整示例** | 待重建（原示例已移除） |

> 页面之间通过相对路径互相链接，请在**同一目录**下整体浏览，勿单独移动单个 HTML 文件。

**推荐阅读顺序**：首页 → `structure-detail` → `skill-md` → `description` → 四个子目录页 → `design` → `examples`。

---

## skill-authoring（待重建）

一个用来**新建 / 校验 / 优化 Agent Skill** 的技能——**内容已移除，待重建**。

**为什么移除**：原示例由单方面完成，没有经过「示例要求说明书」的定义，也没有经过验收，不具备作为示例的资格。

**当前状态**：目录位置保留，内含一份 [`README.md`](skill-authoring/README.md) 说明移除原因与重建前提。完整内容在 git 历史中（提交 `32bdef6` 及更早），可恢复。

**重建前提**：先完成《示例要求说明书》——定义它要证明什么、必须覆盖哪些目录与页面原则、验收标准、形态与主题。

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
| [`skills-ref`](https://github.com/agentskills/agentskills/tree/main/skills-ref) | 可选 | 校验库。安装后 `validate.py` 会优先调用它；未安装时自动退化为内置的**格式检查**，输出中的 `engine` 字段会标明用的是哪套 |

安装校验库（可选）：

```bash
# 需先取得 agentskills 仓库（见下方「与上游的关系」）
cd <agentskills>/skills-ref
python3 -m venv .venv && source .venv/bin/activate && pip install -e .
```

---

## 内容口径（阅读时请注意）

文档对每一条规则都区分了**性质**，不要把它们当成同一等级的约束：

| 标记 | 含义 |
|---|---|
| **硬性** | 运行时强制，违反会导致技能无法被加载 |
| **建议** | 我们给出的推荐，不做不会报错，但效果会差 |
| **实验性** | 客户端支持不一，谨慎使用 |

典型例子：**硬性**只覆盖 frontmatter 字段、命名与必需文件——违反会被校验器拒绝。而「调度信息必须完整清晰、冗余必须剔除」属于**建议**层面的原则，不进校验器，违反了也不会报错。

---

## 与上游的关系

本项目的格式规范与 **[agentskills/agentskills](https://github.com/agentskills/agentskills)** 保持一致，`skill-authoring` 的校验也优先复用其参考库 `skills-ref`。

上游仓库**不包含在本仓库中**（已在 [`.gitignore`](.gitignore) 中排除）。如需完整校验能力，请单独克隆：

```bash
git clone https://github.com/agentskills/agentskills.git
```

---

## 许可

本项目采用 **Apache-2.0**，完整条款见 [LICENSE](LICENSE)。
