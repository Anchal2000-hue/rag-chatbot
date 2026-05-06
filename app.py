import sys
sys.path.insert(0, 'E:/pypackages')

from flask import Flask, render_template, jsonify, request
from groq import Groq
from dotenv import load_dotenv
import os
import json
import uuid

load_dotenv()

app = Flask(__name__)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Simple in-memory storage
documents = {}
chat_histories = {}

def extract_text_from_pdf(file):
    import PyPDF2
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def chunk_text(text, chunk_size=1000, overlap=200):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
    return chunks

def simple_search(query, chunks, top_k=3):
    query_words = set(query.lower().split())
    scores = []
    for i, chunk in enumerate(chunks):
        chunk_words = set(chunk.lower().split())
        score = len(query_words & chunk_words)
        scores.append((score, i, chunk))
    scores.sort(reverse=True)
    return [chunk for _, _, chunk in scores[:top_k]]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'})

    file = request.files['file']
    if not file.filename.endswith('.pdf'):
        return jsonify({'error': 'Please upload a PDF file'})

    session_id = str(uuid.uuid4())[:8]
    text = extract_text_from_pdf(file)
    chunks = chunk_text(text)

    documents[session_id] = {
        'chunks': chunks,
        'filename': file.filename,
        'total_pages': len(text) // 2000 + 1
    }
    chat_histories[session_id] = []

    return jsonify({
        'session_id': session_id,
        'filename': file.filename,
        'chunks': len(chunks),
        'preview': text[:300] + '...'
    })

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    session_id = data.get('session_id')
    question = data.get('question')

    if session_id not in documents:
        return jsonify({'error': 'Please upload a PDF first'})

    doc = documents[session_id]
    relevant_chunks = simple_search(question, doc['chunks'])
    context = '\n\n'.join(relevant_chunks)

    history = chat_histories.get(session_id, [])
    history_text = '\n'.join([f"Q: {h['q']}\nA: {h['a']}" for h in history[-3:]])

    prompt = f"""You are a helpful assistant that answers questions based ONLY on the provided document content.

Document: {doc['filename']}

Relevant Content:
{context}

Previous conversation:
{history_text}

Question: {question}

Instructions:
- Answer ONLY based on the document content above
- If the answer is not in the document, say "I couldn't find this information in the document"
- Be concise and helpful
- Quote relevant parts when useful"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=1000
    )

    answer = response.choices[0].message.content
    chat_histories[session_id].append({'q': question, 'a': answer})

    return jsonify({
        'answer': answer,
        'sources': len(relevant_chunks)
    })

@app.route('/clear', methods=['POST'])
def clear():
    data = request.json
    session_id = data.get('session_id')
    if session_id in chat_histories:
        chat_histories[session_id] = []
    return jsonify({'status': 'cleared'})

if __name__ == '__main__':
    app.run(debug=True)