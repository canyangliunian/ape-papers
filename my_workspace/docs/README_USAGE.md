# APE 论文浏览器使用指南

## 简介

APE (Autonomous Policy Evaluation) 论文浏览器是一个 AI 辅助经济学研究学习系统，帮助用户通过分析 APE 论文仓库，学习如何使用 AI Agents（如 Claude Code、Codex）进行经济学研究和论文写作。

**作者**：凌贵旺（南京农业大学经济管理学院）
**邮箱**：lingguiwang@yeah.net

---

## 快速开始

### 1. 列出所有可用论文

```bash
python3 paper_explorer.py --list
```

### 2. 查看论文完整流程

```bash
python3 paper_explorer.py apep_0185 --flow
```

### 3. 查看帮助信息

```bash
python3 paper_explorer.py --help
```

---

## 核心功能

| 命令 | 描述 | 示例 |
|------|------|------|
| `--list` | 列出所有可用论文 | `python3 paper_explorer.py --list` |
| `--flow` | 展示完整研究流程 | `python3 paper_explorer.py apep_0185 --flow` |
| `--init` | 查看初始化配置 | `python3 paper_explorer.py apep_0185 --init` |
| `--ideas` | 浏览研究想法和排序 | `python3 paper_explorer.py apep_0185 --ideas` |
| `--plan` | 查看研究计划 | `python3 paper_explorer.py apep_0185 --plan` |
| `--code` | 查看代码结构 | `python3 paper_explorer.py apep_0185 --code` |
| `--paper` | 生成论文摘要 | `python3 paper_explorer.py apep_0185 --paper` |
| `--review` | 查看评审意见 | `python3 paper_explorer.py apep_0185 --review` |
| `--compare v1 v2` | 对比版本差异 | `python3 paper_explorer.py apep_0185 --compare v1 v16` |
| `--extract` | 提取 AI 提示词模板 | `python3 paper_explorer.py apep_0185 --extract` |

---

## 研究流程架构

APE 论文流程分为 **6 个阶段**，涉及 **20+ 种文件类型**：

### 阶段 1：初始化

| 文件 | 作用 |
|------|------|
| `initialization.md` | 研究配置：领域、方法、数据来源选择 |
| `initialization.sha256` | 初始化配置的哈希验证 |

### 阶段 2：发现

| 文件 | 作用 |
|------|------|
| `ideas.md` | 生成多个研究想法（政策、识别、机制、数据来源） |
| `ideas_ranked.json` | 想法排序结果（分数、推荐） |
| `ranking.md` | 详细排序评估（DiD 评估、优缺点分析） |
| `ranking_status.json` | 排序状态（是否进入执行阶段） |
| `initial_plan.md` | 基于选中想法的初步研究计划 |
| `conditions.md` | **关键文件**！验证数据可行性条件，全部标记 RESOLVED 才能继续 |

### 阶段 3：执行

| 文件/文件夹 | 作用 |
|-------------|------|
| `research_plan.md` | 最终锁定研究计划（识别策略、数据方案） |
| `code/` | 分析代码（`01_fetch_data.R`, `02_clean_data.R`, `03_main_analysis.R` 等） |
| `figures/` | 生成图表 |
| `tables/` | 生成表格 |
| `scan_report.json` | 数据扫描报告 |

### 阶段 4：内部评审

| 文件 | 作用 |
|------|------|
| `advisor_gpt_1.md` | GPT 导师建议（检查数据设计、回归合理性、完整性） |
| `advisor_gemini_1.md` | Gemini 导师建议 |
| `advisor_grok_1.md` | Grok 导师建议 |
| `advisor_code_1.md` | Code 导师建议 |
| `advisor_summary.json` | 导师建议汇总 |

### 阶段 5：论文写作

| 文件 | 作用 |
|------|------|
| `PROMPT.md` | **论文生成提示词**（给 AI 的详细指令） |
| `paper.tex` | LaTeX 源码 |
| `paper.pdf` | 最终 PDF |
| `references.bib` | 参考文献 BibTeX 文件 |

### 阶段 6：外部评审与修订

| 文件 | 作用 |
|------|------|
| `review_gpt_1.md` | GPT 评审意见 |
| `review_gemini_1.md` | Gemini 评审意见 |
| `review_grok_1.md` | Grok 评审意见 |
| `review_cc_1.md` | CrossCheck 评审意见 |
| `parallel_review_summary.json` | 多模型评审汇总 |
| `reply_to_reviewers_1.md` | 回应评审意见 |
| `revision_plan_1.md` | 修订计划 |

---

## 学习路径

