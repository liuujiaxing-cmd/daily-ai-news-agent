# src/summarizer.py
import json
import concurrent.futures
from typing import List, Dict
from openai import OpenAI
from .config import OPENAI_API_KEY, OPENAI_BASE_URL, LLM_MODEL, TOKEN_SAVING_MODE

from .preferences import USER_INTERESTS, USER_DISLIKES
from .memory_manager import MemoryManager

class NewsSummarizer:
    def __init__(self):
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not found in environment variables.")
        
        self.client = OpenAI(
            api_key=OPENAI_API_KEY,
            base_url=OPENAI_BASE_URL
        )
        self.model = LLM_MODEL
        self.memory = MemoryManager()

    def batch_filter_articles(self, news_items: List[Dict]) -> List[Dict]:
        """
        [Filter Step] Use a single cheap LLM call to filter out irrelevant news by title.
        """
        if not news_items:
            return []
            
        print(f"🔍 [Token Saving] Batch filtering {len(news_items)} articles by title...")
        
        # Prepare list for prompt
        titles_text = ""
        for i, item in enumerate(news_items):
            titles_text += f"{i}. {item['title']} (Source: {item['source']})\n"
            
        prompt = f"""
请作为一名严格的 AI 新闻编辑，从以下列表中筛选出**真正重要**且**符合用户兴趣**的新闻。

用户兴趣: {", ".join(USER_INTERESTS)}
不感兴趣: {", ".join(USER_DISLIKES)}

筛选标准：
1. 必须是 AI 领域的**重大**进展、新模型发布、重要研究或商业大事件。
2. 剔除：教程类("How to")、过于细分的每日论文、无关的推广、重复的报道。
3. 严格控制数量，只保留最有价值的前 30%-50%。

新闻列表：
{titles_text}

请仅输出保留的新闻编号列表，格式如 JSON：
{{
    "keep_indices": [0, 2, 5, ...]
}}
"""
        try:
            response = self.client.chat.completions.create(
                model=self.model, # Can use a cheaper model here if available
                messages=[
                    {"role": "system", "content": "You are a strict news editor. Output JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            result = json.loads(response.choices[0].message.content)
            keep_indices = set(result.get("keep_indices", []))
            
            filtered_items = [item for i, item in enumerate(news_items) if i in keep_indices]
            print(f"📉 Filtered down to {len(filtered_items)} items (from {len(news_items)})")
            return filtered_items
            
        except Exception as e:
            print(f"⚠️ Filter failed, keeping all items: {e}")
            return news_items

    def analyze_single_article(self, item: Dict) -> Dict:
        """
        [Map Step] Analyze a single article's full content to extract key insights.
        """
        # Truncate content if too long to save tokens
        content = item.get('full_content', item.get('summary', ''))[:3000]
        
        prompt = f"""
请分析以下 AI 新闻内容，提取关键信息。

用户偏好（请据此调整 importance_score）：
- 重点关注: {", ".join(USER_INTERESTS)}
- 忽略或低分: {", ".join(USER_DISLIKES)}

标题：{item['title']}
来源：{item['source']}
内容：
{content}

请输出 JSON 格式（不要 Markdown 标记）：
{{
    "title_zh": "中文标题",
    "summary_zh": "中文摘要（50字以内）",
    "key_points": ["关键点1", "关键点2", "关键点3"],
    "category": "模型/行业/学术/应用/其他",
    "importance_score": 1-10 (符合用户兴趣的给高分，无关的给低分),
    "impact_analysis": "一句话分析其对行业的影响"
}}
"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an AI analyst. Output raw JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            analysis = json.loads(response.choices[0].message.content)
            
            # Merge analysis back into item
            item.update(analysis)
            return item
        except Exception as e:
            # print(f"Error analyzing {item['title']}: {e}")
            return item

    def summarize(self, news_items: List[Dict]) -> Dict:
        """
        [Reduce Step] Aggregate analyzed items into a final report.
        """
        if not news_items:
            return {}

        # 0. Pre-filtering (Token Saving)
        if TOKEN_SAVING_MODE and len(news_items) > 5:
            news_items = self.batch_filter_articles(news_items)

        # 1. Map: Parallel analysis of each article
        print(f"🧠 Analyzing {len(news_items)} articles in depth...")
        analyzed_items = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(self.analyze_single_article, item) for item in news_items]
            for future in concurrent.futures.as_completed(futures):
                try:
                    analyzed_items.append(future.result())
                except Exception:
                    pass

        # 2. Filter & Sort
        # Filter out low quality items (importance < 4) or errors
        valid_items = [i for i in analyzed_items if i.get('importance_score', 0) >= 4]
        valid_items.sort(key=lambda x: x.get('importance_score', 0), reverse=True)

        # 3. Reduce: Generate final structure
        top_stories = []
        categories = {
            "模型与技术": [],
            "行业与商业": [],
            "学术与研究": [],
            "工具与应用": [],
            "其他": []
        }

        # Pick top 5
        for i, item in enumerate(valid_items):
            story_data = {
                "title": item.get('title_zh', item['title']),
                "summary": item.get('summary_zh', item['summary']),
                "source": item['source'],
                "link": item['link'],
                "image": item.get('image'),
                "impact": item.get('impact_analysis', ''),
                "key_points": item.get('key_points', [])
            }

            if i < 5:
                top_stories.append(story_data)
            else:
                cat = item.get('category', '其他')
                # Map LLM category to our fixed keys
                target_cat = "其他"
                if "模型" in cat or "技术" in cat: target_cat = "模型与技术"
                elif "行业" in cat or "商业" in cat: target_cat = "行业与商业"
                elif "学术" in cat or "研究" in cat: target_cat = "学术与研究"
                elif "应用" in cat or "工具" in cat: target_cat = "工具与应用"
                
                categories[target_cat].append(story_data)

        # Generate Intro using Top Stories + Memory Context
        history_context = self.memory.get_context_string(days=3)
        
        intro_prompt = f"""
请根据以下今日头条新闻，结合过去几天的历史背景，生成一句简短的今日 AI 行业动态综述。

历史背景（仅作参考，无需强行关联）：
{history_context}

今日头条：
{[t['title'] for t in top_stories]}

要求：简练、专业，突出连续性（如果有）。
"""
        try:
            intro_resp = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": intro_prompt}]
            )
            intro_text = intro_resp.choices[0].message.content.strip()
        except:
            intro_text = "今日 AI 领域有多项重要更新。"

        final_summary = {
            "title": f"AI Daily Insight ({valid_items[0]['published'][:10] if valid_items else ''})",
            "intro": intro_text,
            "top_stories": top_stories,
            "categories": categories
        }
        
        # Save to memory
        self.memory.save_summary(final_summary)
        
        return final_summary

    def generate_deep_report(self, topic: str, research_data: list) -> str:
        """
        Generate a long-form deep dive report based on research data.
        """
        context = ""
        for i, item in enumerate(research_data):
            context += f"--- Source {i+1}: {item['title']} ---\n"
            context += f"{item['full_content'][:2000]}\n\n"

        prompt = f"""
请根据以下收集到的资料，撰写一份关于 "{topic}" 的深度行业研报。

资料库：
{context}

要求：
1. 结构清晰：包含【背景与现状】、【核心技术/事件解析】、【市场竞争格局】、【未来趋势预测】四个章节。
2. 深度分析：不要简单的堆砌资料，要进行逻辑串联和观点提炼。
3. 数据支撑：引用资料中的关键数据。
4. 篇幅：1500字左右。
5. 格式：Markdown。
"""
        try:
            print(f"🧠 Generating deep dive report for '{topic}'...")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a senior AI industry analyst."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating report: {e}"

    def generate_marp_slides(self, topic: str, report_content: str, style: str = "academic") -> str:
        """
        Convert a deep dive report into a Marp-formatted slide deck.
        Style options: 'academic' (default, strict), 'viral' (for social media/business).
        """
        
        if style == "viral":
            # Commercial/Viral Style
            theme_instruction = "theme: uncover" # A more modern/visual theme
            style_instruction = """
            3. **风格**：
               - 极具视觉冲击力，适合社交媒体传播。
               - 标题要夸张、吸引眼球（Clickbait风格）。
               - 每一页字数要少，重点突出金句。
               - **不要**包含 Methodology 页。
               - **不要**写汇报人名字。
            """
        else:
            # Default Academic Style (User Preference)
            theme_instruction = "theme: gaia"
            style_instruction = """
            3. **风格**：专业、学术、极简。
            4. **特殊要求**：
               - 包含 "Methodology" 页（简述研究方法：PICO分析/广度搜索+深度综合）。
               - 封面页汇报人必须写：刘佳兴。
               - 禁止使用占位符，必须描述具体的图表内容。
            """

        prompt = f"""
请将以下深度研报内容转换为 Marp (Markdown Presentation Ecosystem) 格式的 PPT 代码。

研报主题：{topic}
研报内容：
{report_content[:3000]}... (截取部分内容)

要求：
1. **格式**：必须是标准的 Marp Markdown 格式。
   - 头部包含 `marp: true`, `{theme_instruction}`, `paginate: true`。
   - 每页幻灯片用 `---` 分隔。
2. **结构**：
   - 封面页：标题、副标题。
   - 目录页。
   - 正文页：提炼关键点，使用列表。
   - 结束页。
{style_instruction}
5. **语言**：中文。

输出示例：
---
marp: true
{theme_instruction}
paginate: true
---

# 标题
## 副标题

---
...
"""
        try:
            print(f"🎨 Generating Marp slides for '{topic}' (Style: {style})...")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a presentation expert skilled in Marp markdown."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5 if style == "viral" else 0.3
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating slides: {e}"

    def generate_video_script(self, topic: str, report_content: str, platform: str = "tiktok") -> str:
        """
        Generate a short video script based on the report.
        """
        prompt = f"""
请将以下深度研报内容改编为一个适合 {platform} (抖音/TikTok/小红书) 的短视频口播文案。

主题：{topic}
参考内容：
{report_content[:2000]}

要求：
1. **黄金前三秒**：开头必须有一个极其抓人的钩子（Hook），引发好奇或焦虑。
2. **口语化**：完全大白话，不要书面语，多用“家人们”、“注意看”、“绝了”等连接词（视平台风格而定）。
3. **分镜描述**：左侧写【画面建议】，右侧写【口播文案】。
4. **时长**：控制在 60-90 秒（约 200-300 字）。
5. **结尾**：引导关注/点赞/评论。

输出格式示例：
【画面：主播震惊脸，背景放相关新闻截图】
文案：天呐，这件事如果真的发生了，我们所有人的钱袋子都要缩水！

【画面：展示数据图表，箭头指向关键下降趋势】
文案：大家看这张图，短短三天...
"""
        try:
            print(f"🎬 Generating video script for '{topic}'...")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a viral content creator."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7 
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating script: {e}"
