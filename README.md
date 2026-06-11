# Cross-Border E-Commerce AI Copilot

## 项目简介

面向出海电商独立站场景的智能客服与运营Agent系统，能够自动处理售前咨询、多语言翻译、邮件营销和差评预警等核心业务。系统基于多Agent协作架构，集成订单查询、物流追踪等外部工具，支持Slack/Discord等即时通讯平台接入。

## 解决的核心问题

- 出海商家面临多语言客服沟通障碍与人力成本高企
- 售前咨询、售后处理、营销触达需要频繁切换多套系统
- 差评和客户投诉缺少实时预警与自动响应机制

## 核心功能模块

### 1. 智能路由分发
- 用户消息进入后，由路由Agent自动识别意图
- 分发至售前Agent / 售后Agent / 营销Agent 处理
- 支持上下文记忆，连续对话不丢失信息

### 2. 售前咨询Agent
- 回复产品规格、价格、优惠活动等问题
- 多语言自动识别与回复（英语、西班牙语、法语等）
- 从知识库检索FAQ和产品文档

### 3. 售后处理Agent
- 查询订单状态、物流轨迹
- 处理退换货、退款等常见售后流程
- 差评预警：监测用户负面情绪，自动升级人工处理

### 4. 邮件营销Agent
- 根据用户历史行为生成个性化营销邮件
- 支持优惠券发放、弃购召回等场景
- 营销效果追踪与简要分析

## 技术架构

- **Agent框架**: LangGraph（状态图编排多Agent协作流程）
- **大语言模型**: OpenAI GPT-4o / Claude 3.5 Sonnet
- **工具集成**:
  - 订单查询API (Shopify / WooCommerce)
  - 物流追踪API (17Track / AfterShip)
  - 向量数据库知识库 (Pinecone / Chroma)
- **记忆系统**: 短期记忆（对话上下文） + 长期记忆（用户画像与偏好）
- **前端交互**: Web聊天界面 (Next.js) / Slack Bot 接入
- **部署**: Docker + AWS / Vercel

## 技术架构图

```

┌─────────────────────────────────────────────────────────┐
│                      用户消息输入                         │
│             (Web Chat / Slack / Discord)                │
└─────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────┐
│                    路由 Agent (Router)                   │
│           意图识别 → 分发至下游专业Agent                    │
└─────────────────────────────────────────────────────────┘
│                    │                    │
▼                    ▼                    ▼
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│   售前 Agent      │ │   售后 Agent     │ │   营销 Agent      │
│  • 产品问答        │ │  • 订单查询       │ │  • 邮件生成       │
│  • 多语言翻译      │ │  • 物流追踪       │ │  • 优惠券发放      │
│  • 知识库检索      │ │  • 差评预警       │ │  • 弃购召回        │
└──────────────────┘ └──────────────────┘ └──────────────────┘
│                    │                    │
▼                    ▼                    ▼
┌─────────────────────────────────────────────────────────┐
│                     工具层 (Tools)                       │
│  订单API  物流API  知识库  邮件服务  情感分析                │
└─────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────┐
│                   记忆系统 (Memory)                       │
│   短期记忆 (对话上下文)  │  长期记忆 (用户偏好数据库)          │
└─────────────────────────────────────────────────────────┘

```

## 项目亮点与工程能力体现

- **多Agent协作**: 基于LangGraph实现Agent间状态传递与任务编排
- **工具调用**: Agent自主判断并调用外部API，非固定流程
- **多语言支持**: 语言自动检测，无需用户手动切换
- **记忆系统**: 用户在售前问过的信息，售后场景无需重复提供
- **安全确认机制**: 发邮件、退款等敏感操作加入人工确认环节
- **可观测性**: 集成LangSmith追踪Agent每一步决策，便于调试与优化

## 快速开始

```bash
# 克隆项目
git clone https://github.com/shuaig1/Cross-Border E-Commerce AI Copilot.git

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env，填入 OPENAI_API_KEY 等必要信息

# 启动后端
python app.py

# 启动前端 (进入 frontend 目录)
npm install && npm run dev
```

Cross-Border E-Commerce AI Copilot/
├── backend/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── router_agent.py        # 路由Agent，意图识别与分发
│   │   ├── presale_agent.py       # 售前咨询Agent
│   │   ├── aftersale_agent.py     # 售后处理Agent
│   │   ├── marketing_agent.py     # 邮件营销Agent
│   │   └── base_agent.py          # Agent基类，封装通用逻辑
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── shopify_api.py         # Shopify订单查询
│   │   ├── tracking_api.py        # 物流追踪 (17Track/AfterShip)
│   │   ├── knowledge_base.py      # 向量库检索工具
│   │   ├── email_service.py       # 邮件发送
│   │   └── sentiment.py           # 情感分析/差评预警
│   ├── memory/
│   │   ├── __init__.py
│   │   ├── short_term.py          # 对话上下文管理
│   │   └── long_term.py           # 用户偏好持久化
│   ├── graph/
│   │   ├── __init__.py
│   │   └── workflow.py            # LangGraph 状态图编排逻辑
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py              # FastAPI路由定义
│   │   └── schemas.py             # Pydantic请求/响应模型
│   ├── config.py                  # 配置加载（环境变量、模型参数等）
│   ├── main.py                    # FastAPI 入口
│   └── requirements.txt           # Python依赖
│
├── frontend/
│   ├── public/                    # 静态资源
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatWindow.tsx      # 聊天窗口组件
│   │   │   └── Message.tsx        # 单条消息组件
│   │   ├── hooks/
│   │   │   └── useChat.ts         # 与后端通信的自定义Hook
│   │   ├── pages/
│   │   │   └── index.tsx          # 主页面
│   │   └── styles/                # 样式文件
│   ├── package.json
│   ├── tsconfig.json
│   └── next.config.js
│
├── bot/                           # 即时通讯接入
│   ├── slack_bot.py               # Slack Bot
│   └── discord_bot.py             # Discord Bot
│
├── docker-compose.yml             # 一键启动本地环境
├── Dockerfile                     # 容器化配置
├── .env.example                   # 环境变量示例
├── .gitignore
└── README.md                      # 项目说明（即你那份Markdown）