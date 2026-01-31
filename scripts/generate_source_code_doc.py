import os
import sys

# Add parent directory to sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(PROJECT_ROOT)

def generate_source_code_doc():
    source_dir = os.path.join(PROJECT_ROOT, "src")
    output_file = os.path.join(PROJECT_ROOT, "docs", "source_code.txt")
    extensions = [".py", ".ts", ".tsx"] # Scan Python and TS/TSX files
    
    print(f"🔍 Scanning {source_dir} for source code...")
    
    total_lines = 0
    with open(output_file, "w", encoding="utf-8") as outfile:
        for root, _, files in os.walk(source_dir):
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "r", encoding="utf-8") as infile:
                            lines = infile.readlines()
                            
                        # Filter comments and empty lines
                        clean_lines = []
                        for line in lines:
                            stripped = line.strip()
                            # Skip empty lines
                            if not stripped:
                                continue
                            # Skip comments (Python # or JS //)
                            if stripped.startswith("#") or stripped.startswith("//"):
                                continue
                            clean_lines.append(line)
                            
                        if clean_lines:
                            outfile.write(f"--- File: {file_path} ---\n")
                            outfile.writelines(clean_lines)
                            outfile.write("\n\n")
                            total_lines += len(clean_lines)
                            print(f"✅ Processed {file}: {len(clean_lines)} lines")
                            
                    except Exception as e:
                        print(f"⚠️ Error reading {file_path}: {e}")

    print("="*50)
    print(f"🎉 Source code document generated: {output_file}")
    print(f"📊 Total lines of code (clean): {total_lines}")
    print("="*50)

if __name__ == "__main__":
    generate_source_code_doc()
