---
title: AI Daily News Agent
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: streamlit
sdk_version: 1.31.0
app_file: src/dashboard.py
pinned: false
license: mit
---

# 🤖 AI Daily News Agent

An intelligent, autonomous agent that fetches, analyzes, and summarizes the latest AI news from around the world.

## ✨ Features

- **Automated Fetching**: Aggregates news from 10+ sources including RSS feeds, Blogs, and Reddit.
- **Deep Understanding**: Uses **OpenAI/DeepSeek** to read full articles and extract key insights.
- **Context-Aware**: Remembers past events to provide continuous narrative summaries.
- **Deep Dive Mode (Pro)**: Performs on-demand deep research on specific topics (e.g., "DeepSeek Architecture").
- **Multi-Channel Delivery**:
  - 📊 **Web Dashboard**: Interactive Streamlit interface.
  - 📧 **Email**: Daily HTML digest.
  - 📱 **WeChat**: Ready-to-copy Markdown format.

## 🚀 Quick Start (Local)

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/daily_ai_news_agent.git
   cd daily_ai_news_agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   Create a `.env` file in the root directory:
   ```bash
   OPENAI_API_KEY=sk-xxxx
   OPENAI_BASE_URL=https://api.deepseek.com
   LLM_MODEL=deepseek-chat
   ```

4. **Run the Dashboard**
   ```bash
   streamlit run src/dashboard.py
   ```

## ☁️ Deploy to Streamlit Cloud

1. Fork this repository to your GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io/).
3. Connect your GitHub account and select this repository.
4. **Main file path**: `daily_ai_news_agent/src/dashboard.py` (Note: Adjust based on your repo structure).
5. **Advanced Settings**: Add your `OPENAI_API_KEY` and other secrets.
6. Click **Deploy**!

## 📂 Project Structure

```
daily_ai_news_agent/
├── src/
│   ├── main.py           # Core logic pipeline
│   ├── dashboard.py      # Streamlit Web UI
│   ├── fetcher.py        # RSS Fetching
│   ├── deep_research.py  # DuckDuckGo Search
│   ├── summarizer.py     # LLM Analysis
│   └── ...
├── templates/            # HTML Report Templates
├── output/               # Generated Reports
└── requirements.txt
```

## 📄 License

MIT
