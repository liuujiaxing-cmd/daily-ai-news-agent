# src/config.py
import os
from dotenv import load_dotenv

# Load .env from project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

# RSS Feeds List
RSS_FEEDS = {
    # --- 英文主流 ---
    "OpenAI Blog": "https://openai.com/blog/rss.xml",
    "Google DeepMind": "https://deepmind.google/blog/rss.xml",
    "Microsoft Research": "https://www.microsoft.com/en-us/research/feed/",
    "Hugging Face Blog": "https://huggingface.co/blog/feed.xml",
    "TechCrunch AI": "https://techcrunch.com/category/artificial-intelligence/feed/",
    "The Verge AI": "https://www.theverge.com/rss/ai/index.xml",
    "MIT Technology Review AI": "https://www.technologyreview.com/topic/artificial-intelligence/feed",
    "Reddit Machine Learning": "https://www.reddit.com/r/MachineLearning/.rss",
    
    # --- 中文深度 ---
    "机器之心": "https://www.jiqizhixin.com/rss",
    "量子位": "https://www.qbitai.com/feed",
}

# LLM Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o")

# Email Configuration
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
EMAIL_RECIPIENTS = os.getenv("EMAIL_RECIPIENTS", "").split(",")

# Report Configuration
REPORT_OUTPUT_DIR = os.path.join(BASE_DIR, "output")
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
