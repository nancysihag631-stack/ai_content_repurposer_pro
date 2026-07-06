# app.py - AI Content Repurposer (Fixed: real Ollama AI, clean terminal)
import streamlit as st
import pandas as pd
import ollama
import requests

# Suppress Streamlit context warnings permanently
st.cache_data._suppress_st_warning_in_get_or_create = True

st.title("✨ AI Content Repurposer Pro")
st.markdown("**FREE local AI: Blog → 5 social posts**")

st.sidebar.title("🚀 Quick Start")
st.sidebar.info("1. Open [localhost:8501](http://localhost:8501)\n2. Install Ollama + `ollama pull llama3.2`\n3. Upload TXT → Generate!")

if st.sidebar.button("🔍 Check Ollama"):
    try:
        r = requests.get("http://localhost:11434/api/tags", timeout=2)
        if r.status_code == 200:
            st.sidebar.success(" Ollama ready!")
        else:
            st.sidebar.warning("Run `ollama pull llama3.2`")
    except:
        st.sidebar.error(" Install Ollama from ollama.com")

# Main app
uploaded_file = st.file_uploader("📁 Upload blog (.txt/.md)", type=['txt','md','text'])
if uploaded_file:
    try:
        content = uploaded_file.read().decode('utf-8')
        st.success(f"✅ Loaded {len(content)} chars")
    except Exception as e:
        st.error(f"❌ File error: {e}")
        st.stop()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        style = st.selectbox("Style", ["Twitter Thread", "LinkedIn", "Instagram", "Email", "YouTube"])
    with col2:
        tone = st.selectbox("Tone", ["Casual", "Professional", "Fun"])
    with col3:
        max_len = st.slider("Length", 100, 400, 200)
    
    if st.button("✨ Generate 5 Posts", type="primary", use_container_width=True):
        with st.spinner("AI working..."):
            try:
                prompts = [
                    f"Make {style} post from this blog, {tone} tone, under {max_len} chars:\n{content[:1500]}",
                    f"Create engaging {style} from blog excerpt, {tone} style, max {max_len} chars:\n{content[:1500]}",
                    f"Repurpose blog as {style} post. {tone.title()}, concise {max_len} chars:\n{content[:1500]}",
                    f"Social {style} adaptation of blog, {tone} voice, {max_len} chars:\n{content[:1500]}",
                    f"Turn blog into {style} content, {tone} tone, limited to {max_len} chars:\n{content[:1500]}"
                ]
                posts = []
                for p in prompts:
                    resp = ollama.generate(model='llama3.2', prompt=p)
                    post = resp['response'][:max_len].strip()
                    posts.append(post)
                
                for i, post in enumerate(posts, 1):
                    st.markdown(f"### Post {i}")
                    st.write(post)
                
                csv_data = pd.DataFrame({'Social Post': posts}).to_csv(index=False).encode()
                st.download_button("💾 Download All", csv_data, "ai_posts.csv", use_container_width=True)
                st.success("🎉 Done!")
            except Exception as e:
                st.error(f"AI error: {e}. Check Ollama running.")

st.markdown("---")
st.caption("Powered by Ollama (free local AI)")
