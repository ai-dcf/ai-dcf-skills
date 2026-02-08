# 智能内容分析功能说明

**修改目标：** 根据用户输入智能分析信息量，动态调整提示词结构和内容点数，避免信息量固定死板的问题。

---

## 核心改进

### 之前的问题
- ❌ 内容点数固定（3-5 个）
- ❌ 结论部分总是存在（有时不需要）
- ❌ 没有根据主题复杂度调整
- ❌ 信息密度无法灵活处理

### 改进后的方案
- ✅ 内容点数动态调整（2-8 个）
- ✅ 结论部分自动判定（需要时才添加）
- ✅ 根据复杂度智能调整内容深度
- ✅ 根据信息密度灵活处理结构
- ✅ 基本原则："讲清楚" - 信息匹配内容复杂度

---

## 实现方案

### 1. 新增 `analyze_content_complexity()` 方法

**功能：** 深度分析用户输入的内容复杂度和信息量

**分析维度：**
```
输入分析 (topic + audience + key_point)
    ↓
┌─ 文本长度分析 → 详细程度评估
├─ 关键词识别 → 复杂度评分
├─ 关键词识别 → 信息密度评分
└─ 用户意图分析 → 结论需求判定
    ↓
返回分析结果字典：
{
    "complexity": "simple|medium|complex",      # 复杂度
    "info_density": "low|medium|high",          # 信息密度
    "suggested_points": 2-8,                    # 推荐内容点数
    "needs_conclusion": True/False,             # 是否需要结论
    "conclusion_type": "cta|summary|insight|none",  # 结论类型
    "content_depth": "shallow|medium|deep",     # 内容深度
    "text_length": 42,                          # 输入文本长度
}
```

### 2. 修改内容结构生成方法

**变更方式：** 所有结构生成方法现在接收 `analysis` 参数

**示例 - 流程型结构：**
```python
def _structure_flow(self, topic, analysis):
    num_stages = analysis["suggested_points"]  # 动态点数
    depth = analysis["content_depth"]           # 动态深度

    # 根据分析结果生成不同的结构描述
    if depth == "deep":
        # 每个阶段详细说明 (2-3 句)
    else:
        # 每个阶段简洁说明 (1-2 句)
```

**受影响的方法：**
- `_structure_flow()` - 流程型
- `_structure_comparison()` - 对比型
- `_structure_list()` - 列表型
- `_structure_timeline()` - 时间线型
- `_structure_general()` - 通用型

### 3. 动态结论部分处理

**逻辑流程：**
```
分析用户输入
    ↓
IF 用户提供了 key_point
    → 需要结论 (insight/cta)
ELSE IF 包含"应该", "建议"等CTA关键词
    → 需要结论 (cta)
ELSE IF 复杂度为 complex
    → 需要结论 (summary)
ELSE
    → 不需要结论

生成对应类型的结论指导
```

**结论类型：**
- **CTA** (Call-to-Action) - 行动号召
  ```
  "Provide actionable recommendation or next steps"
  ```
- **Summary** - 总结
  ```
  "Summarize the key insights or main takeaway"
  ```
- **Insight** - 洞察
  ```
  "Share a key insight or thought to remember"
  ```
- **None** - 不需要
  ```
  信息图自然结束，无结论部分
  ```

### 4. 修改 generate_compact() 和 generate()

**变更点：**
- 调用 `analyze_content_complexity()` 分析用户输入
- 将分析结果传递给内容结构生成方法
- 根据 `needs_conclusion` 动态添加或跳过结论部分
- 在约束中记录分析结果

---

## 使用示例

### 示例 1：简单主题

**用户输入：**
```
主题：什么是 AI
```

**系统分析：**
```
- 文本长度：8 字
- 复杂度：simple (没有复杂度关键词)
- 信息密度：low
- 建议点数：2 个
- 需要结论：False
- 内容深度：shallow
```

**生成的提示词包含：**
```
Main Content:
Use a balanced layout with 2 supporting points
- 每点：简洁标题 + 1 句说明

[无结论部分]
```

### 示例 2：复杂主题

**用户输入：**
```
主题：企业数字化转型框架与实施策略分析
受众：管理层
关键点：选择正确的转型路径
```

**系统分析：**
```
- 文本长度：35 字
- 复杂度：complex (包含"框架", "策略", "分析")
- 信息密度：high (包含"与", "分析")
- 建议点数：6 个 (5 + 1 for high density)
- 需要结论：True (有关键点 + 复杂内容)
- 内容深度：deep
- 结论类型：cta
```