建议按以下顺序学习 `apep_0185`（关于最低工资网络溢出效应的研究）：

| 步骤 | 阶段 | 关键文件 | 命令 |
|------|--------|----------|------|
| 1 | 初始化 | `initialization.md` | `--init` |
| 2 | 想法生成 | `ideas.md` + `ranking.md` | `--ideas` |
| 3 | 研究设计 | `research_plan.md` | `--plan` |
| 4 | 数据分析 | `code/*.R` | `--code` |
| 5 | 论文写作 | `PROMPT.md` + `paper.tex` | `--paper` |
| 6 | 评审迭代 | `review_*.md` + `reply_to_reviewers_*.md` | `--review` |
| 7 | 版本对比 | 对比 v1 → v16 | `--compare v1 v16` |

### 学习建议

1. **第一阶段**：先阅读 `initialization.md`，了解研究的背景和目标
2. **第二阶段**：研究 `ideas.md` 和 `ranking.md`，了解如何生成和评估研究想法
3. **第三阶段**：仔细阅读 `research_plan.md`，了解研究设计的细节
4. **第四阶段**：阅读代码文件，理解数据获取、清洗、分析的完整流程
5. **第五阶段**：阅读 `PROMPT.md`，学习如何给 AI 提供论文写作指令
6. **第六阶段**：阅读评审意见和回复，了解如何处理审稿人意见
7. **第七阶段**：对比不同版本，了解论文是如何迭代改进的

---

## 相关论文推荐

根据您的研究领域（区域经济学、农业经济学、国际贸易学），推荐以下论文：

| 论文 ID | 主题 | 方法 | 相关性 | 推荐命令 |
|---------|------|------|--------|----------|
| apep_0185 | 网络溢出、shift-share | 空间 DiD | ★★★★（网络+区域） | `--flow` |
| apep_0001 | 州政策 | DiD | ★★★（劳动经济学） | `--flow` |
| apep_0135 | 政策扩散 | 空间计量 | ★★★（国际贸易/政策传播） | `--flow` |
| apep_0119 | 贸易政策 | 贸易引力模型 | ★★★（国际贸易） | `--flow` |
| apep_0149 | 农业生产 | DiD | ★★★（农业经济学） | `--flow` |

---

## 提示词模板提取

使用 `--extract` 命令可以从选定的论文中提取 AI 提示词模板：

```bash
python3 paper_explorer.py apep_0185 --extract
```

提取的模板将保存在 `analysis/templates/` 目录下：

- `init_template.md` - 初始化提示词模板
- `idea_prompt.md` - 研究想法生成提示词模板
- `plan_prompt.md` - 研究计划提示词模板

这些模板可以作为您自己研究的起点。

---

## 目录结构

```
ape-papers/
├── paper_explorer.py          # 主工具脚本
├── README_USAGE.md            # 本使用指南
├── analysis/                 # 分析输出目录
│   ├── templates/            # AI 提示词模板
│   │   ├── init_template.md
│   │   ├── idea_prompt.md
│   │   └── plan_prompt.md
│   └── notes/              # 学习笔记（用户自行创建）
│       └── apep_0185_notes.md
├── apep_0001/
├── apep_0002/
├── ...
└── apep_0324/
```

---

## 常见问题

### Q: 如何选择要学习的论文？

A: 建议从 `apep_0185` 开始，这篇论文有 16 个版本，展示了完整的研究迭代过程。然后根据您的具体研究领域选择相关论文。

### Q: 版本对比中的符号含义是什么？

A:
- `=` 文件未变化
- `~` 文件已修改
- `-` 文件仅在版本 A 中
- `+` 文件仅在版本 B 中

### Q: 如何使用提取的提示词模板？

A: 将 `analysis/templates/` 中的模板作为您自己的研究起点，根据您的具体研究问题进行修改。

### Q: 代码目录中的文件按什么顺序执行？

A: 代码文件按数字顺序执行：
- `00_packages.R` - 加载依赖包
- `01_fetch_data.R` - 获取数据
- `02_clean_data.R` - 清洗数据
- `03_main_analysis.R` - 主要分析
- `04_robustness.R` - 稳健性检验
- `05_figures.R` - 生成图表
- `06_tables.R` - 生成表格

---

## 系统要求

- Python 3.6 或更高版本
- 无需额外安装 Python 包（仅使用标准库）

---

## 联系方式

如有问题或建议，请联系：
- **作者**：凌贵旺
- **机构**：南京农业大学经济管理学院
- **邮箱**：lingguiwang@yeah.net

---

## 许可证

本工具仅供学习和研究使用。
