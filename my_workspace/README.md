# My Workspace - 个人工作区

这是我在 APE 论文仓库中的个人工作区，用于存放分析笔记、工具脚本和文档。

## 目录结构

```
my_workspace/
├── README.md                    # 本文件
├── scripts/                     # 工具脚本
│   └── paper_explorer.py       # APE 论文浏览器
├── docs/                        # 文档
│   ├── IMPLEMENTATION_REPORT.md # 实现报告
│   └── README_USAGE.md          # 使用说明
└── analysis/                    # 分析文件
    ├── notes/                   # 笔记
    │   └── apep_0185_notes_template.md
    └── templates/               # 模板
        ├── idea_prompt.md
        ├── init_template.md
        └── plan_prompt.md
```

## 快速开始

### 使用论文浏览器

```bash
# 列出所有论文
python my_workspace/scripts/paper_explorer.py --list

# 查看论文流程
python my_workspace/scripts/paper_explorer.py apep_0185 --flow

# 查看研究想法
python my_workspace/scripts/paper_explorer.py apep_0185 --ideas

# 查看代码结构
python my_workspace/scripts/paper_explorer.py apep_0185 --code
```

### 更多命令

```bash
# 查看初始化配置
python my_workspace/scripts/paper_explorer.py apep_0185 --init

# 查看研究计划
python my_workspace/scripts/paper_explorer.py apep_0185 --plan

# 查看论文摘要
python my_workspace/scripts/paper_explorer.py apep_0185 --paper

# 查看评审意见
python my_workspace/scripts/paper_explorer.py apep_0185 --review

# 对比版本差异
python my_workspace/scripts/paper_explorer.py apep_0185 --compare v1 v16
```

## 作者信息

- **姓名**: 凌贵旺
- **单位**: 南京农业大学经济管理学院
- **邮箱**: lingguiwang@yeah.net

## 说明

- 此工作区的文件不会影响原始 APE 论文仓库
- 可以随时从上游仓库 pull 最新内容
- 个人修改会保存在自己的 fork 仓库中
