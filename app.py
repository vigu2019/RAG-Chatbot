import streamlit as st
import time
from scraper import scrape_website
from rag_engine import create_vector_store, answer_question

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(
    page_title="RAG Website Chatbot",
    page_icon="🤖",
    layout="centered"
)

# ---------------------------
# Custom Styling
# ---------------------------
st.markdown("""
<style>
.main {
    background-color: #0f172a;
}
h1 {
    text-align: center;
    font-size: 42px;
}
.block-container {
    padding-top: 2rem;
}
.stButton>button {
    background-color: #2563eb;
    color: white;
    border-radius: 8px;
    height: 3em;
    width: 100%;
}
.stTextInput>div>div>input {
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# Title
# ---------------------------
st.title("🤖 RAG Powered Website Chatbot")
st.markdown("Semantic Search • FAISS • Generative AI • Hybrid Mode")

# ---------------------------
# Session State
# ---------------------------
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "sources" not in st.session_state:
    st.session_state.sources = []

# ---------------------------
# Website Input Section
# ---------------------------
st.markdown("### 🌐 Step 1: Enter Website URL")

url = st.text_input("Website URL")

if st.button("🚀 Process Website"):

    if not url:
        st.warning("Please enter a valid URL.")
    else:
        with st.spinner("Scraping and indexing website..."):
            scraped_data = scrape_website(url)
            text = scraped_data["text"]
            sources = scraped_data["sources"]

            vectorstore = create_vector_store(text)

        if vectorstore is None:
            st.error("Unable to extract usable content from this website. It may block scraping or require JavaScript rendering.")
        else:
            st.session_state.vectorstore = vectorstore
            st.success("Website processed successfully!")

        with st.expander("📄 Pages Scraped"):
            for s in sources:
                st.write("-", s)

# ---------------------------
# Question Section
# ---------------------------
st.markdown("### 💬 Step 2: Ask a Question")

question = st.text_input("Ask something about the website")

if st.button("🧠 Get Answer"):

    if st.session_state.vectorstore is None:
        st.warning("Please process a website first.")
    elif not question:
        st.warning("Please enter a question.")
    else:
        with st.spinner("Generating answer..."):
            start_time = time.time()

            answer, retrieved_chunks, mode, similarity_score = answer_question(
                st.session_state.vectorstore,
                question
            )

            end_time = time.time()

        # ---------------------------
        # Display Answer
        # ---------------------------
        st.markdown("## 📝 Answer")
        st.write(answer)

        # ---------------------------
        # Display Mode & Metrics
        # ---------------------------
        st.markdown(f"### 🔎 Mode Used: `{mode}`")
        st.markdown(f"### 📊 Similarity Score: `{round(similarity_score, 3)}`")
        st.markdown(f"⏱️ Response Time: `{round(end_time - start_time, 2)} seconds`")

        # ---------------------------
        # Retrieved Chunks (Transparency)
        # ---------------------------
        if retrieved_chunks:
            with st.expander("🔍 Retrieved Context Chunks"):
                for chunk in retrieved_chunks:
                    st.code(chunk[:400])