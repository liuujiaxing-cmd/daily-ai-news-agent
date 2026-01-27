# src/fetcher.py
import feedparser
import time
import requests
import concurrent.futures
from datetime import datetime, timedelta
from typing import List, Dict
from .config import RSS_FEEDS

class NewsFetcher:
    def __init__(self):
        self.feeds = RSS_FEEDS
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Accept': 'application/rss+xml, application/xml, application/atom+xml, text/xml;q=0.9, */*;q=0.8',
            'Referer': 'https://www.google.com/'
        }

    def parse_time(self, time_struct):
        """Convert time_struct to datetime object"""
        if not time_struct:
            return datetime.now()
        return datetime.fromtimestamp(time.mktime(time_struct))

    def fetch_feed(self, source_info):
        """Fetch single feed with error handling"""
        source_name, feed_url = source_info
        news_items = []
        
        try:
            # print(f"Checking {source_name}...")
            response = requests.get(feed_url, headers=self.headers, timeout=15)
            response.encoding = 'utf-8'
            
            if response.status_code != 200:
                print(f"❌ {source_name}: Status {response.status_code}")
                return []

            feed = feedparser.parse(response.text)
            
            # if feed.bozo:
            #     print(f"⚠️ {source_name}: Parse warning ({feed.bozo_exception})")

            cutoff_time = datetime.now() - timedelta(hours=self.hours_back)
            
            for entry in feed.entries:
                published_parsed = getattr(entry, 'published_parsed', None) or getattr(entry, 'updated_parsed', None)
                published_dt = self.parse_time(published_parsed)

                if published_dt >= cutoff_time:
                    news_items.append({
                        "title": entry.title,
                        "link": entry.link,
                        "summary": getattr(entry, 'summary', getattr(entry, 'description', '')),
                        "source": source_name,
                        "published": published_dt.strftime("%Y-%m-%d %H:%M:%S"),
                        "raw_date": published_dt
                    })
            
            if news_items:
                print(f"✅ {source_name}: Found {len(news_items)} items")
            else:
                print(f"⚪ {source_name}: No new items")
                
            return news_items

        except Exception as e:
            print(f"❌ {source_name}: Error ({str(e)[:50]}...)")
            return []

    def fetch_all(self, hours_back: int = 24) -> List[Dict]:
        """
        Fetch news from all configured RSS feeds in parallel
        """
        self.hours_back = hours_back
        all_news = []
        
        print(f"🚀 Fetching news from {len(self.feeds)} sources (last {hours_back} hours)...")

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            # Submit all tasks
            future_to_source = {
                executor.submit(self.fetch_feed, (name, url)): name 
                for name, url in self.feeds.items()
            }
            
            for future in concurrent.futures.as_completed(future_to_source):
                try:
                    items = future.result()
                    all_news.extend(items)
                except Exception as e:
                    print(f"Error processing feed result: {e}")

        # Sort by date (newest first)
        all_news.sort(key=lambda x: x['raw_date'], reverse=True)
        
        # Remove raw_date object before returning
        for item in all_news:
            del item['raw_date']

        print(f"📊 Total {len(all_news)} news items collected.")
        return all_news

if __name__ == "__main__":
    fetcher = NewsFetcher()
    news = fetcher.fetch_all(hours_back=48)
