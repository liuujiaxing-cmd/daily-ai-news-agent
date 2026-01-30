# src/reporter.py
import os
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from .config import REPORT_OUTPUT_DIR, TEMPLATE_DIR

class Reporter:
    def __init__(self):
        print(f"DEBUG: TEMPLATE_DIR = {TEMPLATE_DIR}")
        if not os.path.exists(TEMPLATE_DIR):
            print(f"ERROR: Template directory does not exist: {TEMPLATE_DIR}")
            
        self.env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
        try:
            self.template = self.env.get_template("report_template.html")
        except Exception as e:
            print(f"ERROR: Could not load template 'report_template.html' from {TEMPLATE_DIR}")
            print(f"Available files: {os.listdir(TEMPLATE_DIR) if os.path.exists(TEMPLATE_DIR) else 'Dir not found'}")
            raise e
        
        # Ensure output directory exists
        if not os.path.exists(REPORT_OUTPUT_DIR):
            os.makedirs(REPORT_OUTPUT_DIR)

    def generate_report(self, data: dict):
        """
        Generate HTML report from data
        """
        if not data:
            print("No data to report.")
            return

        current_time = datetime.now()
        now = current_time.strftime("%Y-%m-%d %H:%M:%S")
        try:
            html_content = self.template.render(data=data, generated_at=now)
        except Exception as e:
            print(f"Error rendering template: {e}")
            return

        filename = f"ai_news_report_{current_time.strftime('%Y%m%d_%H%M%S')}.html"
        filepath = os.path.join(REPORT_OUTPUT_DIR, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_content)
            
        print(f"Report generated successfully: {filepath}")
        return filepath

    def generate_wechat_html(self, data: dict):
        """
        Generate WeChat-optimized HTML report
        """
        if not data:
            return None
            
        try:
            template = self.env.get_template("wechat_template.html")
            
            # Prepare context for template
            context = {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "summary_intro": data.get("intro", ""),
                "hot_news": [],
                "other_news": []
            }
            
            # Process Top Stories
            for item in data.get("top_stories", []):
                context["hot_news"].append({
                    "title": item.get("title"),
                    "source": item.get("source"),
                    "image": item.get("image_url") or "", # Fallback logic in template?
                    "one_sentence_summary": item.get("summary"),
                    "key_points": item.get("key_points", []),
                    "insight": item.get("impact", "")
                })
                
            # Process Categories
            for cat, items in data.get("categories", {}).items():
                for item in items:
                    context["other_news"].append({
                        "title": item.get("title"),
                        "one_sentence_summary": item.get("summary"),
                        "source": item.get("source")
                    })
            
            html_content = template.render(**context)
            
            # Save file
            filename = f"wechat_post_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            filepath = os.path.join(REPORT_OUTPUT_DIR, filename)
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(html_content)
                
            print(f"✅ WeChat HTML ready: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"Error generating WeChat HTML: {e}")
            return None

    def generate_markdown(self, data: dict):
        """
        Generate Markdown report (optional, for simple text output)
        """
        if not data:
            return ""

        md = f"# {data.get('title', 'AI News Report')}\n\n"
        md += f"**{data.get('intro', '')}**\n\n"
        
        md += "## 🔥 Top Stories\n"
        for story in data.get('top_stories', []):
            md += f"### [{story['title']}]({story['link']})\n"
            md += f"**Source:** {story['source']}\n\n"
            md += f"{story['summary']}\n\n"
            if 'impact' in story:
                md += f"> 💡 {story['impact']}\n\n"
        
        for category, stories in data.get('categories', {}).items():
            if stories:
                md += f"## {category}\n"
                for story in stories:
                    md += f"- **[{story['title']}]({story['link']})** ({story['source']}): {story['summary']}\n"
                md += "\n"
        
        # --- Disclaimer ---
        md += "\n---\n"
        md += "### ⚠️ 免责声明\n"
        md += "本报告由 AI 自动生成，内容仅供参考。投资者应自行承担风险。本文不构成任何投资建议。\n"
        # ------------------

        return md

    def generate_wechat_markdown(self, data: dict):
        """
        Generate WeChat Official Account friendly Markdown
        """
        if not data:
            return ""

        today = datetime.now().strftime("%Y-%m-%d")
        
        md = f"# 🤖 AI 每日早报 ({today})\n\n"
        md += f"{data.get('intro', '')}\n\n"
        md += "---\n\n"
        
        # 1. Top Stories (Detailed)
        md += "## 🔥 今日热点\n\n"
        for i, story in enumerate(data.get('top_stories', []), 1):
            title = story['title']
            # WeChat formatting: Bold Title with Emoji
            md += f"### {i}. {title}\n"
            md += f"**来源**: {story['source']}\n\n"
            md += f"{story['summary']}\n\n"
            
            # Key Points (Bullet list)
            if story.get('key_points'):
                md += "**核心要点**:\n"
                for point in story['key_points']:
                    md += f"- {point}\n"
                md += "\n"
                
            if 'impact' in story:
                md += f"> 💡 **深度洞察**: {story['impact']}\n\n"
            
            md += f"🔗 [原文链接]({story['link']})\n\n"
        
        # 2. Categories (Brief)
        for category, stories in data.get('categories', {}).items():
            if stories:
                md += f"## 📂 {category}\n\n"
                for story in stories:
                    md += f"- **{story['title']}**\n"
                    md += f"  {story['summary']} ([{story['source']}]({story['link']}))\n"
                md += "\n"
        
        md += "---\n"
        md += "*本报告由 AI Agent 自动生成，内容仅供参考。*\n"
        md += "*免责声明：本文不构成任何投资建议，请独立判断。*\n" # Disclaimer
        
        return md

if __name__ == "__main__":
    # Test
    mock_data = {
        "title": "AI Daily Test",
        "intro": "Nothing much happened today.",
        "top_stories": [
            {"title": "Test Story 1", "link": "#", "source": "Test", "summary": "This is a test summary.", "impact": "Huge impact."}
        ],
        "categories": {
            "Other": [{"title": "Small Story", "link": "#", "source": "Test", "summary": "Small summary."}]
        }
    }
    reporter = Reporter()
    reporter.generate_report(mock_data)