**生成的提示词包含：**
```
Main Content:
Use a card-based layout with 6 distinct items
- 每点：标题 (bold) + 2-3 句详细说明

Conclusion/Call-to-Action:
Provide actionable recommendation or next steps
Format: 1-2 powerful, actionable sentences
```

### 示例 3：有明确数字的主题

**用户输入：**
```
主题：SaaS 业务的三大增长杠杆
```

**系统分析：**
```
- 检测到明确数字：3
- 建议点数：3 个 (使用用户指定的数字)
- 需要结论：False (简洁、清晰的列表)
```

**生成的提示词包含：**
```
Main Content:
Use a card-based layout with 3 distinct items
- 每点：标题 + 1-2 句说明

[无结论部分，简洁结束]
```

---

## 关键词库

### 复杂度指示词

**增加复杂度的关键词：**
```
系统、分析、研究、框架、模型、体系、策略、方案、生态、
流程、架构、结构、机制、原理、理论、设计、规划、应用
```

**降低复杂度的关键词：**
```
是什么、怎样、基础、入门、初级、简介、概念、定义、
快速、简单、容易、基本
```

### 信息密度指示词

```
和、或、包括、特点、特征、优点、缺点、类型、分类、
分层、区分、对比、差异、不同、多种、多个、综合
```

### CTA 关键词

```
应该、建议、需要、要、行动、做法、方案、对策、改进、
提升、优化、实施、执行、推荐、选择、采用
```

### 总结关键词

```
总结、总体、整体、概括、综合、结论、核心、要点、
关键、重点、主要、通常、一般、基本
```

---

## 修改的文件

### 代码文件
- **`scripts/prompt_generator.py`** - 核心分析和生成逻辑
  - ✅ 新增 `analyze_content_complexity()` 方法
  - ✅ 修改 `generate_content_structure()` - 接收分析结果
  - ✅ 修改 `_structure_flow()` 等 5 个结构方法 - 动态生成
  - ✅ 修改 `generate_compact()` - 支持动态结论
  - ✅ 修改 `generate()` - 支持动态结论

### 文档文件
- **`templates/base-prompt.md`** - 更新模板说明
  - ✅ 新增智能分析机制说明
  - ✅ 新增分析结果调整表
  - ✅ 新增结论部分判定规则
  - ✅ 新增典型场景示例

- **`stages/04-prompt.md`** - 更新阶段说明
  - ✅ 新增智能内容分析章节
  - ✅ 新增分析算法说明
  - ✅ 更新参考文件说明

---

## 用户体验

### 对用户的影响

✅ **完全透明** - 用户不需要做任何额外操作
✅ **自动优化** - 系统根据内容自动调整
✅ **更灵活** - 不同复杂度的主题得到最佳的提示词
✅ **更清晰** - 信息量与内容复杂度匹配

### 工作流不变

```
用户输入主题 → 选风格 → 选比例 → 系统自动分析并生成最优提示词 → 复制或出图
          ↑
         新增自动分析过程（用户无感知）
```

---

## 典型改进效果

### 简单内容
**之前：** 固定 3-5 个点，可能显得冗长或信息不足
**现在：** 精确 2-3 个点，简洁清晰 ✅

### 复杂内容
**之前：** 固定 3-5 个点，可能信息不够充分
**现在：** 动态 5-6 个点 + 详细说明，信息充分 ✅

### 无需结论的内容
**之前：** 强制添加结论，显得冗余
**现在：** 根据需要自动省略，简洁自然 ✅

### 需要明确行动的内容
**之前：** 通用结论，没有针对性
**现在：** CTA 类型的结论，有明确的指向性 ✅

---

## 测试建议

### 测试用例 1：简单主题
```
Input: "什么是云计算"
Expected: 2-3 个点，无结论
```

### 测试用例 2：有明确数字
```
Input: "SaaS 的 5 大优势"
Expected: 5 个点（使用用户数字），无结论
```

### 测试用例 3：复杂主题 + 关键点
```
Input: Topic: "AI 时代企业的人才战略"
       Key Point: "如何吸引和留住 AI 人才"
Expected: 5-6 个点，CTA 类型结论
```

### 测试用例 4：详细需求
```
Input: 长文本 (80+ 字)，包含多个复杂词
Expected: 6+ 个点，深层内容说明，总结类结论
```

---

## 后续优化建议

1. **学习反馈** - 根据实际生成效果调整关键词权重
2. **语言适配** - 支持多语言的复杂度分析
3. **用户偏好** - 记录用户的风格偏好（喜欢简洁/详细）
4. **A/B 测试** - 对比固定结构 vs 动态结构的效果
