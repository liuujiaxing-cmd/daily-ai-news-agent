import os
import sys
import argparse

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.email_sender import EmailSender

def add_subscriber_if_not_exists(email: str):
    """
    Check if email exists in subscribers.txt, if not, append it.
    """
    file_path = "subscribers.txt"
    if not os.path.exists(file_path):
        print("⚠️ subscribers.txt not found.")
        return

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f.readlines()]
    
    if email in lines:
        print(f"ℹ️ User {email} already exists in database. Skipping addition.")
        return
    
    # Append new user
    print(f"🆕 Adding new user {email} to database...")
    with open(file_path, "a") as f:
        f.write(f"{email}\n")
    print("✅ User added to subscribers.txt")

def send_welcome_email(user_email: str):
    """
    Send a welcome email with the latest report to a new subscriber.
    """
    # Step 0: Ensure user is in DB
    add_subscriber_if_not_exists(user_email)

    print(f"👋 Preparing welcome email for: {user_email}")

    # 1. Find the latest report
    output_dir = "output"
    if not os.path.exists(output_dir):
        print("❌ No output directory found. Please run main.py first.")
        return

    # Filter for standard HTML reports (not WeChat posts)
    files = sorted([f for f in os.listdir(output_dir) if f.endswith('.html') and 'ai_news_report' in f], reverse=True)
    
    if not files:
        print("❌ No HTML reports found.")
        return

    latest_report = os.path.join(output_dir, files[0])
    print(f"📖 Attaching latest report: {latest_report}")
    
    with open(latest_report, "r") as f:
        report_content = f.read()

    # 2. Construct Welcome Message (Prepend to report)
    welcome_header = f"""
    <div style="background-color: #e3f2fd; padding: 20px; border-radius: 8px; margin-bottom: 20px; border: 1px solid #90caf9;">
        <h2 style="color: #1565c0; margin-top: 0;">🎉 欢迎订阅 AI Daily News!</h2>
        <p>感谢您的订阅！我是您的 AI 情报助手。</p>
        <p>从明天开始，我将在每天早上 8:00 (北京时间) 为您准时送上全球最新的 AI 行业动态。</p>
        <p>为了让您先睹为快，这是<strong>今天的最新简报</strong>，请查收 👇</p>
        <p style="font-size: 12px; color: #666;">(建议将此邮箱设为星标联系人，防止进入垃圾箱)</p>
    </div>
    <hr style="border: 0; border-top: 1px solid #eee; margin: 30px 0;">
    """
    
    full_html = welcome_header + report_content

    # 3. Send Email
    print("📧 Sending email...")
    sender = EmailSender()
    
    # Override recipients to just this single user
    sender.recipients = [user_email]
    
    try:
        sender.send_report(full_html, "Welcome to AI Daily News! 🎉")
        print(f"✅ Welcome email sent to {user_email}!")
    except Exception as e:
        print(f"❌ Failed to send welcome email: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send welcome email to new subscriber")
    parser.add_argument("email", help="Email address of the new subscriber")
    args = parser.parse_args()
    
    if "@" not in args.email:
        print("❌ Invalid email address.")
        sys.exit(1)
        
    send_welcome_email(args.email)
