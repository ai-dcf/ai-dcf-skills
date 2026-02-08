#!/usr/bin/env python3
"""
Prompt Generator Module
用于生成优化的信息图提示词
"""

from pathlib import Path
import re


class PromptGenerator:
    """提示词生成器"""

    def __init__(self, templates_dir):
        """
        初始化生成器

        Args:
            templates_dir: 模板目录路径
        """
        self.templates_dir = Path(templates_dir)
        self.styles = {
            "default": "style-default.md",
            "chalkboard": "style-chalkboard.md",
            "vintage": "style-vintage.md",
        }
        # 人物信息图关键词
        self.character_keywords = {
            # 角色相关
            "角色", "人物", "人设", "角色设定", "设定", "头像",
            # 属性相关
            "属性", "特征", "特点", "性格", "个性", "脾气",
            # 人际关系
            "人际", "关系", "宿敌", "对手", "伙伴", "搭档", "羁绊", "朋友",
            # 装备/物品
            "装备", "物品", "道具", "武器", "宝物", "秘宝",
            # 情绪表情
            "表情", "情绪", "心情", "情感",
            # 档案相关
            "档案", "档案卡", "名片", "简历", "通缉令", "身份",
            # 游戏/动画相关
            "游戏角色", "动画角色", "卡通", "虚拟", "漫画",
            # 角色描述方式
            "我想设计", "角色介绍", "人物介绍", "角色卡", "角色资料",
        }

    def load_template(self, filename):
        """加载模板文件"""
        template_path = self.templates_dir / filename
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()

    def detect_character_infographic(self, topic, audience=None, key_point=None):
        """
        自动检测是否为人物信息图

        Args:
            topic: 信息图主题
            audience: 受众（可选）
            key_point: 关键点（可选）

        Returns:
            bool: 是否为人物信息图
        """
        # 组合所有输入文本
        combined_text = " ".join(filter(None, [topic, audience, key_point])).lower()

        # 关键词匹配
        keyword_count = 0
        for keyword in self.character_keywords:
            if keyword.lower() in combined_text:
                keyword_count += 1

        # 如果包含3个或以上的相关关键词，或包含特定的高权重关键词
        high_weight_keywords = {"角色设定", "人物设定", "角色卡", "角色资料", "人物介绍", "角色介绍"}
        has_high_weight = any(kw.lower() in combined_text for kw in high_weight_keywords)

        is_character = keyword_count >= 3 or has_high_weight

        return is_character

    def get_style_block(self, style_key):
        """获取风格描述块"""
        if style_key not in self.styles:
            raise ValueError(f"Unknown style: {style_key}")

        template_file = self.styles[style_key]
        return self.load_template(template_file)

    def analyze_content_complexity(self, topic, audience=None, key_point=None):
        """
        分析内容的复杂度和信息量

        Args:
            topic: 主题
            audience: 受众（可选）
            key_point: 关键点（可选）

        Returns:
            dict: 包含以下信息
                - complexity: 复杂度等级 (simple/medium/complex)
                - info_density: 信息密度 (low/medium/high)
                - suggested_points: 建议的主要内容点数量 (2-8)
                - needs_conclusion: 是否需要结论部分
                - conclusion_type: 结论类型 (cta/summary/insight/none)
                - content_depth: 内容深度 (shallow/medium/deep)
        """
        combined_text = " ".join(filter(None, [topic, audience, key_point]))

        # 计算文本长度
        text_length = len(combined_text)

        # 计算内容点的数量指示
        # 检查用户是否明确指定了数量（如"5大"、"3种"等）
        import re
        number_pattern = r'(\d+)[个种大类点条|]'
        explicit_numbers = re.findall(number_pattern, combined_text)

        # 分析主题的复杂度
        complex_indicators = ["系统", "分析", "研究", "框架", "模型", "体系", "策略", "方案", "生态"]
        simple_indicators = ["是什么", "怎样", "基础", "入门", "初级", "简介"]

        complexity_score = 0
        for indicator in complex_indicators:
            complexity_score += combined_text.count(indicator)
        for indicator in simple_indicators:
            complexity_score -= combined_text.count(indicator)

        # 分析信息密度
        # 通过关键词数量估计
        info_keywords = ["和", "或", "包括", "特点", "特征", "优点", "缺点", "类型", "分类", "分层"]
        info_density_score = sum(combined_text.count(kw) for kw in info_keywords)

        # 判定复杂度级别
        if complexity_score >= 3:
            complexity = "complex"
        elif complexity_score >= 1:
            complexity = "medium"
        else:
            complexity = "simple"

        # 判定信息密度
        if info_density_score >= 5:
            info_density = "high"
        elif info_density_score >= 2:
            info_density = "medium"
        else:
            info_density = "low"

        # 根据文本长度和复杂度推荐内容点数
        if explicit_numbers:
            suggested_points = min(int(explicit_numbers[0]), 8)  # 最多8个
        else:
            if complexity == "complex" and info_density == "high":
                suggested_points = 6  # 复杂且信息密集：6个点
            elif complexity == "complex":
                suggested_points = 5  # 复杂但信息一般：5个点
            elif complexity == "medium":
                suggested_points = 4  # 中等：4个点
            else:
                suggested_points = 3  # 简单：3个点

            # 根据文本长度调整
            if text_length > 80:
                suggested_points = min(suggested_points + 1, 8)
            elif text_length < 20:
                suggested_points = max(suggested_points - 1, 2)

        # 判断是否需要结论
        # 检查用户是否提到了行动、决策、建议等
        cta_keywords = ["应该", "建议", "需要", "要", "行动", "做法", "方案", "对策", "改进"]
        summary_keywords = ["总结", "总体", "整体", "概括", "综合", "结论"]

        needs_cta = any(kw in combined_text for kw in cta_keywords)
        needs_summary = any(kw in combined_text for kw in summary_keywords)

        if key_point:
            # 如果用户已提供关键点，通常需要结论
            needs_conclusion = True
            if needs_cta:
                conclusion_type = "cta"  # 行动号召
            elif needs_summary:
                conclusion_type = "summary"  # 总结
            else:
                conclusion_type = "insight"  # 洞察
        elif needs_cta:
            needs_conclusion = True
            conclusion_type = "cta"
        elif complexity == "complex":
            # 复杂内容通常需要总结
            needs_conclusion = True
            conclusion_type = "summary"
        else:
            # 简单内容可能不需要结论
            needs_conclusion = False
            conclusion_type = "none"

        # 判定内容深度
        if complexity == "complex" and text_length > 60:
            content_depth = "deep"
        elif complexity == "complex" or info_density == "high":
            content_depth = "medium"
        else:
            content_depth = "shallow"

        return {
            "complexity": complexity,
            "info_density": info_density,
            "suggested_points": suggested_points,
            "needs_conclusion": needs_conclusion,
            "conclusion_type": conclusion_type,
            "content_depth": content_depth,
            "text_length": text_length,
        }

    def detect_content_type(self, topic):
        """
        根据主题关键词检测内容类型

        Returns:
            str: 内容类型 (flow/comparison/list/timeline/general)
        """
        topic_lower = topic.lower()

        flow_keywords = ["流程", "步骤", "阶段", "周期", "漏斗", "管道", "过程", "流", "阶级"]
        if any(word in topic_lower for word in flow_keywords):
            return "flow"

        comparison_keywords = ["对比", "区别", "差异", "对抗", "vs", "vs.", "对", "相比"]
        if any(word in topic_lower for word in comparison_keywords):
            return "comparison"

        list_keywords = ["列表", "清单", "要点", "类型", "风险", "优势", "特点", "特征", "种", "个"]
        if any(word in topic_lower for word in list_keywords):
            return "list"

        timeline_keywords = ["时间", "历史", "演变", "发展", "里程碑", "进化", "时代", "年代"]
        if any(word in topic_lower for word in timeline_keywords):
            return "timeline"

        return "general"

    def generate_content_structure(self, topic, content_type=None, audience=None, key_point=None):
        """
        根据主题、内容类型和复杂度分析生成内容结构描述

        Args:
            topic: 信息图主题
            content_type: 内容类型（如果为None则自动检测）
            audience: 受众（可选，用于分析）
            key_point: 关键点（可选，用于分析）

        Returns:
            str: 内容结构描述
        """
        if content_type is None:
            content_type = self.detect_content_type(topic)

        # 分析内容复杂度
        analysis = self.analyze_content_complexity(topic, audience, key_point)

        structures = {
            "flow": self._structure_flow(topic, analysis),
            "comparison": self._structure_comparison(topic, analysis),
            "list": self._structure_list(topic, analysis),
            "timeline": self._structure_timeline(topic, analysis),
            "general": self._structure_general(topic, analysis),
        }

        return structures.get(content_type, structures["general"])

    def _structure_flow(self, topic, analysis):
        """流程型结构 - 根据复杂度动态生成"""
        num_stages = analysis["suggested_points"]
        depth = analysis["content_depth"]

        structure = f"Use a vertical or horizontal flow diagram:\n\n"
        structure += f"1. Define {num_stages} stages/steps (from start to end)\n"
        structure += f"2. Connect stages with clear arrows showing direction\n"

        if depth == "deep":
            structure += f"3. Each stage: title + 2-3 key points describing the action\n"
            structure += f"4. Show metrics, duration, or outcomes for each stage\n"
            structure += f"5. Include decision points or branching if applicable\n"
        else:
            structure += f"3. Each stage: title + 1-2 short descriptive sentences\n"
            structure += f"4. Optional: show key metrics or outcomes\n"
            structure += f"5. Maintain clear flow direction\n"

        structure += f"6. Use consistent visual spacing and alignment\n"
        return structure

    def _structure_comparison(self, topic, analysis):
        """对比型结构 - 根据复杂度动态生成"""
        depth = analysis["content_depth"]
        info_density = analysis["info_density"]

        structure = "Use a left-right or top-bottom comparison layout:\n\n"
        structure += "1. Create two clearly distinct sections/columns\n"

        if info_density == "high":
            structure += "2. Each side: title + 4-5 detailed comparison points\n"
        else:
            structure += "2. Each side: title + 2-3 comparison points\n"

        structure += "3. Use contrasting visual elements (colors, icons, styles)\n"

        if depth == "deep":
            structure += "4. Add summary indicators (checkmarks, ratings, or performance metrics)\n"
        else:
            structure += "4. Optional: add simple visual indicators (checkmarks, icons)\n"

        structure += "5. Ensure very clear visual separation between items\n"
        return structure

    def _structure_list(self, topic, analysis):
        """列表/卡片型结构 - 根据复杂度动态生成"""
        num_cards = analysis["suggested_points"]
        depth = analysis["content_depth"]

        structure = f"Use a card-based or grid layout:\n\n"
        structure += f"1. Create {num_cards} distinct cards or sections\n"

        if depth == "deep":
            structure += f"2. Each card: title (bold) + 2-3 detailed bullet points\n"
            structure += f"3. Include icons, numbers, or visual indicators for each card\n"
        else:
            structure += f"2. Each card: title (bold) + 1-2 short sentences\n"
            structure += f"3. Optional: add icons or numbers for visual hierarchy\n"

        structure += f"4. Use consistent card styling, borders, and spacing\n"
        structure += f"5. Arrange cards in balanced rows/columns with adequate spacing\n"
        return structure

    def _structure_timeline(self, topic, analysis):
        """时间线型结构 - 根据复杂度动态生成"""
        num_milestones = analysis["suggested_points"]

        structure = f"Use a horizontal or vertical timeline:\n\n"
        structure += f"1. Display {num_milestones} key milestones/periods/events\n"
        structure += f"2. Each milestone: year/era/phase + clear label and brief description\n"
        structure += f"3. Use connecting line with clear visual markers for each point\n"
        structure += f"4. Add small icons or visual indicators for each period if relevant\n"
        structure += f"5. Show clear progression from past to present (or future)\n"
        return structure

    def _structure_general(self, topic, analysis):
        """通用型结构 - 根据复杂度动态生成"""
        num_points = analysis["suggested_points"]
        depth = analysis["content_depth"]

        structure = f"Use a balanced, hierarchical layout:\n\n"
        structure += f"1. Central concept or main title prominently displayed\n"
        structure += f"2. {num_points} supporting points arranged around central concept\n"

        if depth == "deep":
            structure += f"3. Each point: title + 1-2 explanatory sentences or details\n"
        else:
            structure += f"3. Each point: title + brief 1-sentence description\n"

        structure += f"4. Use consistent spacing and clear visual hierarchy\n"
        structure += f"5. Include connecting elements (lines, arrows) to show relationships\n"
        return structure

    def generate(self, topic, style, audience=None, key_point=None, include_base_template=False):
        """
        生成完整提示词
        自动检测是否为人物信息图并选择合适的模板

        Args:
            topic: 信息图主题
            style: 风格 (default/chalkboard/vintage)
            audience: 受众（可选）
            key_point: 关键点/行动号召（可选）
            include_base_template: 是否包含基础模板注释

        Returns:
            str: 完整的提示词
        """
        # 自动检测是否为人物信息图
        is_character = self.detect_character_infographic(topic, audience, key_point)

        if is_character:
            # 人物信息图生成逻辑
            parts = []

            # 1. 画幅与标题
            parts.append("# Character Infographic Generation Prompt\n")
            parts.append("Create a 16:9 landscape character infographic image\n\n")

            # 2. 标题部分
            parts.append("## Title Section\n")
            parts.append(f"**Title (large, bold):** {topic} 角色设定卡\n")

            if key_point:
                parts.append(f"**Subtitle (small):** {key_point}\n")

            if audience:
                parts.append(f"**Target Audience:** {audience}\n")

            parts.append("\n")

            # 3. 人物信息图的标准结构
            parts.append("## Layout Structure\n")
            parts.append("- **Center Block**: Main character portrait in decorative frame\n")
            parts.append("- **Top Block**: 3-4 emotion/expression variations displayed horizontally\n")
            parts.append("- **Left Column**: Personal information/attributes section with title\n")
            parts.append("- **Right Column**: Key relationships and companion characters\n")
            parts.append("- **Bottom Block**: Signature items/equipment display\n")
            parts.append("\n")

            # 4. 风格描述
            parts.append("## Style Requirements\n")
            style_block = self.get_style_block(style)
            parts.append(style_block)
            parts.append("\n\n")

            # 5. 强制约束
            parts.append("## Strict Constraints\n")
            parts.append("- **Language**: Chinese characters must be clear, readable, and large\n")
            parts.append("- **Organization**: Each section must have clear visual boundaries\n")
            parts.append("- **Content**: Do NOT add any text beyond what is specified above\n")
            parts.append("- **Layout**: Abundant whitespace, clear section separation, balanced composition\n")
            parts.append("- **Quality**: No cluttered backgrounds, no random characters or watermarks\n")
            parts.append("- **Readability**: All character information must be easily comprehensible at a glance\n")

            full_prompt = "".join(parts)
            return full_prompt

        else:
            # 原有的通用信息图生成逻辑
            parts = []

            # 1. 画幅与标题
            parts.append("# Infographic Generation Prompt\n")
            parts.append("Create a 16:9 landscape infographic image\n\n")

            # 2. 标题部分
            parts.append("## Title Section\n")
            parts.append(f"**Title (large, bold, centered):** {topic}\n")

            if key_point:
                parts.append(f"**Subtitle (small, informative):** {key_point}\n")

            if audience:
                parts.append(f"**Target Audience:** {audience}\n")

            parts.append("\n")

            # 3. 分析内容复杂度
            analysis = self.analyze_content_complexity(topic, audience, key_point)

            # 4. 主体内容结构
            parts.append("## Main Content Structure\n")
            content_type = self.detect_content_type(topic)
            content_structure = self.generate_content_structure(topic, content_type, audience, key_point)
            parts.append(content_structure)
            parts.append("\n\n")

            # 5. 根据分析结果添加结论部分指导
            if analysis["needs_conclusion"]:
                parts.append("## Conclusion/Call-to-Action Section\n")
                conclusion_type = analysis["conclusion_type"]

                if conclusion_type == "cta":
                    parts.append("Include a clear action-oriented conclusion that guides viewers toward a decision or next step.\n")
                    parts.append("Format: 1-2 powerful, actionable sentences at the bottom.\n\n")
                elif conclusion_type == "summary":
                    parts.append("Include a summary that synthesizes the main points and reinforces the core message.\n")
                    parts.append("Format: 1-2 impactful sentences that capture the essence.\n\n")
                elif conclusion_type == "insight":
                    parts.append("Include a memorable insight or key takeaway for the viewer.\n")
                    parts.append("Format: 1 concise, thought-provoking sentence.\n\n")

            # 6. 风格描述
            parts.append("## Style Requirements\n")
            style_block = self.get_style_block(style)
            parts.append(style_block)
            parts.append("\n\n")

            # 7. 强制约束
            parts.append("## Strict Constraints\n")
            parts.append("- **Language**: Chinese characters must be clear, readable, and large\n")
            parts.append("- **Content**: Do NOT add any text beyond what is specified above\n")
            parts.append("- **Layout**: Abundant whitespace, clear alignment, balanced composition\n")
            parts.append("- **Quality**: No cluttered backgrounds, no random characters or watermarks\n")
            parts.append("- **Accessibility**: High contrast, easy to read from a distance\n")
            parts.append(f"- **Information Density**: Optimized for {analysis['info_density']} information density\n")
            parts.append(f"- **Complexity Level**: Designed for {analysis['complexity']} content\n")

            full_prompt = "".join(parts)
            return full_prompt

    def generate_character_compact(self, topic, style, audience=None, key_point=None):
        """
        生成人物信息图的简洁版提示词

        Args:
            topic: 信息图主题（通常是角色名或角色相关描述）
            style: 风格
            audience: 受众（可选）
            key_point: 关键点（可选）

        Returns:
            str: 紧凑的人物信息图提示词
        """
        parts = []
        parts.append(f"Create a 16:9 landscape character infographic image\n\n")

        # 标题
        parts.append(f"**Title (large, bold):** {topic} 角色设定卡\n")
        if key_point:
            parts.append(f"**Subtitle:** {key_point}\n")

        parts.append("\n")

        # 人物信息图的标准布局
        parts.append("**Layout Structure:**\n")
        parts.append("- Center: Main character portrait in decorative frame\n")
        parts.append("- Top: 3-4 emotion/expression variations\n")
        parts.append("- Left: Personal information/attributes section\n")
        parts.append("- Right: Key relationships/companion characters\n")
        parts.append("- Bottom: Signature items/equipment display\n")
        parts.append("\n")

        # 风格
        style_block = self.get_style_block(style)
        parts.append(f"**Style:**\n{style_block}\n\n")

        # 约束
        parts.append("**Constraints:**\n")
        parts.append("- Chinese text must be clear, large, highly readable\n")
        parts.append("- All information must be clearly organized in designated sections\n")
        parts.append("- Do NOT add any extra text beyond specified content\n")
        parts.append("- Abundant whitespace, clear visual boundaries between sections\n")
        parts.append("- No watermarks, no signatures\n")

        return "".join(parts)

    def generate_compact(self, topic, style, audience=None, key_point=None):
        """
        生成简洁版提示词（单个代码块，便于复制）
        自动检测是否为人物信息图并选择合适的模板
        根据内容复杂度动态生成提示词

        Args:
            topic: 信息图主题
            style: 风格
            audience: 受众（可选）
            key_point: 关键点（可选）

        Returns:
            str: 紧凑的提示词（适合直接复制到出图工具）
        """
        # 自动检测是否为人物信息图
        is_character = self.detect_character_infographic(topic, audience, key_point)

        if is_character:
            return self.generate_character_compact(topic, style, audience, key_point)
        else:
            # 通用信息图生成逻辑（支持智能信息量分析）
            parts = []
            parts.append(f"Create a 16:9 landscape infographic image\n\n")

            # 标题
            parts.append(f"**Title (large, bold, centered):** {topic}\n")
            if key_point:
                parts.append(f"**Subtitle:** {key_point}\n")

            parts.append("\n")

            # 分析内容复杂度并生成内容结构
            analysis = self.analyze_content_complexity(topic, audience, key_point)
            content_structure = self.generate_content_structure(topic, audience=audience, key_point=key_point)
            parts.append("**Main Content:**\n")
            parts.append(content_structure)
            parts.append("\n")

            # 根据分析结果动态添加结论部分
            if analysis["needs_conclusion"]:
                parts.append("\n**Conclusion/Call-to-Action:**\n")
                conclusion_type = analysis["conclusion_type"]

                if conclusion_type == "cta":
                    parts.append("- Provide actionable recommendation or next steps\n")
                    parts.append("- Format: 1 clear, concise sentence\n")
                elif conclusion_type == "summary":
                    parts.append("- Summarize the key insights or main takeaway\n")
                    parts.append("- Format: 1 impactful sentence highlighting the core message\n")
                elif conclusion_type == "insight":
                    parts.append("- Share a key insight or thought to remember\n")
                    parts.append("- Format: 1 memorable sentence\n")

                parts.append("\n")

            # 风格
            style_block = self.get_style_block(style)
            parts.append(f"**Style:**\n{style_block}\n\n")

            # 约束
            parts.append("**Constraints:**\n")
            parts.append("- Chinese text must be clear, large, no clutter\n")
            parts.append("- Do NOT add any extra text beyond specified content\n")
            parts.append("- Abundant whitespace, clear alignment\n")
            parts.append("- No watermarks, no signatures\n")
            parts.append("- Information density should match the suggested content points\n")

            return "".join(parts)


def main():
    """测试"""
    from pathlib import Path

    script_dir = Path(__file__).parent
    templates_dir = script_dir.parent / "templates"

    generator = PromptGenerator(templates_dir)

    # 测试用例
    topic = "AI 的 5 大风险"
    style = "default"
    audience = "小白"
    key_point = "了解风险，更好地拥抱 AI"

    print("="*60)
    print("Compact Prompt:")
    print("="*60)
    compact = generator.generate_compact(topic, style, audience, key_point)
    print(compact)

    print("\n" + "="*60)
    print("Full Prompt:")
    print("="*60)
    full = generator.generate(topic, style, audience, key_point)
    print(full)


if __name__ == "__main__":
    main()
