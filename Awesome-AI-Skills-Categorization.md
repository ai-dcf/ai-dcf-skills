# AI Agent Skills 分类与目录结构

本项目基于 `anthropics/skills`, `vercel-labs/agent-skills`, `ComposioHQ/awesome-claude-skills` 进行整理。

## 目录结构

所有 Skill 按场景分类，存放于对应目录下的 `skills/` 子文件夹中。

### 1. FullStack_Engineering (全栈研发)
> 存放产品、设计、前端、后端、架构、DevOps、测试等所有研发相关 Skill。

- **Product & Design**:
  - `01_ProductManager_Brainstorming`: 需求梳理与 PRD
  - `prd-doc-writer`: PRD 文档撰写
  - `02_Designer_UIUXIntelligence`: 智能设计系统
  - `ui-ux-pro-max`: 高级 UI/UX 设计
  - `02_Designer_WebGuidelines`: Web 设计规范
  - `02_Designer_BrandGuidelines`: 品牌设计指南
  - `02_Designer_CanvasDesign`: Canvas 设计
- **Frontend & Mobile**:
  - `02_Designer_FrontendImplementation`: 前端实现
  - `03_Developer_ReactBestPractices`: React 最佳实践
  - `03_Developer_ArtifactsBuilder`: 组件生成
  - `03_Mobile_Flutter`: Flutter 开发
  - `frontend-design`: 创意前端设计
- **Backend & Architecture**:
  - `01_Architect_TechStackSelector`: 技术选型
  - `02_Architect_APIDesign`: API 设计
  - `05_Backend_MCPBuilder`: MCP 服务构建指南
  - `05_Backend_Database`: 数据库优化
- **DevOps & Process**:
  - `req-change-workflow`: 需求变更工作流
  - `01_Discovery_GitHubSearch`: GitHub 搜索
- **Testing**:
  - `04_Tester_BrowserAutomation`: 浏览器自动化测试
  - `04_Tester_WebAppTesting`: Web 应用自动化测试 (Playwright)

### 2. Content_Creation (自媒体与内容创作)
> 存放文章写作、配图生成、漫画创作等 Skill。

- **Visual & Image**:
  - `image-assistant`: 文章配图与信息图
  - `infographic`: 信息图设计
  - `manhua-assistant`: 漫画创作助手
  - `image-enhancer`: 图像增强
  - `slack-gif-creator`: GIF 生成
  - `video-downloader`: 视频下载
  - `algorithmic-art`: 算法艺术
- **Writing & Ideation**:
  - `thought-mining`: 思维挖掘与大纲整理
  - `domain-name-brainstormer`: 域名头脑风暴
  - `twitter-algorithm-optimizer`: 社交媒体算法优化
  - `theme-factory`: 主题工厂

### 3. Agent_Building (智能体构建)
> 存放 Meta-Skill (构建 Skill 的 Skill) 与任务调度。

- `00_Meta_Dispatcher`: 任务调度与路由
- `skill-creator`: Skill 创建工具
- `skill-share`: Skill 分享
- `template-skill`: Skill 模板
- `langsmith-fetch`: LangSmith 集成
- `lead-research-assistant`: 潜在客户研究助手
- `raffle-winner-picker`: 抽奖助手

### 4. Office_Documentation (文档与办公自动化)
> 存放 Office 文档处理 Skill。

- `invoice-organizer`: 发票整理
- `file-organizer`: 文件整理
- `internal-comms`: 内部通讯模板
- `meeting-insights-analyzer`: 会议纪要分析
- `tailored-resume-generator`: 简历定制生成
- `doc-coauthoring`: 文档共创
- `docx`: Word 文档自动化 (ISO/ECMA 标准支持)

### 5. Enterprise_Integration (企业集成与连接)
> 存放企业级集成方案与 SaaS 平台自动化。

- **SaaS Automations (50+)**:
  - Communication: `slack-automation`, `discord-automation`, `microsoft-teams-automation`, `zoom-automation`, `telegram-automation`, `whatsapp-automation`, `gmail-automation`, `outlook-automation`
  - Development: `github-automation`, `gitlab-automation`, `bitbucket-automation`, `jira-automation`, `linear-automation`, `sentry-automation`, `render-automation`, `vercel-automation`, `supabase-automation`
  - CRM & Sales: `salesforce-automation`, `hubspot-automation`, `zoho-crm-automation`, `pipedrive-automation`, `stripe-automation`, `shopify-automation`
  - Productivity: `notion-automation`, `trello-automation`, `asana-automation`, `monday-automation`, `clickup-automation`, `google-calendar-automation`, `google-drive-automation`
  - Marketing: `mailchimp-automation`, `instagram-automation`, `twitter-automation`, `tiktok-automation`, `youtube-automation`, `linkedin-automation`
  - Other: `figma-automation`, `miro-automation`, `docusign-automation`, `dropbox-automation`, etc.
