#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
APE (Autonomous Policy Evaluation) 论文浏览器
AI 辅助经济学研究学习系统

作者: 凌贵旺
机构: 南京农业大学经济管理学院
邮箱: lingguiwang@yeah.net
"""

from pathlib import Path
import argparse
import json
import sys
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class ResearchStage(Enum):
    """研究阶段枚举"""
    INITIALIZATION = "初始化"
    DISCOVERY = "发现"
    EXECUTION = "执行"
    INTERNAL_REVIEW = "内部评审"
    PAPER_WRITING = "论文写作"
    EXTERNAL_REVIEW = "外部评审与修订"


@dataclass
class FileInfo:
    """文件信息数据类"""
    path: Path
    stage: ResearchStage
    description: str
    exists: bool = True


class PaperExplorer:
    """APE 论文浏览器核心类"""

    # 阶段 1: 初始化
    INIT_FILES = {
        "initialization.md": (
            ResearchStage.INITIALIZATION,
            "研究配置：领域、方法、数据来源选择"
        ),
        "initialization.sha256": (
            ResearchStage.INITIALIZATION,
            "初始化配置的哈希验证"
        ),
    }

    # 阶段 2: 发现
    DISCOVERY_FILES = {
        "ideas.md": (
            ResearchStage.DISCOVERY,
            "生成多个研究想法（政策、识别、机制、数据来源）"
        ),
        "ideas_ranked.json": (
            ResearchStage.DISCOVERY,
            "想法排序结果（分数、推荐）"
        ),
        "ranking.md": (
            ResearchStage.DISCOVERY,
            "详细排序评估（DiD 评估、优缺点分析）"
        ),
        "ranking_status.json": (
            ResearchStage.DISCOVERY,
            "排序状态（是否进入执行阶段）"
        ),
        "initial_plan.md": (
            ResearchStage.DISCOVERY,
            "基于选中想法的初步研究计划"
        ),
        "conditions.md": (
            ResearchStage.DISCOVERY,
            "验证数据可行性条件，全部标记 RESOLVED 才能继续"
        ),
    }

    # 阶段 3: 执行
    EXECUTION_FILES = {
        "research_plan.md": (
            ResearchStage.EXECUTION,
            "最终锁定研究计划（识别策略、数据方案）"
        ),
        "code/": (
            ResearchStage.EXECUTION,
            "分析代码目录（01_fetch_data.R, 02_clean_data.R, 03_main_analysis.R 等）"
        ),
        "figures/": (
            ResearchStage.EXECUTION,
            "生成图表目录"
        ),
        "tables/": (
            ResearchStage.EXECUTION,
            "生成表格目录"
        ),
        "scan_report.json": (
            ResearchStage.EXECUTION,
            "数据扫描报告"
        ),
    }

    # 阶段 4: 内部评审
    INTERNAL_REVIEW_FILES = {
        "advisor_gpt_1.md": (
            ResearchStage.INTERNAL_REVIEW,
            "GPT 导师建议（检查数据设计、回归合理性、完整性）"
        ),
        "advisor_gemini_1.md": (
            ResearchStage.INTERNAL_REVIEW,
            "Gemini 导师建议"
        ),
        "advisor_grok_1.md": (
            ResearchStage.INTERNAL_REVIEW,
            "Grok 导师建议"
        ),
        "advisor_code_1.md": (
            ResearchStage.INTERNAL_REVIEW,
            "Code 导师建议"
        ),
        "advisor_summary.json": (
            ResearchStage.INTERNAL_REVIEW,
            "导师建议汇总"
        ),
    }

    # 阶段 5: 论文写作
    PAPER_WRITING_FILES = {
        "PROMPT.md": (
            ResearchStage.PAPER_WRITING,
            "论文生成提示词（给 AI 的详细指令）"
        ),
        "paper.tex": (
            ResearchStage.PAPER_WRITING,
            "LaTeX 源码"
        ),
        "paper.pdf": (
            ResearchStage.PAPER_WRITING,
            "最终 PDF"
        ),
        "references.bib": (
            ResearchStage.PAPER_WRITING,
            "参考文献 BibTeX 文件"
        ),
    }

    # 阶段 6: 外部评审与修订
    EXTERNAL_REVIEW_FILES = {
        "review_gpt_1.md": (
            ResearchStage.EXTERNAL_REVIEW,
            "GPT 评审意见"
        ),
        "review_gemini_1.md": (
            ResearchStage.EXTERNAL_REVIEW,
            "Gemini 评审意见"
        ),
        "review_grok_1.md": (
            ResearchStage.EXTERNAL_REVIEW,
            "Grok 评审意见"
        ),
        "review_cc_1.md": (
            ResearchStage.EXTERNAL_REVIEW,
            "CrossCheck 评审意见"
        ),
        "parallel_review_summary.json": (
            ResearchStage.EXTERNAL_REVIEW,
            "多模型评审汇总"
        ),
        "reply_to_reviewers_1.md": (
            ResearchStage.EXTERNAL_REVIEW,
            "回应评审意见"
        ),
        "revision_plan_1.md": (
            ResearchStage.EXTERNAL_REVIEW,
            "修订计划"
        ),
    }

    # 全局文件
    GLOBAL_FILES = {
        "timing.json": "记录各阶段时间（setup、discovery、execution、internal_review）",
        "metadata.json": "论文元数据",
        "REPLICATION.md": "复现说明",
    }

    def __init__(self, base_dir: Path):
        """
        初始化论文浏览器

        Args:
            base_dir: ape-papers 仓库根目录
        """
        self.base_dir = Path(base_dir).resolve()
        self.analysis_dir = self.base_dir / "analysis"
        self.templates_dir = self.analysis_dir / "templates"
        self.notes_dir = self.analysis_dir / "notes"

        # 创建必要的目录
        self._create_directories()

    def _create_directories(self):
        """创建分析目录结构"""
        self.analysis_dir.mkdir(exist_ok=True)
        self.templates_dir.mkdir(exist_ok=True)
        self.notes_dir.mkdir(exist_ok=True)

    def list_papers(self) -> List[Path]:
        """列出所有论文目录"""
        papers = []
        for item in self.base_dir.iterdir():
            if item.is_dir() and item.name.startswith("apep_"):
                papers.append(item)
        return sorted(papers, key=lambda x: int(x.name.replace("apep_", "")))

    def get_versions(self, paper_id: str) -> List[str]:
        """获取指定论文的所有版本"""
        paper_dir = self.base_dir / paper_id
        if not paper_dir.exists():
            raise ValueError(f"论文 {paper_id} 不存在")

        versions = []
        for item in paper_dir.iterdir():
            if item.is_dir() and item.name.startswith("v"):
                try:
                    version_num = int(item.name[1:])
                    versions.append((version_num, item.name))
                except ValueError:
                    continue
        versions.sort()
        return [v[1] for v in versions]

    def show_flow(self, paper_id: str, version: str = "v1") -> str:
        """
        展示完整研究流程

        Args:
            paper_id: 论文 ID（如 "apep_0185"）
            version: 版本号（默认 "v1"）

        Returns:
            格式化的流程文本
        """
        version_dir = self.base_dir / paper_id / version
        if not version_dir.exists():
            return f"错误: {paper_id}/{version} 不存在"

        output = []
        output.append("=" * 80)
        output.append(f"论文: {paper_id}")
        output.append(f"版本: {version}")
        output.append("=" * 80)
        output.append("")

        # 按阶段展示
        all_files = [
            (self.INIT_FILES, ResearchStage.INITIALIZATION),
            (self.DISCOVERY_FILES, ResearchStage.DISCOVERY),
            (self.EXECUTION_FILES, ResearchStage.EXECUTION),
            (self.INTERNAL_REVIEW_FILES, ResearchStage.INTERNAL_REVIEW),
            (self.PAPER_WRITING_FILES, ResearchStage.PAPER_WRITING),
            (self.EXTERNAL_REVIEW_FILES, ResearchStage.EXTERNAL_REVIEW),
        ]

        for files, stage in all_files:
            output.append(f"【{stage.value}】")
            output.append("-" * 40)

            for filename, (_, description) in files.items():
                file_path = version_dir / filename
                exists = file_path.exists()
                status = "✓" if exists else "✗"

                if file_path.is_dir():
                    if exists:
                        count = len(list(file_path.glob("*")))
                        output.append(f"  {status} {filename}/ - {description} ({count} 项)")
                    else:
                        output.append(f"  {status} {filename}/ - {description}")
                else:
                    output.append(f"  {status} {filename} - {description}")

            output.append("")

        # 全局文件
        output.append("【全局文件】")
        output.append("-" * 40)
        for filename, description in self.GLOBAL_FILES.items():
            file_path = version_dir / filename
            exists = file_path.exists()
            status = "✓" if exists else "✗"
            output.append(f"  {status} {filename} - {description}")

        output.append("")
        output.append("=" * 80)

        return "\n".join(output)

    def show_init(self, paper_id: str, version: str = "v1") -> str:
        """查看初始化配置"""
        return self._show_file_content(
            paper_id, version, "initialization.md",
            "初始化配置", ResearchStage.INITIALIZATION
        )

    def show_ideas(self, paper_id: str, version: str = "v1") -> str:
        """浏览研究想法和排序"""
        output = []

        # ideas.md
        ideas_content = self._show_file_content(
            paper_id, version, "ideas.md",
            "", ResearchStage.DISCOVERY, include_header=False
        )
        output.append(ideas_content)
        output.append("\n")

        # ranking.md
        ranking_content = self._show_file_content(
            paper_id, version, "ranking.md",
            "", ResearchStage.DISCOVERY, include_header=False
        )
        output.append(ranking_content)
        output.append("\n")

        # conditions.md
        conditions_content = self._show_file_content(
            paper_id, version, "conditions.md",
            "条件验证", ResearchStage.DISCOVERY, include_header=True
        )
        output.append(conditions_content)

        return "\n".join(output)

    def show_plan(self, paper_id: str, version: str = "v1") -> str:
        """查看研究计划"""
        output = []

        # initial_plan.md
        initial_plan = self._show_file_content(
            paper_id, version, "initial_plan.md",
            "初步研究计划", ResearchStage.DISCOVERY, include_header=True
        )
        output.append(initial_plan)
        output.append("\n")

        # research_plan.md
        research_plan = self._show_file_content(
            paper_id, version, "research_plan.md",
            "最终研究计划", ResearchStage.EXECUTION, include_header=True
        )
        output.append(research_plan)

        return "\n".join(output)

    def show_code(self, paper_id: str, version: str = "v1") -> str:
        """查看代码结构和执行顺序"""
        version_dir = self.base_dir / paper_id / version
        code_dir = version_dir / "code"

        if not code_dir.exists():
            return f"错误: {code_dir} 不存在"

        output = []
        output.append("=" * 80)
        output.append(f"代码结构: {paper_id}/{version}/code/")
        output.append("=" * 80)
        output.append("")

        # 获取所有代码文件
        code_files = sorted([f for f in code_dir.glob("*.R") or code_dir.glob("*.py") or code_dir.glob("*.do")])

        if not code_files:
            code_files = list(code_dir.glob("*.*"))
            code_files = sorted(code_files, key=lambda x: x.name)

        for i, code_file in enumerate(code_files, 1):
            output.append(f"{i}. {code_file.name}")
            output.append(f"   路径: {code_file}")
            if code_file.stat().st_size < 5000:  # 小文件直接显示内容
                try:
                    content = code_file.read_text(encoding="utf-8", errors="ignore")
                    lines = content.split("\n")[:20]  # 只显示前20行
                    for line in lines:
                        output.append(f"   {line}")
                    if len(content.split("\n")) > 20:
                        output.append(f"   ... (共 {len(content.split(chr(10)))} 行)")
                except:
                    output.append("   (无法读取内容)")
            output.append("")

        output.append("=" * 80)

        return "\n".join(output)

    def show_paper(self, paper_id: str, version: str = "v1") -> str:
        """生成论文摘要"""
        output = []

        # PROMPT.md
        prompt_content = self._show_file_content(
            paper_id, version, "PROMPT.md",
            "论文生成提示词", ResearchStage.PAPER_WRITING, include_header=True
        )
        output.append(prompt_content)
        output.append("\n")

        # paper.tex (只显示结构)
        version_dir = self.base_dir / paper_id / version
        tex_file = version_dir / "paper.tex"

        if tex_file.exists():
            output.append("=" * 80)
            output.append(f"LaTeX 源码结构: {paper_id}/{version}/paper.tex")
            output.append("=" * 80)
            output.append("")

            try:
                content = tex_file.read_text(encoding="utf-8", errors="ignore")
                # 提取章节结构
                lines = content.split("\n")
                for line in lines:
                    line = line.strip()
                    if line.startswith("\\section{") or line.startswith("\\subsection{"):
                        output.append(f"  {line}")
            except:
                output.append("  (无法读取 LaTeX 结构)")

        return "\n".join(output)

    def show_review(self, paper_id: str, version: str = "v1") -> str:
        """查看评审意见"""
        output = []

        # 外部评审文件
        review_files = [
            ("review_gpt_1.md", "GPT 评审"),
            ("review_gemini_1.md", "Gemini 评审"),
            ("review_grok_1.md", "Grok 评审"),
            ("reply_to_reviewers_1.md", "回应评审意见"),
        ]

        for filename, title in review_files:
            content = self._show_file_content(
                paper_id, version, filename,
                title, ResearchStage.EXTERNAL_REVIEW, include_header=True
            )
            output.append(content)
            output.append("\n")

        return "\n".join(output)

    def compare_versions(self, paper_id: str, v1: str, v2: str) -> str:
        """对比版本差异"""
        dir1 = self.base_dir / paper_id / v1
        dir2 = self.base_dir / paper_id / v2

        if not dir1.exists():
            return f"错误: {dir1} 不存在"
        if not dir2.exists():
            return f"错误: {dir2} 不存在"

        output = []
        output.append("=" * 80)
        output.append(f"版本对比: {paper_id}")
        output.append(f"版本 A: {v1}")
        output.append(f"版本 B: {v2}")
        output.append("=" * 80)
        output.append("")

        # 获取两个版本的文件列表
        files1 = {f.name: f for f in dir1.glob("*") if f.is_file()}
        files2 = {f.name: f for f in dir2.glob("*") if f.is_file()}

        all_files = set(files1.keys()) | set(files2.keys())

        for filename in sorted(all_files):
            in_v1 = filename in files1
            in_v2 = filename in files2

            if in_v1 and in_v2:
                # 文件都存在，检查是否修改
                size1 = files1[filename].stat().st_size
                size2 = files2[filename].stat().st_size
                if size1 == size2:
                    output.append(f"  = {filename} (未变化)")
                else:
                    output.append(f"  ~ {filename} (已修改: {size1} → {size2} 字节)")
            elif in_v1:
                output.append(f"  - {filename} (仅在 {v1} 中)")
            else:
                output.append(f"  + {filename} (仅在 {v2} 中)")

        output.append("")
        output.append("图例:")
        output.append("  =  文件未变化")
        output.append("  ~  文件已修改")
        output.append("  -  文件仅在版本 A 中")
        output.append("  +  文件仅在版本 B 中")
        output.append("")
        output.append("=" * 80)

        return "\n".join(output)

    def extract_prompt_template(self, paper_id: str = "apep_0185", version: str = "v1") -> str:
        """提取 AI 提示词模板"""
        version_dir = self.base_dir / paper_id / version

        templates = {}
        templates_to_extract = {
            "initialization.md": "init_template.md",
            "ideas.md": "idea_prompt.md",
            "research_plan.md": "plan_prompt.md",
        }

        output = ["提取 AI 提示词模板...", ""]

        for source, target in templates_to_extract.items():
            source_path = version_dir / source
            if source_path.exists():
                # 复制到模板目录
                target_path = self.templates_dir / target
                try:
                    content = source_path.read_text(encoding="utf-8", errors="ignore")
                    target_path.write_text(content, encoding="utf-8")
                    templates[target] = True
                    output.append(f"  ✓ {target} ({source})")
                except Exception as e:
                    templates[target] = False
                    output.append(f"  ✗ {target} - {e}")
            else:
                templates[target] = False
                output.append(f"  ✗ {target} ({source} 不存在)")

        # 尝试提取 PROMPT.md
        prompt_path = version_dir / "PROMPT.md"
        if prompt_path.exists():
            try:
                content = prompt_path.read_text(encoding="utf-8", errors="ignore")
                self.templates_dir.mkdir(exist_ok=True)
                (self.templates_dir / "paper_prompt.md").write_text(content, encoding="utf-8")
                output.append(f"  ✓ paper_prompt.md (PROMPT.md)")
            except Exception as e:
                output.append(f"  ✗ paper_prompt.md - {e}")

        output.append("")
        output.append(f"模板输出目录: {self.templates_dir}")
        output.append("")

        return "\n".join(output)

    def _show_file_content(
        self,
        paper_id: str,
        version: str,
        filename: str,
        title: str,
        stage: ResearchStage,
        include_header: bool = True
    ) -> str:
        """显示文件内容"""
        file_path = self.base_dir / paper_id / version / filename

        output = []

        if include_header:
            output.append("=" * 80)
            output.append(f"论文: {paper_id}")
            output.append(f"版本: {version}")
            output.append(f"阶段: {stage.value}")
            output.append(f"文件: {filename}")
            output.append("=" * 80)
            output.append("")

        if not file_path.exists():
            output.append(f"错误: {file_path} 不存在")
            return "\n".join(output)

        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            output.append(content)
        except Exception as e:
            output.append(f"错误: 无法读取文件 - {e}")

        if include_header:
            output.append("")
            output.append("=" * 80)

        return "\n".join(output)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="APE (Autonomous Policy Evaluation) 论文浏览器 - AI 辅助经济学研究学习系统",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s apep_0185 --flow           展示完整研究流程
  %(prog)s apep_0185 --init           查看初始化配置
  %(prog)s apep_0185 --ideas          浏览研究想法
  %(prog)s apep_0185 --plan           查看研究计划
  %(prog)s apep_0185 --code           查看代码结构
  %(prog)s apep_0185 --paper          生成论文摘要
  %(prog)s apep_0185 --review         查看评审意见
  %(prog)s apep_0185 --compare v1 v16 对比版本差异
  %(prog)s --list                    列出所有论文

学习路径（建议按顺序学习 apep_0185）:
  1. 初始化阶段: --init
  2. 想法生成阶段: --ideas
  3. 研究设计阶段: --plan
  4. 数据分析阶段: --code
  5. 论文写作阶段: --paper
  6. 评审迭代阶段: --review
  7. 版本对比: --compare v1 v16

相关论文推荐:
  - apep_0185: 网络溢出、shift-share ★★★★（网络+区域）
  - apep_0001: 州政策 DiD ★★★（劳动经济学）
  - apep_0135: 政策扩散 ★★★（国际贸易/政策传播）

作者: 凌贵旺 (南京农业大学经济管理学院)
邮箱: lingguiwang@yeah.net
        """
    )

    parser.add_argument("paper_id", nargs="?", help="论文 ID (如 'apep_0185')")
    parser.add_argument("--version", "-v", default="v1", help="版本号 (默认: v1)")
    parser.add_argument("--init", action="store_true", help="查看初始化配置")
    parser.add_argument("--ideas", action="store_true", help="浏览研究想法和排序")
    parser.add_argument("--plan", action="store_true", help="查看研究计划")
    parser.add_argument("--code", action="store_true", help="查看代码结构")
    parser.add_argument("--paper", action="store_true", help="生成论文摘要")
    parser.add_argument("--review", action="store_true", help="查看评审意见")
    parser.add_argument("--flow", action="store_true", help="展示完整研究流程")
    parser.add_argument("--compare", nargs=2, metavar=("V1", "V2"), help="对比两个版本")
    parser.add_argument("--extract", action="store_true", help="提取 AI 提示词模板")
    parser.add_argument("--list", action="store_true", help="列出所有可用论文")
    parser.add_argument("--base-dir", help="指定 ape-papers 仓库目录")

    args = parser.parse_args()

    # 确定基础目录
    if args.base_dir:
        base_dir = Path(args.base_dir)
    else:
        # 脚本在 my_workspace/scripts/ 下，向上两级到仓库根目录
        base_dir = Path(__file__).parent.parent.parent.resolve()

    explorer = PaperExplorer(base_dir)

    # 列出所有论文
    if args.list:
        papers = explorer.list_papers()
        print("=" * 80)
        print("APE 论文仓库 - 可用论文列表")
        print("=" * 80)
        print(f"共 {len(papers)} 篇论文")
        print("")
        for paper in papers:
            versions = explorer.get_versions(paper.name)
            print(f"  {paper.name} ({len(versions)} 个版本: {', '.join(versions)})")
        print("")
        print(f"仓库路径: {base_dir}")
        print("=" * 80)
        return 0

    # 验证论文 ID
    if not args.paper_id:
        parser.print_help()
        return 1

    # 提取提示词模板
    if args.extract:
        result = explorer.extract_prompt_template(args.paper_id, args.version)
        print(result)
        return 0

    # 对比版本
    if args.compare:
        result = explorer.compare_versions(args.paper_id, args.compare[0], args.compare[1])
        print(result)
        return 0

    # 其他命令
    result = ""

    if args.flow:
        result = explorer.show_flow(args.paper_id, args.version)
    elif args.init:
        result = explorer.show_init(args.paper_id, args.version)
    elif args.ideas:
        result = explorer.show_ideas(args.paper_id, args.version)
    elif args.plan:
        result = explorer.show_plan(args.paper_id, args.version)
    elif args.code:
        result = explorer.show_code(args.paper_id, args.version)
    elif args.paper:
        result = explorer.show_paper(args.paper_id, args.version)
    elif args.review:
        result = explorer.show_review(args.paper_id, args.version)
    else:
        # 默认展示流程
        result = explorer.show_flow(args.paper_id, args.version)

    print(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
