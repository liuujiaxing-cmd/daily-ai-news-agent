---
title: AI Daily News Agent
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: streamlit
sdk_version: 1.31.0
app_file: src/dashboard.py
pinned: false
license: MIT
---

# 🤖 每日 AI 资讯智能体 (Daily AI News Agent)

[English](./README.md) | 简体中文

一个智能、自主的 Agent，用于获取、分析和总结全球最新的 AI 资讯。

## ✨ 功能特点

- **自动抓取**：聚合来自 10+ 个信息源的最新资讯，包括 RSS 订阅、博客和 Reddit 等。
- **深度理解**：利用 **OpenAI / DeepSeek** 大语言模型阅读完整文章，并提取核心洞察与摘要。
- **上下文感知**：具备记忆能力，能够联系过往事件提供具有连续性的新闻总结。
- **深度研究模式 (Pro)**：可针对特定主题（如：“DeepSeek 架构”）进行按需的深度定向研究。
- **多渠道分发**：
  - 📊 **Web 仪表盘**：提供交互式的 Streamlit 网页前端。
  - 📧 **邮件推送**：每日定时发送精美的 HTML 格式简报。
  - 📱 **微信公众号**：生成支持一键复制的 Markdown 排版格式。
  - 📕 **小红书图文**：支持自动化生成小红书风格的图文素材。
  - 🎬 **短视频生成**：集成 Remotion，支持将文字资讯转换为短视频。

## 📂 项目结构分析

目前项目的核心结构如下：

```text
daily_ai_news_agent/
├── src/                  # 核心代码与逻辑
│   ├── main.py           # 主执行流与调度
│   ├── dashboard.py      # Streamlit Web 前端 UI
│   ├── fetcher.py        # 资讯与 RSS 抓取模块
│   ├── deep_research.py  # DuckDuckGo 深度搜索引擎
│   ├── summarizer.py     # LLM 分析与摘要处理
│   └── ...               # 其他核心组件 (如邮件发送、内容工厂等)
├── .github/workflows/    # GitHub Actions 自动化工作流 (每日定时任务、同步 HuggingFace 等)
├── scripts/              # 实用脚本工具 (软著文件生成、PDF转换、邮件测试等)
├── docs/                 # 项目文档、API说明、软著材料及总结报告
├── templates/            # 模板文件 (邮件 HTML 模板、微信排版模板)
├── remotion_video/       # 基于 Remotion 的短视频生成模块
├── xhs_output/           # 自动生成的小红书卡片/封面等图文产出物
├── .agents/              # 自定义 Agent 技能 (如小红书自动化脚本、上下文优化等)
├── data/                 # 历史数据存储 (如 history.json 记忆库)
├── subscribers.txt       # 邮件订阅用户列表
└── requirements.txt      # Python 依赖库
```

## 🚀 快速开始 (本地运行)

1. **克隆仓库**
   ```bash
   git clone https://github.com/liuujiaxing-cmd/daily-ai-news-agent.git
   cd daily-ai-news-agent
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **配置环境变量**
   在根目录下创建一个 `.env` 文件，并填入以下内容：
   ```bash
   OPENAI_API_KEY=sk-xxxx
   OPENAI_BASE_URL=https://api.deepseek.com
   LLM_MODEL=deepseek-chat
   ```

4. **运行仪表盘**
   ```bash
   streamlit run src/dashboard.py
   ```

## ☁️ 部署到 Streamlit Cloud

1. 将此仓库 Fork 到你的 GitHub 账号下。
2. 访问 [share.streamlit.io](https://share.streamlit.io/)。
3. 连接你的 GitHub 账号并选择此仓库。
4. **Main file path (主文件路径)**：填写 `src/dashboard.py`。
5. **Advanced Settings (高级设置)**：在 Secrets 环境变量中添加你的 `OPENAI_API_KEY` 等机密信息。
6. 点击 **Deploy (部署)** 即可上线！

## 📄 开源协议

本项目基于 MIT 协议开源。
