# API 接口与数据定义文档 (API & Data Schema)

## 1. 外部 API 接口 (External APIs)

本项目计划集成多个 AI 和数据服务 API 来实现新闻的抓取、分析和生成。

### 1.1 新闻抓取 (News Aggregation)
*   **服务商**: Jina AI (Reader API) / Bing News / NewsAPI
*   **接口地址**: `https://r.jina.ai/{url}` (示例)
*   **功能**: 将网页 URL 转换为 Markdown 格式的纯文本，便于 LLM 处理。
*   **鉴权方式**: API Key (如有)

### 1.2 AI 分析与生成 (Analysis & Generation)
*   **服务商**: DeepSeek (deepseek-chat)
*   **接口地址**: `https://api.deepseek.com/v1/chat/completions`
*   **功能**:
    *   **摘要**: 对长篇新闻进行关键点提取。
    *   **翻译**: 将外文新闻翻译为中文。
    *   **改写**: 生成适合公众号/推特风格的短文。
*   **请求示例**:
    ```json
    {
      "model": "deepseek-chat",
      "messages": [{"role": "user", "content": "请总结以下新闻..."}]
    }
    ```

## 2. 内部数据模型 (Internal Data Schema)

### 2.1 新闻条目 (NewsItem)
用于存储单条新闻的原始信息和处理后的结果。

```json
{
  "id": "uuid-string",
  "source_url": "https://example.com/news/123",
  "title": "新闻标题",
  "publish_date": "2024-02-04T10:00:00Z",
  "content_raw": "原始网页文本...",
  "content_summary": "AI生成的摘要...",
  "tags": ["AI", "Tech", "Apple"],
  "status": "processed" // pending, processing, processed, failed
}
```

### 2.2 每日日报 (DailyReport)
用于生成最终发布的日报聚合内容。

```json
{
  "report_id": "20240204-daily",
  "date": "2024-02-04",
  "items": [
    {
      "title": "标题1",
      "summary": "摘要1",
      "link": "url1"
    },
    {
      "title": "标题2",
      "summary": "摘要2",
      "link": "url2"
    }
  ],
  "generated_markdown": "# 2024-02-04 AI 科技日报\n\n## 1. 标题1..."
}
```
