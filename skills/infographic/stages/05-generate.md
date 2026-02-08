# 阶段 5：出图选择（Generate Image）

**目标：** 让用户选择如何获得最终图片：复制提示词手动生成，还是调用 API 直接出图。

---

## 用户选择（二选一）

### 选项 A：手动复制提示词
- **流程**：用户复制上阶段的提示词
- **工具**：可用任何支持的出图工具（如 Claude、Midjourney、Gemini 等）
- **优势**：灵活、可以多次尝试、微调参数
- **劣势**：手动操作、需要自己找工具

### 选项 B：直接调用 API 出图（推荐）
- **前置条件**：需要配置 `scripts/apimart.env`（APIMart API 密钥）
- **流程**：我直接调用 API 生成图片
- **优势**：一键出图、自动存储、快速获得结果
- **劣势**：需要有效的 API 配置、调用时间视 API 响应速度

---

## 用户选择后的操作

### 如果选择 A：手动复制
- 向用户展示提示词（已在阶段 4 输出）
- 提示："你可以复制上面的提示词，粘贴到任何支持的出图工具中"

### 如果选择 B：API 出图
1. **检查配置**
   - 检查是否存在 `scripts/apimart.env`
   - 如果不存在，提示用户需要配置 API 密钥

2. **生成请求包（JSONL）**
   - 基于阶段 4 的提示词和用户选择的比例，生成一行 JSONL
   - **比例映射到 size 字段的规则**：
     | 用户比例 | size 字段值 |
     |---|---|
     | 16:9 | `"16:9"` |
     | 3:4 | `"3:4"` 或 `"768:1024"` |
     | 9:16 | `"9:16"` 或 `"576:1024"` |
     | 1:1 | `"1:1"` 或 `"1024:1024"` |

   - 示例 JSONL：
   ```jsonl
   {"id":"01","prompt":"[提示词内容]","size":"[用户选择的比例]","n":1,"resolution":"2K","model":"gemini-3-pro-image-preview","pad_url":""}
   ```

3. **调用脚本**
   ```bash
   python3 scripts/apimart_batch_generate.py \
     --config scripts/apimart.env \
     --input [JSONL文件路径]
   ```

4. **输出结果**
   - 脚本会生成图片到 `outputs/` 目录
   - 我展示生成的图片和 URL

---

## 本阶段输出物

- **选项 A**：提示词已复制/已输出
- **选项 B**：生成完毕的图片 + URL + `run.json` 记录

---

## 脚本位置

复用 `image-assistant` 的脚本：
- 脚本路径：`D:\AI编程\Skills\image-assistant\scripts\apimart_batch_generate.py`
- 配置例：`D:\AI编程\Skills\image-assistant\scripts\apimart.env.example`
