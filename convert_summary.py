import markdown
import os

# Custom CSS for a clean, professional look
CSS = """
<style>
    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
        line-height: 1.6;
        color: #333;
        max-width: 800px;
        margin: 0 auto;
        padding: 40px 20px;
        background-color: #f7f9fc;
    }
    .container {
        background-color: #ffffff;
        padding: 40px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    h1 {
        font-size: 2.2em;
        border-bottom: 2px solid #eaecef;
        padding-bottom: 0.3em;
        color: #2c3e50;
    }
    h2 {
        font-size: 1.6em;
        border-bottom: 1px solid #eaecef;
        padding-bottom: 0.3em;
        margin-top: 1.5em;
        color: #2c3e50;
    }
    h3 {
        font-size: 1.3em;
        margin-top: 1.2em;
        color: #34495e;
    }
    ul {
        padding-left: 20px;
    }
    li {
        margin-bottom: 0.5em;
    }
    code {
        background-color: #f6f8fa;
        padding: 0.2em 0.4em;
        border-radius: 3px;
        font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
        font-size: 85%;
    }
    pre {
        background-color: #f6f8fa;
        padding: 16px;
        border-radius: 6px;
        overflow: auto;
    }
    pre code {
        background-color: transparent;
        padding: 0;
    }
    blockquote {
        border-left: 4px solid #dfe2e5;
        padding: 0 1em;
        color: #6a737d;
        margin: 0;
    }
    a {
        color: #0366d6;
        text-decoration: none;
    }
    a:hover {
        text-decoration: underline;
    }
</style>
"""

def convert_md_to_html(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
            
        html_body = markdown.markdown(md_content, extensions=['fenced_code', 'tables'])
        
        full_html = f"""
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Project Summary</title>
            {CSS}
        </head>
        <body>
            <div class="container">
                {html_body}
            </div>
        </body>
        </html>
        """
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(full_html)
            
        print(f"✅ Converted {input_file} to {output_file}")
        
    except Exception as e:
        print(f"❌ Error converting file: {e}")

if __name__ == "__main__":
    convert_md_to_html("project_summary.md", "project_summary.html")
