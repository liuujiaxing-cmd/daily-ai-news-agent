# src/memory_manager.py
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict

MEMORY_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "history.json")

class MemoryManager:
    def __init__(self):
        self.memory_file = MEMORY_FILE
        self._ensure_data_dir()

    def _ensure_data_dir(self):
        """Ensure data directory exists"""
        dirname = os.path.dirname(self.memory_file)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        
        if not os.path.exists(self.memory_file):
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def load_history(self, days: int = 7) -> List[Dict]:
        """
        Load summary history from the last N days.
        """
        try:
            with open(self.memory_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
            
            # Filter by date
            cutoff = datetime.now() - timedelta(days=days)
            recent_history = []
            
            for entry in history:
                try:
                    entry_date = datetime.strptime(entry['date'], "%Y-%m-%d")
                    if entry_date >= cutoff:
                        recent_history.append(entry)
                except ValueError:
                    continue
            
            return recent_history
        except Exception as e:
            print(f"⚠️ Error loading memory: {e}")
            return []

    def save_summary(self, summary_data: Dict):
        """
        Save today's summary to history.
        """
        if not summary_data:
            return

        today = datetime.now().strftime("%Y-%m-%d")
        
        # Create a lightweight record
        record = {
            "date": today,
            "intro": summary_data.get("intro", ""),
            "top_stories": [
                {
                    "title": s["title"],
                    "summary": s["summary"]
                } for s in summary_data.get("top_stories", [])
            ]
        }

        try:
            # Load existing
            with open(self.memory_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
            
            # Remove existing entry for today if any (overwrite)
            history = [h for h in history if h['date'] != today]
            history.append(record)
            
            # Keep only last 30 days to avoid file growing too large
            if len(history) > 30:
                history = history[-30:]

            # Save
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
                
            print(f"💾 Summary saved to memory ({today})")
            
        except Exception as e:
            print(f"❌ Failed to save memory: {e}")

    def get_context_string(self, days: int = 3) -> str:
        """
        Format recent history as a string for LLM context.
        """
        recent = self.load_history(days)
        if not recent:
            return "No recent history available."

        context = "Recent AI News Context:\n"
        for entry in recent:
            context += f"--- {entry['date']} ---\n"
            context += f"Overview: {entry['intro']}\n"
            for story in entry['top_stories']:
                context += f"- {story['title']}: {story['summary']}\n"
            context += "\n"
        
        return context

if __name__ == "__main__":
    mm = MemoryManager()
    print(mm.get_context_string())
