#!/usr/bin/env python3
"""
APIMart Image Generation API Caller
用于调用 APIMart API 生成图片
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

try:
    import requests
except ImportError:
    print("Error: requests library not found. Install with: pip install requests")
    sys.exit(1)


class APImart:
    """APIMart API 调用器"""

    def __init__(self, config_file=None):
        """
        初始化 API 调用器

        Args:
            config_file: 环境配置文件路径
        """
        # 加载环境变量
        if config_file:
            if not Path(config_file).exists():
                raise FileNotFoundError(f"Config file not found: {config_file}")
            load_dotenv(config_file)
        else:
            # 尝试加载默认位置
            default_config = Path(__file__).parent / "apimart.env"
            if default_config.exists():
                load_dotenv(default_config)

        self.api_key = os.getenv("APIMART_API_KEY")
        self.api_url = os.getenv("APIMART_API_URL", "https://api.apimart.com/v1")
        self.timeout = int(os.getenv("APIMART_TIMEOUT", "300"))
        self.max_retries = int(os.getenv("APIMART_MAX_RETRIES", "3"))

        if not self.api_key:
            raise ValueError("APIMART_API_KEY not found in environment or config file")

        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })

    def generate_image(self, prompt, size="16:9", n=1, resolution="2K", model="gemini-3-pro-image-preview"):
        """
        调用 API 生成单张图片

        Args:
            prompt: 提示词
            size: 图片尺寸
            n: 数量
            resolution: 分辨率
            model: 使用的模型

        Returns:
            dict: API 响应
        """
        payload = {
            "prompt": prompt,
            "size": size,
            "n": n,
            "resolution": resolution,
            "model": model,
        }

        try:
            print(f"⏳ 调用 API 生成图片...")
            response = self.session.post(
                f"{self.api_url}/images/generations",
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"❌ API 请求失败: {e}")
            return None

    def generate_batch(self, requests_jsonl, output_dir=None):
        """
        批量调用 API（从 JSONL 文件）

        Args:
            requests_jsonl: JSONL 文件路径
            output_dir: 输出目录

        Returns:
            list: 生成结果列表
        """
        if not Path(requests_jsonl).exists():
            print(f"❌ 请求文件不存在: {requests_jsonl}")
            return []

        if output_dir is None:
            output_dir = Path(__file__).parent.parent / "outputs"

        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)

        results = []

        with open(requests_jsonl, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, 1):
                if not line.strip():
                    continue

                try:
                    request = json.loads(line)
                except json.JSONDecodeError:
                    print(f"❌ 行 {i} 不是有效的 JSON")
                    continue

                request_id = request.get("id", str(i))
                prompt = request.get("prompt")
                size = request.get("size", "16:9")
                n = request.get("n", 1)
                resolution = request.get("resolution", "2K")
                model = request.get("model", "gemini-3-pro-image-preview")

                if not prompt:
                    print(f"❌ 请求 {request_id} 缺少 prompt")
                    continue

                print(f"\n[{i}] 生成图片 {request_id}...")
                response = self.generate_image(prompt, size, n, resolution, model)

                if response:
                    result = {
                        "id": request_id,
                        "status": "success",
                        "response": response,
                        "timestamp": datetime.now().isoformat()
                    }
                    print(f"✅ 生成成功！")
                    results.append(result)
                else:
                    result = {
                        "id": request_id,
                        "status": "failed",
                        "timestamp": datetime.now().isoformat()
                    }
                    results.append(result)

        # 保存结果
        run_file = output_dir / "run.json"
        with open(run_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        print(f"\n✅ 结果已保存到: {run_file}")
        return results


def main():
    """主入口"""
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python3 apimart_caller.py <jsonl_file> [config_file]")
        print("\n示例:")
        print("  python3 apimart_caller.py output/api_request.jsonl scripts/apimart.env")
        sys.exit(1)

    jsonl_file = sys.argv[1]
    config_file = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        caller = APImart(config_file)
        results = caller.generate_batch(jsonl_file)

        if results:
            print(f"\n✅ 生成完成！共 {len(results)} 张图片")
        else:
            print("\n❌ 生成失败")
            sys.exit(1)

    except Exception as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
