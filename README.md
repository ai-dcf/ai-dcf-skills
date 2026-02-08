# AI蛋炒饭 Skills / Claude Code Skills Collection

[English](#english) | [中文](#中文)

---

## 中文

### 📖 简介

这是一个精心打造的 Claude Code Skills 集合，旨在提升内容创作、视觉表达和软件开发的效率。包含信息图生成、多宫格漫画制作、前端设计、PRD 撰写等实用工具，每个 Skill 都经过实战验证，帮助你在日常工作中更加高效。

### ✨ 包含的 Skills

#### 🎨 [信息图生成器](./infographic) (Infographic Generator)
**描述**: 快速生成单张信息图，支持智能风格推荐和人物自动检测，一键生成高质量提示词。

**适用场景**:
- 文章需要配图、公众号封面设计
- 数据图表、流程图的可视化呈现
- 游戏角色卡、人物设定图制作
- 需要统一风格的系列配图

**核心功能**:
- 🎯 **智能识别**: 自动检测内容是否为人物/角色，自动切换专用模板（无需人工干预）
- 🎨 **风格多样**: 内置 16 种专业风格（涵盖科技、商务、艺术、文化、自然等）
- 📐 **自动适配**: 智能推荐最适合的图片比例
- ⚡ **一键出图**: 支持直接调用 API 生成图片或复制提示词
- 📝 **完整流程**: 从主题输入到风格选择、比例确认、提示词生成的全自动流程

**触发方式**:
```
生成一张信息图
给我出个信息图
/infographic
```

---

#### 📸 [配图助手](./image-assistant) (Image Assistant)
**描述**: 深度配图工作流，将文章/模块内容转成统一风格、少字高可读的 16:9 信息图提示词。包含需求澄清、配图规划、文案定稿、提示词封装全流程。

**适用场景**:
- 长文章配图、系列图策划
- 需要严格控制文案的场景
- 追求少字、高可读性的信息图

**核心功能**:
- 📝 **完整工作流**: 需求澄清 -> 配图规划 -> 文案定稿 -> 提示词封装 -> 迭代润色
- 🎯 **精准控制**: 逐张确认画面文案（Copy Spec），确保信息准确
- 🎨 **风格统一**: 默认提供高可读性的手绘/插画风格
- 🔄 **闭环迭代**: 支持多轮反馈润色

**触发方式**:
```
这段内容做个图
/image
/配图
```

---

#### 🖼️ [多宫格漫画助手](./manhua-assistant) (Manhua Assistant)
**描述**: 将文字内容转换成多宫格漫画的生图提示词，模拟手绘草稿的自然错落感，支持批量生产。

**适用场景**:
- 将文章、故事、小说情节可视化
- 制作流程说明、知识科普的漫画版本
- 公众号长图、PPT 插画、海报设计
- 需要批量生成风格统一的多格漫画

**核心功能**:
- 📝 **需求挖掘**: 引导式对话，深度厘清内容、场景与受众
- 📅 **宫格规划**: 自动拆分内容，规划分镜清单与布局
- ✍️ **文案定稿**: 逐格确认画面文案（Copy Spec），确保信息准确
- 🎨 **风格定制**: 支持 14 种手绘风格（日漫、水彩、素描、木刻等）
- 🔄 **闭环迭代**: 支持多轮反馈润色，集成 APIMart 自动出图

**触发方式**:
```
这段内容做成漫画
帮我把这个故事画成四格漫画
/manhua-assistant
```

---

#### 💻 [前端设计](./frontend-design) (Frontend Design)
**描述**: 创建具有高设计质量、风格独特的生产级前端界面。拒绝平庸的 AI 审美，注重排版、配色、动效和空间构成。

**适用场景**:
- 构建网页组件、着陆页
- 仪表盘、应用界面设计
- 需要摆脱“AI味”的界面开发

**触发方式**:
```
设计一个页面
开发一个漂亮的组件
/frontend-design
```

---

#### 🎨 [UI/UX Pro Max](./ui-ux-pro-max)
**描述**: 前端 UI/UX 设计智能库，提供 50+ 风格、20+ 配色、字体搭配及最佳实践。

**适用场景**:
- 设计决策阶段
- 需要美观、惊艳的界面设计时首选
- 查找特定风格（如玻璃拟态、新拟态）的实现参考

**触发方式**:
```
设计漂亮的界面
/ui-ux-pro-max
```

---

#### 📝 [PRD 文档助手](./prd-doc-writer) (PRD Doc Writer)
**描述**: 以故事为驱动的 PRD 撰写工具，强调与用户的“伙伴”关系，通过阶段性确认（旅程地图、单点确认）和可视化（ASCII 线框图 + Mermaid）共同构建高质量文档。

**适用场景**:
- 梳理复杂需求、撰写 PRD
- 用户故事细化
- 需要减少歧义的文档协作

**触发方式**:
```
梳理 PRD
写需求文档
/prd-doc-writer
```

---

#### 🔄 [需求变更工作流](./req-change-workflow) (Req Change Workflow)
**描述**: 针对现有代码库的标准化变更流程，防止“边改边炸”。通过 7 步闭环（澄清→基线→评估→设计→实现→验证→文档）确保变更安全可控。

**适用场景**:
- 修改现有功能
- Chrome 扩展开发
- 涉及核心逻辑的调整

**触发方式**:
```
改需求
需求变更
/req-change-workflow
```

---

#### 🧠 [思维挖掘助手](./thought-mining) (Thought Mining)
**描述**: 通过对话挖掘用户脑中的零散想法，整理成结构化的洞察和文章。

**适用场景**:
- 灵感记录
- 文章构思
- 想法整理

**触发方式**:
```
/thought-mining
/思维挖掘
```

---

### 🚀 快速开始

#### 安装方式

**手动安装**

将本仓库克隆到你的本地 Skills 目录：

```bash
# Claude Code 默认 Skills 目录通常是 ~/.claude/skills/
cd ~/.claude/skills/

# 克隆本仓库
git clone https://gitee.com/ai-dcf/ai-dcf-skills.git
```

或者，你也可以单独复制需要的 Skill 文件夹到你的 Skills 目录。

#### 使用 Skills

在 Claude Code CLI 中，你可以通过 `/` 命令或自然语言触发相应的 Skill。

---

### 📂 项目结构

```
.
├── README.md                    # 项目说明文档
├── LICENSE                      # 许可证
├── frontend-design/             # 前端设计
├── image-assistant/             # 配图助手
├── infographic/                 # 信息图生成器
├── manhua-assistant/            # 多宫格漫画助手
├── prd-doc-writer/              # PRD 文档助手
├── req-change-workflow/         # 需求变更工作流
├── thought-mining/              # 思维挖掘助手
└── ui-ux-pro-max/               # UI/UX 设计智能库
```

---

### 🤝 贡献

欢迎提交 Issue 和 Pull Request！如果你有任何建议或发现了 bug，请随时告诉我。

---

### 📄 许可证

本项目采用 [MIT License](./LICENSE) 开源。

---

## English

### 📖 Introduction

A collection of Claude Code Skills designed to enhance content creation, visual expression, and software development efficiency. Includes tools for infographic generation, manga creation, frontend design, PRD writing, and more. Battle-tested to help you work more effectively.

### ✨ Included Skills

#### 🎨 [Infographic Generator](./infographic)
**Description**: Quickly generate single infographics with smart style recommendation and automatic character detection.

**Use Cases**:
- Article illustrations, social media covers
- Data charts, process visualizations
- Game character cards, character designs
- Series illustrations with unified style

**Core Features**:
- 🎯 **Smart Detection**: Automatically detects character/person content and switches to dedicated templates
- 🎨 **Diverse Styles**: Built-in 16 professional styles (Tech, Business, Art, Culture, etc.)
- 📐 **Auto-Adaptation**: Smart recommendation for best aspect ratios
- ⚡ **Instant Generation**: Support direct API generation or prompt copying
- 📝 **Complete Flow**: Automated flow from topic input to style/ratio selection and prompt generation

**Trigger**:
```
Generate an infographic
Make an infographic for this
/infographic
```

---

#### 📸 [Image Assistant](./image-assistant)
**Description**: Deep workflow for converting content into unified, high-readability 16:9 infographic prompts. Includes requirements clarification, planning, copy finalization, and prompt encapsulation.

**Use Cases**:
- Long article illustrations, series planning
- Scenarios requiring strict copy control
- High readability infographics

**Trigger**:
```
Make an image for this
/image
```

---

#### 🖼️ [Manhua Assistant](./manhua-assistant)
**Description**: Convert text content into multi-panel manga generation prompts, simulating natural hand-drawn layouts.

**Use Cases**:
- Story visualization, novel adaptation
- Process explanation, educational content
- Social media long images, PPT illustrations
- Batch generation of consistent multi-panel manga

**Core Features**:
- 📝 **Requirement Mining**: Guided conversation to deeply clarify content, context, and audience
- 📅 **Panel Planning**: Automatically split content and plan storyboard layouts
- ✍️ **Copy Finalization**: Confirm copy for each panel (Copy Spec) to ensure accuracy
- 🎨 **Style Customization**: Support 14 hand-drawn styles (Manga, Watercolor, Sketch, etc.)
- 🔄 **Closed-Loop Iteration**: Support multi-round feedback and integrated APIMart generation

**Trigger**:
```
Turn this content into a manga
Draw a 4-panel comic for this story
/manhua-assistant
```

---

#### 💻 [Frontend Design](./frontend-design)
**Description**: Create distinctive, production-grade frontend interfaces with high design quality. Avoids generic AI aesthetics, focusing on typography, color, motion, and spatial composition.

**Use Cases**:
- Building web components, landing pages
- Dashboard, app interface design
- Interface development requiring unique aesthetics

**Trigger**:
```
Design a page
Build a beautiful component
/frontend-design
```

---

#### 🎨 [UI/UX Pro Max](./ui-ux-pro-max)
**Description**: Frontend UI/UX design intelligence database, providing 50+ styles, 20+ palettes, font pairings, and best practices.

**Use Cases**:
- Design decision phase
- Creating stunning, gorgeous interfaces
- Finding style references (e.g., Glassmorphism, Neumorphism)

**Trigger**:
```
Design a beautiful interface
/ui-ux-pro-max
```

---

#### 📝 [PRD Doc Writer](./prd-doc-writer)
**Description**: Story-driven PRD writing tool emphasizing "partnership" with users. Builds high-quality docs through staged confirmation (journey map, single-point check) and visualization (ASCII wireframes + Mermaid).

**Use Cases**:
- Clarifying complex requirements, writing PRDs
- Refining user stories
- Collaborative documentation to reduce ambiguity

**Trigger**:
```
Write a PRD
Define requirements
/prd-doc-writer
```

---

#### 🔄 [Req Change Workflow](./req-change-workflow)
**Description**: Standardized workflow for changes in existing codebases to prevent regression. Ensures safety through a 7-step loop (Clarify -> Baseline -> Impact -> Design -> Implement -> Verify -> Docs).

**Use Cases**:
- Modifying existing features
- Chrome extension development
- Core logic adjustments

**Trigger**:
```
Change requirements
Modify feature
/req-change-workflow
```

---

#### 🧠 [Thought Mining](./thought-mining)
**Description**: Mining scattered thoughts from user's mind through conversation, organizing them into structured insights and articles.

**Use Cases**:
- Idea recording
- Article brainstorming
- Thought organization

**Trigger**:
```
/thought-mining
```

---

### 🚀 Quick Start

#### Installation

**Manual Installation**

Clone this repository to your local Skills directory:

```bash
# Claude Code default Skills directory is usually ~/.claude/skills/
cd ~/.claude/skills/

# Clone this repository
git clone https://gitee.com/ai-dcf/ai-dcf-skills.git
```

Or you can simply copy the required Skill folder to your Skills directory.

#### Usage

In Claude Code CLI, you can use them by describing your needs or using the `/` commands.

---

### 🤝 Contributing

Issues and Pull Requests are welcome! If you have any suggestions or find bugs, please feel free to let me know.

---

### 📄 License

This project is open source under the [MIT License](./LICENSE).

---
