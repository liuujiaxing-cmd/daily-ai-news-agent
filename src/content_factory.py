
import os
import argparse
import time
from datetime import datetime
from src.deep_research import DeepResearchFetcher
from src.summarizer import NewsSummarizer
from src.topic_manager import TopicManager
from src.config import REPORT_OUTPUT_DIR

def generate_content_for_topic(topic: str, output_base_dir: str = REPORT_OUTPUT_DIR):
    """
    Automated Content Factory:
    Topic -> Deep Research -> Report -> Viral PPT -> TikTok Script
    """
    print(f"\n🚀 [START] Processing topic: {topic}")
    
    # Initialize agents
    researcher = DeepResearchFetcher()
    summarizer = NewsSummarizer()
    
    # Create topic-specific folder
    safe_topic = "".join([c for c in topic if c.isalnum() or c in (' ', '-', '_')]).strip()[:50]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    topic_dir = os.path.join(output_base_dir, f"{timestamp}_{safe_topic}")
    if not os.path.exists(topic_dir):
        os.makedirs(topic_dir)
    
    # 1. Deep Research
    print("   [Phase 1] Deep Researching...")
    research_data = researcher.research_topic(topic)
    if not research_data:
        print(f"   ❌ No data found for '{topic}'. Skipping.")
        return

    # 2. Generate Deep Report (The Base Material)
    print("   [Phase 2] Generating Base Report...")
    report_content = summarizer.generate_deep_report(topic, research_data)
    
    report_path = os.path.join(topic_dir, "1_report.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content)
    print(f"   ✅ Report saved.")

    # 3. Generate Viral PPT (Marp)
    print("   [Phase 3] Generating Viral PPT...")
    ppt_content = summarizer.generate_marp_slides(topic, report_content, style="viral")
    
    ppt_path = os.path.join(topic_dir, "2_viral_slides.md")
    with open(ppt_path, "w", encoding="utf-8") as f:
        f.write(ppt_content)
    print(f"   ✅ PPT Code saved.")
    
    # 4. Generate Video Script (TikTok)
    print("   [Phase 4] Generating TikTok Script...")
    script_content = summarizer.generate_video_script(topic, report_content, platform="tiktok")
    
    script_path = os.path.join(topic_dir, "3_tiktok_script.txt")
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(script_content)
    print(f"   ✅ Video Script saved.")
    
    print(f"🎉 [DONE] Content ready in: {topic_dir}")

def run_daily_batch(limit: int = 10):
    """
    Fetch trending topics and run content factory for each.
    """
    print(f"🔥 Starting Daily Batch Run (Limit: {limit})")
    
    tm = TopicManager()
    topics = tm.get_trending_topics(count=limit)
    
    print(f"📋 Today's Topics: {topics}")
    
    for i, topic in enumerate(topics, 1):
        print(f"\n----------------------------------------")
        print(f"Processing {i}/{len(topics)}: {topic}")
        try:
            generate_content_for_topic(topic)
        except Exception as e:
            print(f"❌ Error processing '{topic}': {e}")
        
        # Avoid rate limits
        time.sleep(2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Viral Content Factory")
    parser.add_argument("--mode", type=str, default="single", choices=["single", "batch"], help="Mode: single or batch")
    parser.add_argument("--topic", type=str, help="Topic for single mode")
    parser.add_argument("--limit", type=int, default=10, help="Limit for batch mode")
    
    args = parser.parse_args()
    
    if args.mode == "batch":
        run_daily_batch(limit=args.limit)
    else:
        topic = args.topic if args.topic else "2025年春节消费降级现象与机会"
        generate_content_for_topic(topic)
