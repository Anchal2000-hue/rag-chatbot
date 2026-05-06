# RAG Chatbot — Chat with your PDF 🤖📄

An AI-powered chatbot that lets you upload any PDF and ask questions 
about its content in natural language. Built using RAG 
(Retrieval Augmented Generation) architecture from scratch.

## Features

- 📄 Upload any PDF document
- 🤖 Ask questions in natural language
- 💬 AI answers based ONLY on document content
- 📚 Chat history with context memory
- 💡 Suggested questions to get started
- 🔍 Intelligent text chunking and search
- 🗑️ Clear chat and start fresh

## Tech Stack

- **Python** + **Flask** (backend)
- **Groq AI** + **LLaMA 3.3** (language model)
- **PyPDF2** (PDF text extraction)
- **Custom RAG Pipeline** (chunking + retrieval)
- **HTML/CSS/JavaScript** (frontend)

## What is RAG?

RAG (Retrieval Augmented Generation) is an AI architecture that:
1. **Splits** your document into chunks
2. **Searches** for relevant chunks based on your question
3. **Feeds** relevant content to the AI as context
4. **Generates** accurate answers grounded in your document

This prevents AI hallucinations and ensures answers come from your actual document!

## Live Demo

👉 Coming soon on Render

## Run Locally

1. Clone the repo
```bash
   git clone https://github.com/Anchal2000-hue/rag-chatbot.git
   cd rag-chatbot
```

2. Install dependencies
```bash
   pip install flask groq pypdf2 python-dotenv
```

3. Create `.env` file
4. Run the app
```bash
   python app.py
```

5. Open http://127.0.0.1:5000

## How to Use

1. Upload any PDF (resume, textbook, research paper, notes)
2. Wait for processing
3. Ask questions like:
   - "What is this document about?"
   - "Summarize the main points"
   - "What are the key conclusions?"
4. Get instant AI-powered answers!

## Use Cases

- 📝 Chat with your resume
- 📚 Study from textbooks
- 🔬 Analyze research papers
- 📋 Extract info from reports
- 📖 Understand legal documents

## Author

**Anchal** — [github.com/Anchal2000-hue](https://github.com/Anchal2000-hue)

Portfolio: [anchaltiwari.netlify.app](https://anchaltiwari.netlify.app)