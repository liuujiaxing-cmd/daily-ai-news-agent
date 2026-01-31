import os
import sys

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.email_sender import EmailSender

def test_send():
    # 1. Find the latest report
    output_dir = "output"
    if not os.path.exists(output_dir):
        print("❌ No output directory found.")
        return

    files = sorted([f for f in os.listdir(output_dir) if f.endswith('.html')], reverse=True)
    if not files:
        print("❌ No HTML reports found.")
        return

    latest_report = os.path.join(output_dir, files[0])
    print(f"📖 Reading latest report: {latest_report}")
    
    with open(latest_report, "r") as f:
        html_content = f.read()

    # 2. Send Email
    print("📧 Attempting to send email...")
    sender = EmailSender()
    
    # Force reload subscribers from file/env to be sure
    print(f"📋 Recipients list: {sender.recipients}")
    
    sender.send_report(html_content, "AI Daily Insight (Test)")

if __name__ == "__main__":
    test_send()
