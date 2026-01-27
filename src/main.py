# src/main.py
import argparse
import os
import sys

# Add current directory to path so imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.fetcher import NewsFetcher
from src.full_content_fetcher import FullContentFetcher
from src.summarizer import NewsSummarizer
from src.reporter import Reporter
from src.email_sender import EmailSender

def run_daily_job(hours=24):
    print("🚀 Starting Daily AI News Agent...")
    
    # 1. Fetch RSS
    try:
        fetcher = NewsFetcher()
        news_items = fetcher.fetch_all(hours_back=hours)
        if not news_items:
            print("No news found in the specified time range.")
            return
    except Exception as e:
        print(f"Error fetching news: {e}")
        return

    # 2. Enrich with Full Content
    try:
        content_fetcher = FullContentFetcher()
        news_items = content_fetcher.enrich_news_items(news_items)
    except Exception as e:
        print(f"Error enriching news content: {e}")
    
    # 3. Summarize
    try:
        print("🧠 Analyzing and summarizing news (this may take a moment)...")
        summarizer = NewsSummarizer()
        summary_data = summarizer.summarize(news_items)
        if not summary_data:
            print("Failed to generate summary.")
            return
    except Exception as e:
        print(f"Error summarizing news: {e}")
        return

    # 4. Report & Email
    try:
        print("📝 Generating report...")
        reporter = Reporter()
        report_path = reporter.generate_report(summary_data)
        
        # Read HTML content for email
        with open(report_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # Send Email
        # print("📧 Sending email report...")
        # email_sender = EmailSender()
        # email_sender.send_report(html_content, summary_data.get('title', 'AI Daily News'))

        # Also print a quick markdown summary to console
        md_summary = reporter.generate_markdown(summary_data)
        wechat_md = reporter.generate_wechat_markdown(summary_data)
        
        print("\n" + "="*50)
        print("📱 微信公众号版本 (可直接复制):")
        print(wechat_md)
        print("="*50 + "\n")
        
        if report_path:
            print(f"✅ Report ready: {report_path}")
            # Try to open the report automatically on macOS
            if sys.platform == 'darwin':
                os.system(f"open '{report_path}'")
                
    except Exception as e:
        print(f"Error generating report: {e}")

def main():
    parser = argparse.ArgumentParser(description="Daily AI News Agent")
    parser.add_argument("--hours", type=int, default=24, help="Fetch news from the last N hours (default: 24)")
    args = parser.parse_args()
    run_daily_job(args.hours)

if __name__ == "__main__":
    main()
