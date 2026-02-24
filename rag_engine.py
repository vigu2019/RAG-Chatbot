import faiss
import numpy as np
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from transformers import pipeline

# Load local embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Load local generative model
generator = pipeline(
    "text2text-generation",
    model="google/flan-t5-base"
)


def create_vector_store(text):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    chunks = splitter.split_text(text)

    if not chunks:
        return None

    embeddings = embedding_model.encode(chunks)

    if len(embeddings) == 0:
        return None

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))

    return {"index": index, "chunks": chunks}


def answer_question(vectorstore, question):

    # Embed question
    question_embedding = embedding_model.encode([question])

    # Retrieve top 5 relevant chunks
    D, I = vectorstore["index"].search(
        np.array(question_embedding), k=5
    )

    similarity_score = float(D[0][0])

    retrieved_chunks = [
        vectorstore["chunks"][i] for i in I[0]
    ]

    # -----------------------------
    # STRICT RAG MODE
    # -----------------------------
    if similarity_score <= 1.5:

        context = " ".join(retrieved_chunks)
        context = context[:2000]

        prompt = f"""
You are a factual assistant.

Answer the question strictly based on the provided website content.
If the answer is not clearly mentioned in the content, say:
"The answer is not available in the scraped website content."

Website Content:
{context}

Question:
{question}

Provide a clear, structured answer in bullet points.
"""

        result = generator(
            prompt,
            max_length=250,
            do_sample=False,
            repetition_penalty=1.2,
            no_repeat_ngram_size=3
        )

        return (
            result[0]["generated_text"],
            retrieved_chunks,
            "Strict RAG Mode",
            similarity_score
        )

    # -----------------------------
    # GENERAL KNOWLEDGE FALLBACK
    # -----------------------------
    else:

        fallback_prompt = f"""
You are an AI assistant.

The website content does not contain a clear answer.
Answer the following question using general knowledge.

Question:
{question}

Provide a concise explanation.
"""

        fallback = generator(
            fallback_prompt,
            max_length=200,
            do_sample=False
        )

        return (
            fallback[0]["generated_text"],
            [],
            "General Knowledge Mode",
            similarity_score
        )