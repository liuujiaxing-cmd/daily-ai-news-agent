# AI Daily News Agent 软件使用说明书

**软件名称**: AI Daily News Agent (AI 每日新闻智能体)
**版本号**: v2.4
**生成日期**: 2026年01月30日

---

## 1. 软件概述

### 1.1 开发背景
在信息爆炸的时代，科技从业者每天面临海量的新闻资讯。AI Daily News Agent 旨在通过人工智能技术，自动聚合全球主流科技媒体信息，进行深度阅读、筛选和总结，为用户提供高价值的每日情报。

### 1.2 主要功能
*   **多源数据抓取**: 支持 TechCrunch, MIT Review, Hugging Face 等 10+ 个主流 RSS 源。
*   **智能筛选与总结**: 利用 LLM (DeepSeek/OpenAI) 对新闻进行相关性评分和深度总结。
*   **多渠道分发**: 支持生成 HTML 邮件、Markdown 报告以及适配微信公众号的排版格式。
*   **可视化仪表盘**: 提供 Web 端 (Streamlit) 仪表盘，支持历史归档查看和实时数据监控。
*   **深度调研 (Deep Research)**: 针对特定关键词进行网络广度搜索，补充新闻背景。

## 2. 运行环境与安装

### 2.1 硬件要求
*   CPU: 2核 2GHz 及以上
*   内存: 4GB 及以上
*   硬盘: 10GB 可用空间

### 2.2 软件环境
*   操作系统: Windows 10/11, macOS, Linux
*   运行环境: Python 3.10+
*   依赖库: `requests`, `streamlit`, `openai`, `beautifulsoup4` 等 (详见 requirements.txt)

### 2.3 安装步骤
1.  **获取源码**: 从 GitHub 仓库下载最新版本代码。
2.  **安装依赖**: 在终端运行 `pip install -r requirements.txt`。
3.  **配置环境**: 复制 `.env.example` 为 `.env`，并填入 API Key 和邮件配置。

## 3. 功能模块详解

### 3.1 新闻抓取模块 (Fetcher)
[此处插入 Fetcher 运行截图]
该模块负责定时从 RSS 源获取最新文章，并使用 BeautifulSoup 提取正文内容和封面图片。

### 3.2 智能分析模块 (Summarizer)
[此处插入 Summarizer 处理日志截图]
核心模块，采用 Map-Reduce 架构。首先对海量新闻进行初筛（Token Saving），然后对入选新闻进行精读，生成一句话摘要、核心要点和深度洞察。

### 3.3 报表生成模块 (Reporter)
[此处插入 HTML 报告截图]
自动生成精美的 HTML 报告，支持卡片式布局，适配移动端阅读。同时支持生成微信公众号专用格式。

### 3.4 邮件发送模块 (Email Sender)
支持 SMTP 和 Resend API 双模式。支持群发、密送 (BCC) 和打开率追踪。

## 4. 操作流程

### 4.1 启动系统
在终端运行以下命令启动全自动流程：
```bash
python src/main.py --hours 24 --email
```

### 4.2 查看仪表盘
运行以下命令启动 Web 界面：
```bash
streamlit run src/dashboard.py
```
[此处插入 Streamlit 仪表盘截图]

### 4.3 管理订阅用户
编辑 `subscribers.txt` 文件，每行添加一个邮箱地址即可。

## 5. 异常处理
*   **网络超时**: 系统会自动重试 3 次。
*   **API 额度不足**: 也就是 LLM 服务报错，系统会记录日志并跳过当前任务。

---
**版权所有 © 2026 AI Daily News Agent 开发团队**
