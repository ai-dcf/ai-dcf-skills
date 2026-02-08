# 阶段4：提示词封装（Prompt Pack：可执行生成包）

**目标：** 把阶段3的 Copy Spec 原样封装成"可复制/可调用"的提示词包（Prompt Pack），并支持批量出图。阶段4不负责改文案，只负责：模板拼装、风格一致、参数/约束齐全、避免模型乱加字、把提示词整理成可批量请求的结构化请求包。

## 封装原则（避免和阶段3混淆）

- **Copy Spec 是唯一真值**：提示词中"必须逐字放入"的文字，直接来自阶段3，不在这里重写。
- **提示词负责"怎么画"**：画幅、布局、格子结构、分镜线、角色一致性、风格块、强制约束、负面提示、参数。
- **默认"禁额外小字"**：明确写"除指定文字外不要生成任何额外文字"。

## 生成步骤（按顺序）

1. 确定画幅（参考 `references/aspect-ratios.md` 的格子-画幅对照表）
2. **写入风格定义**（分两部分）：
   - **通用约束**：读取 `templates/style-block.md` 的"通用约束"部分（格子布局、角色一致性、文字规范、视觉连贯）
   - **风格特有要素**：读取阶段2确认的对应风格文件（如 `references/style-japanese-manga.md`），写入该风格的质感 + 色调 + 分镜线 + 文字呈现 + 负面约束
   - **风格锁定**：明确写"以[风格名称]为唯一允许的基础风格，不得切换到其他风格"
   - 允许你用自己的话描述该风格，但不能删掉风格文件中的关键要素与负面约束
3. 写清楚布局结构：
   - **格子错位排布**：格子位置刻意不对齐，左右上下自由错落，像手绘草稿般随意自然。大小格子不一，重要格子更大，小格子填补空隙或偏移位置
   - **人类创作痕迹**：格子边缘不完全平行，分镜线不必完全笔直，允许某些格子轻微旋转或倾斜
   - **分镜线样式**：明确写出分镜线的特点（如"白色间隔带，宽度不均，有的地方宽有的地方窄"或"粗黑分镜线，可轻微手绘波动感"）
   - **突破边界**：动态元素（动作线、效果音、角色动作、情绪线条）可大幅突破格子边界，增强视觉流动性和戏剧性
   - **留白节奏**：留白区域形状不规则，有的宽有的窄，像自然呼吸的节奏而非机械均分
   - 如果有角色：明确角色一致性要求（发型/衣着/配色全图统一）
4. **粘贴 Copy Spec 的"必须逐字放入的文字"**
5. 加强制约束 + 负面提示（无乱码/不加字/不密集小字/不背景杂乱/角色不突变）
6. 生成**请求包（JSONL）**：把每张图的 Prompt 内容写入一行（参考 `templates/apimart-requests-jsonl.md`）
7. **执行出图**：用户确认后直接执行出图（不再二次确认）

## 模板使用

- 风格系统入口：`templates/style-block.md`（通用约束 + 风格选择对照表）
- 风格特有要素：阶段2确认的 `references/style-*.md` 文件（必须读取并写入）
- 画幅参考：`references/aspect-ratios.md`（格子-画幅对照表）

## 本阶段输出物

- **Prompt Pack**：按"图1/图2/…"编号输出；每张图一个独立代码块（便于复制/脚本调用）；代码块外最多 1–2 句说明
- **Request Pack（JSONL）**：生成 APIMart 格式的请求文件 `out/apimart.requests.jsonl`
- **执行方式**：当用户在阶段4明确选择"API出图"时：
  1. 先输出提示词让用户查看（选项A：手动出图 或 选项B：API出图）
  2. 用户选择B后，读取 `scripts/apimart.env` 配置，直接执行出图（不再二次确认）

## 风格跑偏风险与对策

> 详细问题分析与解决方案见 `references/common-issues.md`

核心对策：在每张图的 prompt 里都明确"以阶段2确认的[风格名称]为唯一基础，不得换风格"，并写入对应风格文件中的全部负面约束。详细问题与解决方案见 `references/common-issues.md`。

---

## 调用 APIMart API 出图（用户选择后直接执行）

> 规则：**先封装 Prompt Pack 并展示给用户 → 询问"手动出图"还是"API直接出图" → 用户选择"API直接出图"后读取 `scripts/apimart.env` 配置，直接生成JSONL并执行**。不在生成JSONL后再次确认。

### 需要的东西

1. **API 配置**（本地文件）：`scripts/apimart.env`（参考 `templates/api-config.md`）
2. **请求包**（JSONL）：`out/apimart.requests.jsonl`（参考 `templates/apimart-requests-jsonl.md`）

### 请求包字段（每行一张图）

- `id`：建议 `01` / `02` / …
- `prompt`：阶段4输出的 Prompt 内容（可直接粘贴）
- `size`：默认 `16:9`
- `n`：默认 `1`
- `resolution`：默认 `2K`
- `model`：默认 `gemini-3-pro-image-preview`
- `pad_url`：可留空（暂不需要垫图 URL）

### 运行方式（二选一）

**A) 用脚本出图（推荐）**

```bash
python3 scripts/apimart_batch_generate.py \
  --config scripts/apimart.env \
  --input out/apimart.requests.jsonl
```

**B) dry-run（不请求；把 curl 与请求信息写入单个 `run.json`）**

```bash
python3 scripts/apimart_batch_generate.py \
  --config scripts/apimart.env \
  --input out/apimart.requests.jsonl \
  --dry-run
```

