# 用户手册 (User Manual)

## 1. 软件概述
**软件名称**：Daily AI News Agent
**软件版本**：V2.4
**运行环境**：Python 3.9+ / Docker / GitHub Actions

Daily AI News Agent 是一款全自动化的 AI 新闻聚合与分发系统。它利用先进的大语言模型（LLM）技术，自动从全球各大科技源抓取最新资讯，进行智能摘要、深度分析，并通过邮件和 Web 仪表盘分发给订阅用户。V2.4 版本特别增强了商业化功能，支持付费墙（Paywall）、邮件追踪和多渠道分发。

## 2. 功能介绍

### 2.1 自动化新闻抓取 (News Gathering)
**功能描述**：
系统内置多个新闻源适配器（如 Hacker News, Product Hunt, Hugging Face 等），每日定时自动抓取最新热门内容。
- **操作方式**：后台全自动运行，无需人工干预。可通过 `config.yaml` 配置抓取源和关键词。

### 2.2 智能摘要与深度分析 (AI Analysis)
**功能描述**：
利用 DeepSeek 或 OpenAI 模型，对抓取到的长文进行精简摘要，并生成深度分析报告（Deep Dive）。
- **操作方式**：系统自动处理。支持生成“简报模式”和“深度报告模式”。

### 2.3 邮件分发系统 (Email Dispatch)
**功能描述**：
集成 Resend 服务，支持向成千上万的订阅用户发送排版精美的 HTML 邮件。
- **功能亮点**：
    - **双模式发送**：支持“免费版简报”和“付费版深度报告”区分发送。
    - **数据追踪**：实时追踪邮件打开率、点击率，数据可视化展示。

### 2.4 商业化仪表盘 (Monetization Dashboard)
**功能描述**：
提供一个可视化的 Web 仪表盘，展示新闻流和用户状态。
- **付费墙功能**：深度分析内容被锁定，仅付费会员可见（模拟演示）。
- **操作方式**：用户登录 Dashboard 查看历史日报，未付费用户只能看到标题和摘要。

### 2.5 自动化运维 (DevOps)
**功能描述**：
项目集成了 GitHub Actions，实现每日定时触发、自动构建和部署。
- **部署**：支持一键部署到 Vercel 或 Docker 容器。

## 3. 安装与配置

### 3.1 环境要求
- 操作系统：Linux / macOS / Windows
- Python 版本：3.9 及以上
- 依赖库：见 `requirements.txt`

### 3.2 快速启动
1.  克隆代码仓库：
    ```bash
    git clone https://github.com/your-repo/daily-ai-news-agent.git
    ```
2.  安装依赖：
    ```bash
    pip install -r requirements.txt
    ```
3.  配置环境变量：
    复制 `.env.example` 为 `.env`，填入 API Key (OpenAI, Resend 等)。
4.  运行程序：
    ```bash
    python main.py
    ```

## 4. 常见问题
- **Q: 如何添加新的新闻源？**
  A: 在 `news_sources/` 目录下创建一个新的 Python 类继承自 `BaseSource`，并在配置文件中启用即可。
- **Q: 邮件发送失败怎么办？**
  A: 请检查 Resend API Key 是否过期，以及发件域名是否已通过 DNS 验证。
