# src/scheduler.py
import schedule
import time
import sys
import os
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.main import run_daily_job

def job():
    print(f"\n⏰ Scheduled job started at {datetime.now()}")
    try:
        run_daily_job(hours=24)
    except Exception as e:
        print(f"❌ Job failed: {e}")
    print(f"✅ Job finished at {datetime.now()}\n")

if __name__ == "__main__":
    print("🤖 AI News Agent Scheduler is running...")
    print("📅 Schedule: Daily at 08:00")
    
    # Schedule the job every day at 08:00
    schedule.every().day.at("08:00").do(job)
    
    # Also run once immediately on startup for verification (optional)
    # job()

    while True:
        schedule.run_pending()
        time.sleep(60)
