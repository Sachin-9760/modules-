import os
import tempfile

import streamlit as st
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_ollama import ChatOllama, OllamaEmbeddings

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.vectorstores import FAISS

from langchain_text_splitters import RecursiveCharacterTextSplitter


# Load environment variables
load_dotenv()


def get_openai_api_key():
    key = os.getenv("OPENAI_API_KEY", "").strip()
    placeholder_values = {
        "",
        "your_openai_api_key_here",
        "replace_me",
        "changeme",
        "example",
        "sk-",
    }
    return key if key and key.lower() not in {value.lower() for value in placeholder_values} else None


# Page configuration
st.set_page_config(
    page_title="LangChain Document Q&A",
    page_icon="📚",
    layout="wide"
)

st.title("📚 LangChain Document Q&A")
st.write(
    "Upload a document and ask questions using a swappable AI model provider."
)


# Sidebar
with st.sidebar:
    st.header("⚙️ Model Settings")

    openai_available = get_openai_api_key() is not None
    provider_options = ["Ollama"]
    if openai_available:
        provider_options.append("OpenAI")

    provider = st.selectbox(
        "Model provider",
        provider_options,
        index=0
    )

    if provider == "OpenAI":
        model_name = st.text_input(
            "OpenAI model",
            "gpt-4o-mini"
        )

        if not get_openai_api_key():
            st.warning(
                "OPENAI_API_KEY is missing or still set to a placeholder value. "
                "Add a real key to .env and restart Streamlit."
            )

    else:
        chat_model = st.text_input(
            "Ollama chat model",
            "deepseek-r1"
        )
        embedding_model = st.text_input(
            "Ollama embedding model",
            "nomic-embed-text"
        )

        st.info(
            "Make sure Ollama is installed and running."
        )

    top_k = st.slider(
        "Retrieved chunks",
        min_value=1,
        max_value=8,
        value=4
    )


# Document loader
def load_document(uploaded_file):

    suffix = os.path.splitext(
        uploaded_file.name
    )[1].lower()

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix
    ) as tmp:

        tmp.write(uploaded_file.getvalue())
        file_path = tmp.name

    try:

        if suffix == ".pdf":
            documents = PyPDFLoader(file_path).load()

        else:
            documents = TextLoader(
                file_path,
                encoding="utf-8"
            ).load()

        return documents

    finally:

        os.remove(file_path)


# Chat model
def get_chat_model():

    if provider == "OpenAI":
        api_key = get_openai_api_key()
        if not api_key:
            st.error(
                "OpenAI API key is invalid or missing. Set OPENAI_API_KEY in the .env file to a valid key."
            )
            st.stop()

        return ChatOpenAI(
            model=model_name,
            temperature=0,
            api_key=api_key
        )

    return ChatOllama(
        model=chat_model,
        temperature=0
    )


# Embedding model
def get_embeddings():

    if provider == "OpenAI":

        return OpenAIEmbeddings()

    return OllamaEmbeddings(
        model=embedding_model
    )


# File uploader
uploaded = st.file_uploader(
    "📄 Upload a PDF, TXT, or Markdown file",
    type=["pdf", "txt", "md"]
)


if uploaded:

    try:

        # Create vector database
        if (
            st.session_state.get("file_name")
            != uploaded.name
        ):

            with st.spinner(
                "Loading and indexing document..."
            ):

                documents = load_document(
                    uploaded
                )

                # Split document into chunks
                splitter = RecursiveCharacterTextSplitter(
                    chunk_size=900,
                    chunk_overlap=150
                )

                chunks = splitter.split_documents(
                    documents
                )

                # Create FAISS vector database
                vectorstore = FAISS.from_documents(
                    chunks,
                    get_embeddings()
                )

                # Save in session
                st.session_state.vectorstore = vectorstore
                st.session_state.file_name = uploaded.name
                st.session_state.chunk_count = len(chunks)

        st.success(
            f"✅ Indexed {st.session_state.chunk_count} "
            f"chunks from {uploaded.name}"
        )


        # Question input
        question = st.text_input(
            "💬 Ask a question about your document"
        )


        if question:

            # Retriever
            retriever = (
                st.session_state.vectorstore
                .as_retriever(
                    search_kwargs={
                        "k": top_k
                    }
                )
            )

            # Retrieve relevant chunks
            retrieved_documents = retriever.invoke(
                question
            )

            # Combine context
            context = "\n\n".join(
                document.page_content
                for document in retrieved_documents
            )


            # Prompt
            prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        """You are a document question-answering assistant.

Answer the question using ONLY the provided document context.

If the answer cannot be found in the document,
say:

"I couldn't find that information in the uploaded document."

Keep the answer clear and concise.

Document context:
{context}
"""
                    ),
                    (
                        "human",
                        "{question}"
                    )
                ]
            )


            # LangChain chain
            chain = (
                prompt
                | get_chat_model()
                | StrOutputParser()
            )


            # Generate answer
            with st.spinner(
                "🤖 Generating answer..."
            ):

                answer = chain.invoke(
                    {
                        "context": context,
                        "question": question
                    }
                )


            # Display answer
            st.subheader("📝 Answer")

            st.write(answer)


            # Show retrieved chunks
            with st.expander(
                "🔍 Show retrieved context"
            ):

                for i, document in enumerate(
                    retrieved_documents,
                    start=1
                ):

                    st.markdown(
                        f"### Chunk {i}"
                    )

                    st.write(
                        document.page_content[:2000]
                    )


    except Exception as error:

        st.error(
            "❌ Something went wrong."
        )

        st.exception(error)


else:

    st.info(
        "👆 Upload a document to start."
    )

    st.markdown(
        """
## How the RAG pipeline works

**Document**
↓
**Document Loader**
↓
**Text Splitter**
↓
**Embeddings**
↓
**FAISS Vector Database**
↓
**Retriever**
↓
**Prompt**
↓
**LLM**
↓
**Answer**

### Supported providers

- OpenAI
- Ollama
"""
    )