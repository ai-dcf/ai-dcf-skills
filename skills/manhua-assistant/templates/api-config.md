## API 配置（APIMart 平台）

> 建议：把真实 `TOKEN` 放在 `scripts/apimart.env`（本地文件），不要写进文档/仓库或聊天记录。

本 Skill 使用 APIMart 平台进行图片生成。

| 模型 | 配置键 | 特点 |
|------|--------|------|
| **Gemini-3-Pro** (APIMart) | `TOKEN`, `API_URL`, `MODEL` | 精确比例控制 (16:9/3:4等)、异步任务、高分辨率 |

### 完整配置示例

```env
# ==================== APIMart 配置 (Gemini-3-Pro) ====================

# API Token
TOKEN=your_apimart_token_here

# API 地址
API_URL=https://api.apimart.ai/v1/images/generations

# 模型名称
MODEL=gemini-3-pro-image-preview

# 图片分辨率: 2K, 4K
RESOLUTION=2K

# 图片尺寸配置（使用比例如 16:9, 1:1, 3:4, 9:16 等）
SIZE=16:9

# 生成数量
N=1

# 垫图 URL（可选，用于图生图）
PAD_URL=
```

### SIZE 参数说明

- 使用精确比例：`16:9`, `9:16`, `1:1`, `3:4`, `4:3`, `3:2`, `2:3`, `21:9`
- 根据格子数量调整，详细对照表见 `references/aspect-ratios.md`

### 运行方式

```bash
python3 scripts/apimart_batch_generate.py \
  --config scripts/apimart.env \
  --input out/apimart.requests.jsonl
```

**dry-run（不请求；把 curl 与请求信息写入单个 `run.json`）**

```bash
python3 scripts/apimart_batch_generate.py \
  --config scripts/apimart.env \
  --input out/apimart.requests.jsonl \
  --dry-run
```
