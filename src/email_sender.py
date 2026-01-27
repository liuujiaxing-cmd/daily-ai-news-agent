# src/email_sender.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from .config import SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, EMAIL_RECIPIENTS

class EmailSender:
    def __init__(self):
        self.server = SMTP_SERVER
        self.port = SMTP_PORT
        self.user = SMTP_USER
        self.password = SMTP_PASSWORD
        self.recipients = [r.strip() for r in EMAIL_RECIPIENTS if r.strip()]

    def send_report(self, html_content: str, title: str):
        """
        Send the HTML report via email
        """
        if not self.recipients:
            print("⚠️ No email recipients configured. Skipping email.")
            return

        if not self.user or not self.password:
            print("⚠️ SMTP credentials not configured. Skipping email.")
            return

        msg = MIMEMultipart()
        msg['From'] = f"AI Daily Agent <{self.user}>"
        msg['To'] = ", ".join(self.recipients)
        msg['Subject'] = f"🤖 {title} - {datetime.now().strftime('%Y-%m-%d')}"

        msg.attach(MIMEText(html_content, 'html'))

        try:
            print(f"📧 Sending email to {len(self.recipients)} recipients...")
            with smtplib.SMTP(self.server, self.port) as server:
                server.starttls()
                server.login(self.user, self.password)
                server.send_message(msg)
            print("✅ Email sent successfully!")
        except Exception as e:
            print(f"❌ Failed to send email: {e}")

if __name__ == "__main__":
    # Test
    sender = EmailSender()
    sender.send_report("<h1>Test Report</h1><p>This is a test.</p>", "Test Subject")
