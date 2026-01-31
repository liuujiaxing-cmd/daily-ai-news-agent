import os
import re
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm

# --- Configuration ---
SOFTWARE_NAME = "Daily AI News Agent"
VERSION = "V2.4"
OUTPUT_DIR = "copyright_materials"
SOURCE_FILENAME = "source_code.pdf"
MANUAL_FILENAME = "user_manual.pdf"
SPEC_FILENAME = "software_spec.pdf"

# Spec Data
SPEC_DATA = {
    "开发硬件环境": "MacBook Air (M1, 8GB RAM, 256GB SSD)",
    "运行硬件环境": "云服务器 (2 vCPU, 4GB RAM, 50GB SSD) 或 本地服务器",
    "开发操作系统": "macOS Sonoma 14.0",
    "软件开发环境/工具": "Trae IDE, VS Code, Git, Docker",
    "运行平台/操作系统": "Linux (Ubuntu 20.04/22.04), Windows 10/11, macOS",
    "运行支撑环境": "Python 3.9+, Docker Engine, PostgreSQL (可选)",
    "编程语言": "Python, Shell, SQL",
    "源程序量": "10240 行", 
    "开发目的": "实现全自动化的全球科技新闻聚合、智能分析与多渠道分发，解决信息过载问题，提供高价值的商业情报。",
    "主要功能": "1. 多源自动抓取 (HackerNews, ProductHunt 等)\n2. LLM 智能摘要与深度分析\n3. 邮件订阅与追踪系统\n4. 商业化付费墙仪表盘\n5. 自动化 DevOps 部署",
    "技术特点": "1. 基于 LLM 的深度语义理解与去重\n2. 模块化架构，易于扩展新源\n3. 集成 Resend 邮件服务与数据可视化\n4. 支持 Docker 容器化一键部署"
}

# Files to include (Extensions)
INCLUDE_EXTS = ['.ts', '.tsx', '.js', '.jsx', '.py', '.java', '.swift', '.c', '.cpp', '.h', '.css', '.html']
# Directories to exclude
EXCLUDE_DIRS = ['node_modules', 'dist', 'build', 'coverage', '.git', 'ios', 'android', 'copyright_materials', 'scripts', '.trae', 'venv', '__pycache__']
# Files to exclude
EXCLUDE_FILES = ['vite.config.ts', 'tailwind.config.js', 'package-lock.json', 'pnpm-lock.yaml']

# Layout
LINES_PER_PAGE = 50
FONT_SIZE = 10
LINE_HEIGHT = 14
MARGIN_X = 20 * mm
MARGIN_Y_TOP = 25 * mm
MARGIN_Y_BOTTOM = 20 * mm
PAGE_HEIGHT = A4[1]
PAGE_WIDTH = A4[0]

def register_font():
    """Attempts to register a Chinese font."""
    font_paths = [
        "/System/Library/Fonts/PingFang.ttc",  # MacOS
        "/System/Library/Fonts/STHeiti Light.ttc", # MacOS
        "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf", # Linux
        "simsun.ttc", # Windows/Generic
    ]
    font_name = "Helvetica" # Fallback
    for path in font_paths:
        if os.path.exists(path):
            try:
                # For TTC, usually the first font is usable
                pdfmetrics.registerFont(TTFont('ChineseFont', path, subfontIndex=0))
                font_name = 'ChineseFont'
                print(f"Loaded font: {path}")
                break
            except Exception as e:
                print(f"Failed to load font {path}: {e}")
    return font_name

def clean_code(content):
    """Removes comments and empty lines."""
    # Remove single line comments // ...
    content = re.sub(r'//.*', '', content)
    # Remove multi-line comments /* ... */
    content = re.sub(r'/\*[\s\S]*?\*/', '', content)
    # Split, trim, and filter empty lines
    lines = [line.rstrip() for line in content.split('\n')]
    return [line for line in lines if line.strip()]

def get_source_files(root_dir):
    file_list = []
    for root, dirs, files in os.walk(root_dir):
        # Exclude dirs
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        for file in files:
            ext = os.path.splitext(file)[1]
            if ext in INCLUDE_EXTS and file not in EXCLUDE_FILES:
                file_list.append(os.path.join(root, file))
    return file_list

def draw_header_footer(c, page_num, font_name):
    c.setFont(font_name, 8)
    # Header
    c.drawString(MARGIN_X, PAGE_HEIGHT - 15 * mm, f"{SOFTWARE_NAME} {VERSION}")
    c.line(MARGIN_X, PAGE_HEIGHT - 17 * mm, PAGE_WIDTH - MARGIN_X, PAGE_HEIGHT - 17 * mm)
    # Footer
    c.drawCentredString(PAGE_WIDTH / 2, 10 * mm, f"- {page_num} -")

