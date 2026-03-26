# 需求变更与迭代记录 (Changelog & Requirements)

## v0.1.0 (Initialization) - 2024-02-04

### 🚀 初始功能
*   **项目初始化**: 建立 `daily_ai_news_agent` 项目结构。
*   **文档体系**: 创建 `docs` 目录及四大核心管理文档。
*   **技术选型**:
    *   LLM: DeepSeek V3
    *   Crawler: Jina Reader
    *   Framework: Python (LangChain / AutoGen 待定)

---

## 待办需求池 (Backlog)

### Phase 1: 核心流程跑通 (MVP)
*   [ ] **RSS/URL 采集器**: 编写 Python 脚本，从指定源 (如 HackerNews, Twitter) 获取 URL 列表。
*   [ ] **Jina 内容提取**: 对接 Jina API，将 URL 转为 Markdown。
*   [ ] **DeepSeek 摘要**: 编写 Prompt，让 AI 总结新闻核心价值。
*   [ ] **Markdown 报告生成**: 将多条摘要聚合为一篇日报。

### Phase 2: 自动化与分发
*   [ ] **GitHub Actions / Cron**: 设置定时任务，每天早上 8 点自动运行。
*   [ ] **多渠道分发**:
    *   自动推送到 Telegram Channel。
    *   自动发送邮件 (SMTP)。
    *   自动发布到 WordPress/Notion。

### Phase 3: 深度智能化
*   [ ] **相关性评分**: 让 AI 判断新闻是否重要，过滤掉“水文”。
*   [ ] **分类打标**: 自动给新闻打上 #AI #Crypto #Design 等标签。
