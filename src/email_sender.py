# src/email_sender.py
import smtplib
import os
import time
import resend
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from .config import SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, EMAIL_RECIPIENTS, BASE_DIR

class EmailSender:
    def __init__(self):
        self.server = SMTP_SERVER
        self.port = SMTP_PORT
        self.user = SMTP_USER
        self.password = SMTP_PASSWORD
        self.resend_key = os.getenv("RESEND_API_KEY")
        
        if self.resend_key:
            resend.api_key = self.resend_key
        
        # Load recipients: Priority File > Env Var
        self.recipients = self._load_subscribers()
        
    def _load_subscribers(self):
        """Load emails from subscribers.txt if exists, else from .env"""
        subs_file = os.path.join(BASE_DIR, "subscribers.txt")
        emails = []
        
        if os.path.exists(subs_file):
            try:
                with open(subs_file, "r") as f:
                    emails = [line.strip() for line in f if line.strip() and "@" in line and not line.startswith("#")]
            except Exception as e:
                print(f"Error reading subscribers.txt: {e}")
        
        # Fallback to .env
        if not emails:
            emails = [r.strip() for r in EMAIL_RECIPIENTS if r.strip()]
            
        return list(set(emails)) # Dedup

    def send_report(self, html_content: str, title: str):
        """
        Send the HTML report via Resend (Preferred) or SMTP
        """
        if not self.recipients:
            print("⚠️ No email recipients configured. Skipping email.")
            return

        subject = f"🤖 {title} - {datetime.now().strftime('%Y-%m-%d')}"

        # 1. Try Resend (If Configured)
        if self.resend_key:
            try:
                print(f"📧 Sending via Resend API to {len(self.recipients)} recipients...")
                # Resend supports bulk sending, but best practice is batching or BCC
                # Here we use 'bcc' field for privacy
                params = {
                    "from": "AI Daily Agent <onboarding@resend.dev>", # Default test domain
                    "to": ["delivered@resend.dev"], # Placeholder for 'To' field
                    "bcc": self.recipients,
                    "subject": subject,
                    "html": html_content
                }
                
                # If user has verified domain, use it
                if self.user and "@" in self.user and "gmail" not in self.user and "qq" not in self.user:
                     params["from"] = f"AI Daily Agent <{self.user}>"

                r = resend.Emails.send(params)
                print(f"✅ Email sent via Resend! ID: {r.get('id')}")
                return
            except Exception as e:
                print(f"⚠️ Resend failed: {e}. Falling back to SMTP...")

        # 2. Fallback to SMTP
        if not self.user or not self.password:
            print("⚠️ SMTP credentials not configured. Skipping email.")
            return

        msg = MIMEMultipart()
        msg['From'] = f"AI Daily Agent <{self.user}>"
        # Use BCC to hide recipients list
        msg['Subject'] = subject
        
        msg.attach(MIMEText(html_content, 'html'))

        # Retry logic
        max_retries = 3
        for attempt in range(max_retries):
            try:
                print(f"📧 Sending via SMTP to {len(self.recipients)} recipients (Attempt {attempt+1})...")
                with smtplib.SMTP(self.server, self.port) as server:
                    server.starttls()
                    server.login(self.user, self.password)
                    # Send to list (SMTP handles BCC automatically if not in 'To' header)
                    server.sendmail(self.user, self.recipients, msg.as_string())
                print("✅ Email sent successfully via SMTP!")
                return
            except Exception as e:
                print(f"❌ Failed to send email: {e}")
                if attempt < max_retries - 1:
                    time.sleep(5) # Wait before retry
                else:
                    print("❌ Max retries reached. Email sending failed.")

if __name__ == "__main__":
    # Test
    sender = EmailSender()
    sender.send_report("<h1>Test Report</h1><p>This is a test.</p>", "Test Subject")
