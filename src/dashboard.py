# src/dashboard.py
import streamlit as st
import sys
import os
import json
import threading
from datetime import datetime, timedelta

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.main import run_daily_job
from src.memory_manager import MemoryManager
from src.config import RSS_FEEDS, EMAIL_RECIPIENTS
from src.preferences import USER_INTERESTS, USER_DISLIKES
from src.deep_research import DeepResearchFetcher
from src.summarizer import NewsSummarizer

st.set_page_config(
    page_title="AI Daily Intelligence",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern look
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .report-frame {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .premium-badge {
        background-color: #FFD700;
        color: #000;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 0.8em;
        font-weight: bold;
        margin-left: 5px;
    }
</style>
""", unsafe_allow_html=True)

def run_agent_async():
    """Run the agent in a separate thread"""
    with st.spinner("🚀 Agent is running... This may take 1-2 minutes."):
        try:
            run_daily_job(hours=24)
            st.success("✅ Agent finished successfully! Refreshing data...")
            st.rerun()
        except Exception as e:
            st.error(f"❌ Error: {e}")

def generate_deep_dive(topic):
    """Run deep research and generation"""
    status_text = st.empty()
    progress_bar = st.progress(0)
    
    try:
        # 1. Search
        status_text.text(f"🔍 Searching web for '{topic}'...")
        researcher = DeepResearchFetcher()
        progress_bar.progress(20)
        
        # 2. Fetch Content
        data = researcher.research_topic(topic)
        if not data:
            st.error("No data found.")
            return
            
        status_text.text(f"📖 Reading {len(data)} articles...")
        progress_bar.progress(50)
        
        # 3. Generate Report
        status_text.text("🧠 Synthesizing deep report...")
        summarizer = NewsSummarizer()
        report_md = summarizer.generate_deep_report(topic, data)
        progress_bar.progress(90)
        
        status_text.text("✅ Done!")
        progress_bar.progress(100)
        
        return report_md
        
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# --- Metrics Calculation ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
report_dir = os.path.join(BASE_DIR, "output")

mm = MemoryManager()
history = mm.load_history(days=30)
total_reports = len(history)
total_stories = sum(len(h.get('top_stories', [])) for h in history)
last_run = history[-1]['date'] if history else "N/A"

# --- Sidebar ---
with st.sidebar:
    # st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=64)
    st.title("AI Intelligence")
    st.caption(f"v2.3 | Last Run: {last_run}")
    st.markdown("---")
    
    st.subheader("⚡ Actions")
    if st.button("🚀 Trigger New Run", type="primary"):
        run_agent_async()
    
    st.markdown("---")
    st.subheader("⚙️ Configuration")
    
    with st.expander("📡 Data Sources", expanded=False):
        st.write(f"Active Feeds: **{len(RSS_FEEDS)}**")
        for name, url in RSS_FEEDS.items():
            st.text_input(name, value=url, disabled=True)
            
    with st.expander("👤 Interest Profile", expanded=False):
        st.write("**Focus Areas:**")
        st.info(", ".join(USER_INTERESTS))
        st.write("**Exclusions:**")
        st.warning(", ".join(USER_DISLIKES))
        
    with st.expander("📧 Delivery", expanded=False):
        st.write(f"Recipients: {', '.join(EMAIL_RECIPIENTS)}")

# --- Main Content ---
st.title("📊 Intelligence Dashboard")

# Top Metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Reports", total_reports, "+1" if total_reports > 0 else "0")
with col2:
    st.metric("Stories Analyzed", total_stories, f"+{len(history[-1].get('top_stories', []))}" if history else "0")
with col3:
    st.metric("Active Feeds", len(RSS_FEEDS))
with col4:
    st.metric("System Status", "Online", delta_color="normal")

st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["📄 Latest Report", "💎 Deep Dive (Beta)", "🗄️ Archive", "🧠 Knowledge Graph"])

with tab1:
    # Load latest report
    if os.path.exists(report_dir):
        files = sorted([f for f in os.listdir(report_dir) if f.endswith('.html')], reverse=True)
        
        if files:
            latest_file = files[0]
            file_path = os.path.join(report_dir, latest_file)
            
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.subheader(f"📑 {latest_file}")
            with col_b:
                with open(file_path, "r") as f:
                    html_content = f.read()
                st.download_button(
                    label="📥 Download HTML",
                    data=html_content,
                    file_name=latest_file,
                    mime="text/html",
                    use_container_width=True
                )
            
            # Preview (iframe)
            st.components.v1.html(html_content, height=800, scrolling=True)
        else:
            st.info("No reports found. Click 'Trigger New Run' to generate one.")
    else:
        st.warning(f"Output directory not found: {report_dir}")

with tab2:
    st.markdown("### 💎 Deep Dive Research")
    st.markdown("*Generate a comprehensive research report on any AI topic.* <span class='premium-badge'>PRO</span>", unsafe_allow_html=True)
    
    topic = st.text_input("Enter a topic (e.g., 'Agentic Workflow', 'DeepSeek Technical Architecture')", placeholder="What do you want to research?")
    
    if st.button("🔍 Generate Report", type="primary", disabled=not topic):
        report_md, slides_md = generate_deep_dive(topic)
        if report_md:
            st.markdown("---")
            
            # Display Report
            with st.expander("📄 Research Report", expanded=True):
                st.markdown(report_md)
                st.download_button("📥 Download Report (MD)", report_md, file_name=f"{topic}_report.md")
            
            # Display Slides
            if slides_md:
                with st.expander("🎨 Presentation Slides (Marp)", expanded=True):
                    st.code(slides_md, language="markdown")
                    st.download_button("📥 Download Slides (Marp MD)", slides_md, file_name=f"{topic}_slides.md")

with tab3:
    st.subheader("📜 Historical Reports")
    if os.path.exists(report_dir):
        files = sorted([f for f in os.listdir(report_dir) if f.endswith('.html')], reverse=True)
        
        if files:
            col_list, col_preview = st.columns([1, 2])
            
            with col_list:
                selected_file = st.radio("Select Date", files, format_func=lambda x: x.replace("ai_news_report_", "").replace(".html", ""))
                
            with col_preview:
                if selected_file:
                    file_path = os.path.join(report_dir, selected_file)
                    with open(file_path, "r") as f:
                        html_content = f.read()
                    st.components.v1.html(html_content, height=600, scrolling=True)
        else:
            st.info("No historical reports found.")
    else:
        st.warning(f"Output directory not found: {report_dir}")

with tab4:
    st.subheader("🧠 Memory Stream")
    if history:
        # Timeline view
        for entry in reversed(history):
            with st.expander(f"🗓️ {entry['date']} - {entry['intro'][:50]}...", expanded=False):
                st.info(f"**Overview:** {entry['intro']}")
                st.markdown("#### Top Stories")
                for story in entry.get('top_stories', []):
                    st.markdown(f"- **{story['title']}**: {story['summary']}")
    else:
        st.info("No memory history available yet.")
