
import json
from datetime import datetime
from duckduckgo_search import DDGS
from openai import OpenAI
from .config import OPENAI_API_KEY, OPENAI_BASE_URL, LLM_MODEL

class TopicManager:
    def __init__(self):
        self.ddgs = DDGS()
        self.client = OpenAI(
            api_key=OPENAI_API_KEY,
            base_url=OPENAI_BASE_URL
        )
        self.model = LLM_MODEL

    def get_trending_topics(self, count: int = 10) -> list:
        """
        Fetch trending topics from search and refine with LLM.
        """
        print(f"🔍 Fetching top {count} trending topics...")
        
        # 1. Search for trends
        try:
            query = f"today's top news and trending topics in China {datetime.now().strftime('%Y-%m-%d')}"
            results = self.ddgs.text(query, max_results=10)
            
            if not results:
                print("⚠️ Search returned empty, using fallback trends.")
                return self._get_fallback_topics(count)
                
            raw_text = "\n".join([f"- {r['title']}: {r['body']}" for r in results])
            
        except Exception as e:
            print(f"❌ Error fetching trends: {e}")
            return self._get_fallback_topics(count)

        # 2. Extract specific topics using LLM
        prompt = f"""
请根据以下搜索结果，提炼出 {count} 个当下中国互联网最热门、最适合做短视频（有争议、有流量、有新意）的话题。

搜索结果：
{raw_text}

要求：
1. 话题要具体（例如：“iPhone 16 销量暴跌” 而不是 “科技新闻”）。
2. 去重。
3. 返回纯 JSON 数组格式，不要 Markdown。

示例：
["话题1", "话题2", ...]
"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a social media trend analyst. Output JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            content = response.choices[0].message.content
            # Handle potential wrapper keys
            data = json.loads(content)
            if isinstance(data, list):
                topics = data
            elif "topics" in data:
                topics = data["topics"]
            else:
                # Try to find the first list in values
                topics = next((v for v in data.values() if isinstance(v, list)), [])
            
            # Fallback if parsing failed
            if not topics:
                return self._get_fallback_topics(count)
                
            return topics[:count]
            
        except Exception as e:
            print(f"❌ Error extracting topics: {e}")
            return self._get_fallback_topics(count)

    def _get_fallback_topics(self, count: int) -> list:
        """
        Fallback topics in case search fails.
        """
        defaults = [
            "2025春节档电影票房预测",
            "OpenAI o3 模型发布影响",
            "年轻人为何不爱换手机了",
            "新能源汽车价格战",
            "职场35岁危机真相",
            "预制菜进校园争议",
            "房地产市场最新政策解读",
            "大学生就业难现状",
            "董宇辉新号带货数据分析",
            "马斯克火星殖民计划更新"
        ]
        return defaults[:count]
