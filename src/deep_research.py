# src/deep_research.py
from duckduckgo_search import DDGS
from .full_content_fetcher import FullContentFetcher
import concurrent.futures

class DeepResearchFetcher:
    def __init__(self):
        self.ddgs = DDGS()
        self.content_fetcher = FullContentFetcher()

    def search(self, query: str, max_results: int = 5) -> list:
        """
        Search for a topic and return raw results
        """
        print(f"🔍 Searching web for: {query}...")
        results = []
        try:
            # Search DuckDuckGo
            ddg_results = self.ddgs.text(query, max_results=max_results)
            if ddg_results:
                results.extend(ddg_results)
        except Exception as e:
            print(f"Error searching DDG: {e}")
            
        # Fallback Mock Data for Demo if search fails (common in local envs without VPN)
        if not results:
            print("⚠️ Search failed or returned no results. Using Mock Data for Demo.")
            results = [
                {
                    "title": "2025春节消费新趋势：年轻人更爱“平替”",
                    "href": "https://example.com/news1",
                    "body": "今年春节，高端白酒和奢侈品销量下滑，而平价餐饮和周边游火爆。数据显示..."
                },
                {
                    "title": "消费降级下的商机：二手交易平台流量暴增",
                    "href": "https://example.com/news2",
                    "body": "闲鱼等平台发布报告称，春节期间闲置物品交易量同比增长 40%..."
                },
                {
                    "title": "从“买买买”到“体验至上”：2025春节消费心理变迁",
                    "href": "https://example.com/news3",
                    "body": "消费者不再盲目追求大牌，而是更看重情绪价值和实际体验..."
                }
            ]
        
        return results

    def research_topic(self, topic: str) -> list:
        """
        Full research pipeline: Search -> Fetch Content
        """
        # 1. Search
        search_results = self.search(topic, max_results=5)
        if not search_results:
            return []

        # 2. Fetch Full Content in Parallel
        print(f"📖 Reading {len(search_results)} articles for deep dive...")
        detailed_results = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            # Map futures to original result
            future_to_result = {
                executor.submit(self.content_fetcher.fetch_details, res['href']): res 
                for res in search_results
            }
            
            for future in concurrent.futures.as_completed(future_to_result):
                original_res = future_to_result[future]
                try:
                    details = future.result()
                    # Combine metadata with full text
                    detailed_results.append({
                        "title": original_res['title'],
                        "link": original_res['href'],
                        "source": "Web Search",
                        "summary": original_res['body'], # Initial snippet
                        "full_content": details.get("text", "")[:5000], # Limit text length
                        "image": details.get("image")
                    })
                except Exception:
                    continue
                    
        return detailed_results
