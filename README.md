Good. We’ll make this look like a serious job-level project, not a college assignment.

Copy this into your `README.md`.

---

# 🤖 RAG Powered Website Chatbot

Semantic Search • FAISS • Generative AI • Hybrid Mode

---

## 📌 Overview

This project implements a **Retrieval-Augmented Generation (RAG) powered chatbot** that can answer questions about any website by:

1. Scraping website content
2. Converting content into embeddings
3. Indexing them using FAISS
4. Retrieving relevant context
5. Generating grounded answers using a local LLM

Unlike traditional chatbots, this system ensures responses are based strictly on retrieved website content, reducing hallucinations.

---

## 🚀 Live Demo

🔗 Live App: *(Add your Streamlit link here)*
🔗 GitHub Repository: https://github.com/vigu2019/RAG-Chatbot/

---

## 🧠 Architecture

```
User Question
      ↓
Website Scraper
      ↓
Text Chunking
      ↓
Sentence Embeddings (MiniLM)
      ↓
FAISS Vector Index
      ↓
Top-K Retrieval
      ↓
Grounded Prompt
      ↓
FLAN-T5 Generator
      ↓
Structured Answer
```

---

## 🛠 Tech Stack

* **Python**
* **Streamlit** – Frontend interface
* **FAISS** – Vector similarity search
* **SentenceTransformers (MiniLM)** – Embeddings
* **FLAN-T5 (HuggingFace)** – Local text generation
* **BeautifulSoup + Requests** – Web scraping

---

## 🔍 Key Features

### ✅ Recursive Website Crawling

* Crawls internal links within domain
* Filters navigation, scripts, and boilerplate content

### ✅ Semantic Search with FAISS

* Embedding-based similarity search
* Top-K relevant context retrieval

### ✅ Hallucination Guard

* Similarity threshold prevents false answers
* Returns “Answer not available” when content is insufficient

### ✅ Hybrid RAG Mode

* Strictly grounded mode
* Option to allow generative expansion (if enabled)

### ✅ Context Transparency

* Shows retrieved chunks for debugging
* Improves explainability

### ✅ Performance Metrics

* Response time tracking
* Crawl statistics display

---

## 🧪 Example Usage

1. Enter a website URL
2. Process the website
3. Ask a question about the content
4. Get a structured answer with contextual grounding

---

## ⚠️ Limitations

* Websites requiring heavy JavaScript rendering (e.g., Amazon) may block scraping.
* Currently uses static HTML parsing.
* No JavaScript rendering engine (Selenium/Playwright) integrated.

---

## 🔮 Future Improvements

* JavaScript rendering using Playwright
* Cross-encoder re-ranking for improved retrieval accuracy
* Chunk metadata tracking
* Multi-document indexing
* Cloud deployment with scalable vector DB
* Conversational memory support

---

## 💡 Why This Matters

This project demonstrates:

* Applied NLP engineering
* Vector databases and similarity search
* LLM grounding techniques
* Prompt engineering
* Full-stack AI integration

It reflects real-world AI product development patterns used in:

* Enterprise knowledge assistants
* Documentation Q&A systems
* Internal company copilots
* Legal and research assistants

---

## 🧑‍💻 Author

**Vignesh Murali**
Computer Science Undergraduate