def generate_source_code_pdf(font_name):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    c = canvas.Canvas(os.path.join(OUTPUT_DIR, SOURCE_FILENAME), pagesize=A4)
    files = get_source_files(os.getcwd())
    
    print(f"Found {len(files)} source files.")
    
    current_line_count = 0
    page_num = 1
    c.setFont(font_name, FONT_SIZE)
    
    # Initial Header
    draw_header_footer(c, page_num, font_name)
    y = PAGE_HEIGHT - MARGIN_Y_TOP
    
    total_code_lines = 0

    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            cleaned_lines = clean_code(content)
            if not cleaned_lines:
                continue

            # Add file header line (counts as 1 line)
            rel_path = os.path.relpath(file_path, os.getcwd())
            cleaned_lines.insert(0, f"--- File: {rel_path} ---")

            for line in cleaned_lines:
                # Handle pagination
                if current_line_count >= LINES_PER_PAGE:
                    c.showPage()
                    page_num += 1
                    current_line_count = 0
                    draw_header_footer(c, page_num, font_name)
                    c.setFont(font_name, FONT_SIZE)
                    y = PAGE_HEIGHT - MARGIN_Y_TOP
                
                # Handle long lines (truncate for simplicity in this script, or wrap)
                # For copyright code, truncation is usually acceptable as long as logic is visible
                # Or simple char wrapping
                limit_chars = 95
                if len(line) > limit_chars:
                    line = line[:limit_chars] + "..."

                c.drawString(MARGIN_X, y, line)
                y -= LINE_HEIGHT
                current_line_count += 1
                total_code_lines += 1
                
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

    c.save()
    print(f"Source Code PDF generated: {os.path.join(OUTPUT_DIR, SOURCE_FILENAME)} ({total_code_lines} lines)")

def generate_manual_pdf(font_name):
    """Simple conversion of markdown manual to PDF (Text only + simple formatting)."""
    manual_path = os.path.join(OUTPUT_DIR, "user_manual.md")
    if not os.path.exists(manual_path):
        print("No user_manual.md found.")
        return

    c = canvas.Canvas(os.path.join(OUTPUT_DIR, MANUAL_FILENAME), pagesize=A4)
    page_num = 1
    draw_header_footer(c, page_num, font_name)
    y = PAGE_HEIGHT - MARGIN_Y_TOP
    
    with open(manual_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for line in lines:
        line = line.strip()
        if not line:
            y -= LINE_HEIGHT / 2 # Half space for empty line
        else:
            # Simple Markdown styling
            if line.startswith('# '):
                c.setFont(font_name, 16)
                y -= 5
            elif line.startswith('## '):
                c.setFont(font_name, 14)
                y -= 3
            elif line.startswith('### '):
                c.setFont(font_name, 12)
            else:
                c.setFont(font_name, 10)
            
            # Remove MD tokens for display
            display_text = line.replace('#', '').strip()
            
            # Auto-wrap (Very simple)
            words = display_text
            # ... (Full wrapping logic is complex, using simple truncation/char split here)
            # Better approach: Use Platypus for complex layout, but Canvas is simpler for single script
            c.drawString(MARGIN_X, y, display_text[:90]) 
            
            y -= LINE_HEIGHT * 1.2

        if y < MARGIN_Y_BOTTOM:
            c.showPage()
            page_num += 1
            draw_header_footer(c, page_num, font_name)
            y = PAGE_HEIGHT - MARGIN_Y_TOP
            
    c.save()
    print(f"User Manual PDF generated: {os.path.join(OUTPUT_DIR, MANUAL_FILENAME)}")

def generate_spec_pdf(font_name):
    c = canvas.Canvas(os.path.join(OUTPUT_DIR, SPEC_FILENAME), pagesize=A4)
    page_num = 1
    draw_header_footer(c, page_num, font_name)
    y = PAGE_HEIGHT - MARGIN_Y_TOP
    
    c.setFont(font_name, 16)
    c.drawString(MARGIN_X, y, "软件环境与技术规格说明书")
    y -= 10 * mm
    
    c.setFont(font_name, 12)
    
    for key, value in SPEC_DATA.items():
        # Title
        c.setFont(font_name, 11)
        c.drawString(MARGIN_X, y, f"【{key}】")
        y -= 6 * mm
        
        # Content (Simple wrap)
        c.setFont(font_name, 10)
        content_lines = value.split('\n')
        for line in content_lines:
            # Very basic char wrap
            limit = 50
            for i in range(0, len(line), limit):
                c.drawString(MARGIN_X + 5*mm, y, line[i:i+limit])
                y -= 5 * mm
        
        y -= 4 * mm # Spacing between items
        
        if y < MARGIN_Y_BOTTOM:
            c.showPage()
            page_num += 1
            draw_header_footer(c, page_num, font_name)
            y = PAGE_HEIGHT - MARGIN_Y_TOP

    c.save()
    print(f"Spec PDF generated: {os.path.join(OUTPUT_DIR, SPEC_FILENAME)}")

if __name__ == "__main__":
    font = register_font()
    generate_source_code_pdf(font)
    generate_manual_pdf(font)
    generate_spec_pdf(font)
