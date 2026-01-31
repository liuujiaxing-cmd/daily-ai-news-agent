import os
import re
import sys

# Add parent directory to sys.path to find files in docs/
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(PROJECT_ROOT)

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Preformatted
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register a font that supports Chinese (using system font or fallback)
# Note: On macOS, we can usually find PingFang or Arial Unicode. 
# For safety in this environment, we might need to use a standard font or try to load one.
# Since we can't easily download fonts, we will try to use a built-in one if available, 
# but ReportLab's default fonts don't support Chinese.
# WE MUST REGISTER A CHINESE FONT.
# I will try to use a common macOS font path.

FONT_PATH = "/System/Library/Fonts/PingFang.ttc"
FONT_NAME = "PingFang"

try:
    pdfmetrics.registerFont(TTFont(FONT_NAME, FONT_PATH))
except:
    try:
        # Fallback to another common font
        FONT_PATH = "/System/Library/Fonts/STHeiti Light.ttc"
        FONT_NAME = "STHeiti"
        pdfmetrics.registerFont(TTFont(FONT_NAME, FONT_PATH))
    except:
        print("⚠️ Warning: Could not load Chinese font. Output might contain tofu characters.")
        FONT_NAME = "Helvetica" # Fallback (no Chinese support)

def clean_manual_content(text):
    """Remove placeholders and reminders"""
    # Remove lines containing brackets like [此处插入...]
    lines = text.split('\n')
    cleaned = []
    for line in lines:
        if re.search(r'\[.*截图.*\]', line):
            continue
        cleaned.append(line)
    return '\n'.join(cleaned)

def create_source_code_pdf():
    input_file = os.path.join(PROJECT_ROOT, "docs", "source_code.txt")
    output_file = os.path.join(PROJECT_ROOT, "docs", "source_code.pdf")
    
    if not os.path.exists(input_file):
        print(f"❌ File not found: {input_file}")
        return

    doc = SimpleDocTemplate(output_file, pagesize=A4,
                            rightMargin=50, leftMargin=50,
                            topMargin=50, bottomMargin=50)
    
    styles = getSampleStyleSheet()
    code_style = ParagraphStyle(
        'Code',
        parent=styles['Code'],
        fontName=FONT_NAME,
        fontSize=8,
        leading=10,
        spaceAfter=0,
    )
    
    header_style = ParagraphStyle(
        'Header',
        parent=styles['Heading1'],
        fontName=FONT_NAME,
        fontSize=16,
        spaceAfter=20,
        alignment=TA_LEFT
    )

    story = []
    story.append(Paragraph("软件源代码", header_style))
    story.append(Spacer(1, 12))
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split content to avoid paragraph too large error
    lines = content.split('\n')
    chunk_size = 50 # lines per paragraph chunk
    
    for i in range(0, len(lines), chunk_size):
        chunk = '\n'.join(lines[i:i+chunk_size])
        # Escape HTML characters for ReportLab
        chunk = chunk.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        # Use Preformatted for code to preserve whitespace
        story.append(Preformatted(chunk, code_style))
    
    doc.build(story)
    print(f"✅ Generated: {output_file}")

def create_manual_pdf():
    input_file = os.path.join(PROJECT_ROOT, "docs", "user_manual.md")
    output_file = os.path.join(PROJECT_ROOT, "docs", "user_manual.pdf")
    
    if not os.path.exists(input_file):
        print(f"❌ File not found: {input_file}")
        return

    doc = SimpleDocTemplate(output_file, pagesize=A4,
                            rightMargin=50, leftMargin=50,
                            topMargin=50, bottomMargin=50)
    
    styles = getSampleStyleSheet()
    
    # Define styles with Chinese font
    normal_style = ParagraphStyle(
        'Normal_CN',
        parent=styles['Normal'],
        fontName=FONT_NAME,
        fontSize=10,
        leading=14,
        spaceAfter=6
    )
    
    h1_style = ParagraphStyle(
        'H1_CN',
        parent=styles['Heading1'],
        fontName=FONT_NAME,
        fontSize=18,
        leading=22,
        spaceAfter=12,
        spaceBefore=12
    )
    
    h2_style = ParagraphStyle(
        'H2_CN',
        parent=styles['Heading2'],
        fontName=FONT_NAME,
        fontSize=14,
        leading=18,
        spaceAfter=10,
        spaceBefore=10
    )
    
    story = []
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = clean_manual_content(content)
    
    for line in content.split('\n'):
        line = line.strip()
        if not line:
            continue
            
        if line.startswith('# '):
            story.append(Paragraph(line[2:], h1_style))
        elif line.startswith('## '):
            story.append(Paragraph(line[3:], h2_style))
        elif line.startswith('### '):
            # Treat h3 as bold normal text or smaller header
            story.append(Paragraph(f"<b>{line[4:]}</b>", normal_style))
        elif line.startswith('* ') or line.startswith('- '):
            # Bullet points
            story.append(Paragraph(f"• {line[2:]}", normal_style))
        else:
            story.append(Paragraph(line, normal_style))
            
    doc.build(story)
    print(f"✅ Generated: {output_file}")

if __name__ == "__main__":
    try:
        create_source_code_pdf()
        create_manual_pdf()
    except Exception as e:
        print(f"❌ Fatal Error: {e}")
