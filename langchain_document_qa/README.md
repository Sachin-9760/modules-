# LangChain Document Q&A

## 1. Open the project

In VS Code terminal:

```powershell
cd langchain_document_qa
```

## 2. Create virtual environment

```powershell
python -m venv .venv
.venv\Scripts\activate
```

## 3. Install packages

```powershell
pip install -r requirements.txt
```

## 4A. OpenAI provider

Create a file named `.env`:

```env
OPENAI_API_KEY=your_api_key_here
```

Then run:

```powershell
streamlit run app.py
```

## 4B. Ollama provider

Install Ollama, make sure it is running, and pull a model:

```powershell
ollama pull llama3.2
```

Then:

```powershell
streamlit run app.py
```

Select `Ollama` in the sidebar.

## What you learn

- Prompt templates
- Chat models
- Output parsers
- Document loaders
- Text splitting
- Embeddings
- FAISS vector store
- Retrievers
- Basic RAG
- Swappable model providers
