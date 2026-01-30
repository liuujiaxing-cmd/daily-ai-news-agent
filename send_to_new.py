import os
from src.email_sender import EmailSender

def send_to_new_subscribers():
    # New subscribers list
    new_subs = [
        "1308289476@qq.com"
    ]

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
    
    # OVERRIDE recipients list for this run only
    sender.recipients = new_subs
    print(f"📋 Targeted Recipients: {sender.recipients}")
    
    sender.send_report(html_content, "AI Daily Insight (New Subscriber Welcome)")

if __name__ == "__main__":
    send_to_new_subscribers()
