#!/usr/bin/env python3
"""
Infographic Skill - Main Orchestrator
用于驱动整个信息图生成流程的主脚本
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime

class InfographicOrchestrator:
    """信息图生成的主控流程"""

    def __init__(self):
        self.skill_dir = Path(__file__).parent
        self.stages_dir = self.skill_dir / "stages"
        self.templates_dir = self.skill_dir / "templates"
        self.output_dir = self.skill_dir / "output"
        self.output_dir.mkdir(exist_ok=True)

        # 当前会话的状态
        self.session = {
            "timestamp": datetime.now().isoformat(),
            "topic": None,
            "audience": None,
            "key_point": None,
            "style": None,
            "prompt": None,
            "generation_method": None,
            "template_type": None,  # 记录使用的模板类型
        }

        # 风格映射
        self.styles = {
            "default": "默认风格",
            "chalkboard": "手绘黑板报风格",
            "vintage": "复古怀旧风格",
        }

    def load_stage(self, stage_num):
        """加载指定阶段的文档"""
        stage_file = self.stages_dir / f"0{stage_num}-{self._get_stage_name(stage_num)}.md"
        if stage_file.exists():
            with open(stage_file, 'r', encoding='utf-8') as f:
                return f.read()
        return None

    def _get_stage_name(self, stage_num):
        """获取阶段名称"""
        stage_names = {
            1: "topic",
            2: "style",
            3: "prompt",
            4: "generate",
        }
        return stage_names.get(stage_num, "unknown")

    def _create_prompt_generator(self):
        """创建 PromptGenerator 实例"""
        from prompt_generator import PromptGenerator
        return PromptGenerator(self.templates_dir)

    def generate_prompt(self, topic, style, audience=None, key_point=None):
        """
        根据主题、风格生成提示词
        自动检测是否为人物信息图并选择合适的模板

        Args:
            topic: 信息图主题
            style: 选定的风格 (default/chalkboard/vintage)
            audience: 受众（可选）
            key_point: 关键点（可选）

        Returns:
            str: 优化的提示词
        """
        # 使用 PromptGenerator 生成提示词（自动包含人物信息图检测）
        try:
            prompt_generator = self._create_prompt_generator()
            prompt = prompt_generator.generate_compact(topic, style, audience, key_point)
            return prompt
        except Exception as e:
            print(f"❌ 提示词生成失败：{e}")
            return None

    def save_session(self):
        """保存当前会话到 JSON"""
        output_file = self.output_dir / f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.session, f, ensure_ascii=False, indent=2)
        return str(output_file)

    def generate_jsonl_request(self, prompt, request_id="01"):
        """
        生成 APIMart API 请求格式 (JSONL)
        """
        request = {
            "id": request_id,
            "prompt": prompt,
            "size": "16:9",
            "n": 1,
            "resolution": "2K",
            "model": "gemini-3-pro-image-preview",
            "pad_url": ""
        }
        return json.dumps(request, ensure_ascii=False)

    def run_stage_1_topic_input(self):
        """阶段1：主题输入"""
        print("\n" + "="*60)
        print("🎨 信息图生成器 - 阶段 1：主题输入")
        print("="*60)

        topic = input("\n请输入信息图主题（例如：'AI的5大风险'）：").strip()
        if not topic:
            print("❌ 主题不能为空")
            return False

        self.session["topic"] = topic

        # 可选：受众
        audience = input("\n（可选）针对谁看？（例如：小白/从业者/老板）：").strip()
        if audience:
            self.session["audience"] = audience

        # 可选：关键点
        key_point = input("\n（可选）希望读者记住什么？：").strip()
        if key_point:
            self.session["key_point"] = key_point

        # 复述确认
        print("\n✅ 已确认主题：")
        print(f"   主题：{topic}")
        if audience:
            print(f"   受众：{audience}")
        if key_point:
            print(f"   重点：{key_point}")

        return True

    def run_stage_2_style_selection(self):
        """阶段2：风格选择"""
        print("\n" + "="*60)
        print("🎨 信息图生成器 - 阶段 2：风格选择")
        print("="*60)

        print("\n请选择信息图风格：\n")
        print("1️⃣  默认风格")
        print("    特点：奶油纸纹 + 彩铅线稿 + 淡水彩、暖色调")
        print("    适用：通用、商务、教育\n")

        print("2️⃣  手绘黑板报风格")
        print("    特点：黑板/粉笔画、手绘感强、朋克风")
        print("    适用：教程、创意、年轻化\n")

        print("3️⃣  复古怀旧风格")
        print("    特点：老报纸纹理、70-90年代杂志风")
        print("    适用：历史、文化、复古主题\n")

        choice = input("请输入选择（1/2/3，默认为1）：").strip() or "1"

        style_map = {
            "1": "default",
            "2": "chalkboard",
            "3": "vintage",
        }

        if choice not in style_map:
            print("❌ 选择无效，使用默认风格")
            choice = "1"

        style_key = style_map[choice]
        style_name = self.styles[style_key]
        self.session["style"] = style_key

        print(f"\n✅ 已选择：{style_name}")
        return True

    def run_stage_3_prompt_generation(self):
        """阶段3：提示词生成"""
        print("\n" + "="*60)
        print("🎨 信息图生成器 - 阶段 3：提示词生成")
        print("="*60)

        topic = self.session["topic"]
        style = self.session["style"]
        audience = self.session.get("audience")
        key_point = self.session.get("key_point")

        # 自动检测是否为人物信息图（无需用户感知）
        prompt_generator = self._create_prompt_generator()
        is_character = prompt_generator.detect_character_infographic(topic, audience, key_point)

        template_type = "人物信息图" if is_character else "通用信息图"
        print(f"\n生成中... (主题: {topic}, 风格: {self.styles[style]}, 类型: {template_type})\n")

        prompt = self.generate_prompt(topic, style, audience, key_point)
        if not prompt:
            print("❌ 提示词生成失败")
            return False

        self.session["prompt"] = prompt
        self.session["template_type"] = template_type  # 记录使用的模板类型

        print("="*60)
        print("✅ 生成的提示词如下：\n")
        print(prompt)
        print("="*60)

        return True

    def run_stage_4_generation_method(self):
        """阶段4：出图方式选择"""
        print("\n" + "="*60)
        print("🎨 信息图生成器 - 阶段 4：出图选择")
        print("="*60)

        print("\n请选择出图方式：\n")
        print("A. 复制提示词")
        print("   - 手动复制上面的提示词")
        print("   - 粘贴到任何支持的工具（Claude、Gemini 等）\n")

        print("B. 直接调用 API 出图")
        print("   - 需要配置 APIMart API 密钥")
        print("   - 一键生成，自动保存\n")

        choice = input("请选择（A/B，默认为A）：").strip().upper() or "A"

        if choice == "A":
            self.session["generation_method"] = "manual"
            print("\n✅ 已选择：手动复制提示词")
            print("提示词已显示在上方，你可以复制使用。")
            self.save_session()
            return True

        elif choice == "B":
            self.session["generation_method"] = "api"
            print("\n✅ 已选择：直接调用 API")

            # 检查配置
            api_config = self.skill_dir / "scripts" / "apimart.env"
            if not api_config.exists():
                print("\n⚠️  未找到 API 配置文件")
                print(f"需要在 {api_config} 中配置 API 密钥")
                print("参考：../image-assistant/scripts/apimart.env.example")
                return False

            print("\n准备调用 API...")
            self._call_api_generate()
            self.save_session()
            return True

        else:
            print("❌ 选择无效，使用默认方式（A）")
            self.session["generation_method"] = "manual"
            return True

    def _call_api_generate(self):
        """调用 APIMart API 生成图片"""
        print("\n⏳ 调用 APIMart API 生成图片...")

        # 生成 JSONL 请求
        jsonl_request = self.generate_jsonl_request(self.session["prompt"])

        # 保存请求到临时文件
        requests_file = self.output_dir / "api_request.jsonl"
        with open(requests_file, 'w', encoding='utf-8') as f:
            f.write(jsonl_request + "\n")

        print(f"✅ 请求文件已保存：{requests_file}")
        print(f"\n可以手动调用脚本：")
        print(f"python3 ../image-assistant/scripts/apimart_batch_generate.py \\")
        print(f"  --config scripts/apimart.env \\")
        print(f"  --input {requests_file}")

        # TODO: 这里可以直接调用脚本，但需要考虑跨目录的相对路径问题

    def run_full_workflow(self):
        """运行完整工作流"""
        try:
            if not self.run_stage_1_topic_input():
                return False

            if not self.run_stage_2_style_selection():
                return False

            if not self.run_stage_3_prompt_generation():
                return False

            if not self.run_stage_4_generation_method():
                return False

            print("\n" + "="*60)
            print("🎉 信息图生成完成！")
            print("="*60)
            print(f"\n会话已保存到：{self.output_dir}")

            return True

        except KeyboardInterrupt:
            print("\n\n⚠️  已取消")
            return False
        except Exception as e:
            print(f"\n❌ 错误：{e}")
            return False


def main():
    """主入口"""
    orchestrator = InfographicOrchestrator()
    success = orchestrator.run_full_workflow()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
