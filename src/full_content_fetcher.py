# src/full_content_fetcher.py
from newspaper import Article
from bs4 import BeautifulSoup
import requests
import concurrent.futures

class FullContentFetcher:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        }

    def fetch_details(self, url: str) -> dict:
        """
        Fetch full content and top image using newspaper3k/bs4
        """
        result = {
            "text": "",
            "image": None
        }
        
        try:
            # Method 1: Newspaper3k
            article = Article(url)
            article.download()
            article.parse()
            
            if article.text and len(article.text) > 200:
                result["text"] = article.text
            
            if article.top_image:
                result["image"] = article.top_image

            # Method 2: Fallback if text is empty or missing image
            if not result["text"] or not result["image"]:
                response = requests.get(url, headers=self.headers, timeout=10)
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Fallback Text
                if not result["text"]:
                    paragraphs = soup.find_all('p')
                    text = ' '.join([p.get_text() for p in paragraphs])
                    if len(text) > 100:
                        result["text"] = text

                # Fallback Image (og:image)
                if not result["image"]:
                    og_image = soup.find("meta", property="og:image")
                    if og_image and og_image.get("content"):
                        result["image"] = og_image["content"]

            return result
            
        except Exception as e:
            # print(f"Error fetching content for {url}: {e}")
            return result

    def enrich_news_items(self, news_items: list) -> list:
        """
        Parallel fetch full content and images for all news items
        """
        print(f"📖 Fetching full content & images for {len(news_items)} articles...")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            future_to_item = {
                executor.submit(self.fetch_details, item['link']): item 
                for item in news_items
            }
            
            for future in concurrent.futures.as_completed(future_to_item):
                item = future_to_item[future]
                try:
                    details = future.result()
                    
                    # Update Content
                    if details["text"] and len(details["text"]) > 200:
                        item['full_content'] = details["text"]
                    else:
                        item['full_content'] = item['summary'] # Fallback
                    
                    # Update Image
                    item['image'] = details["image"]
                        
                except Exception:
                    item['full_content'] = item['summary']
                    item['image'] = None
        
        return news_items
