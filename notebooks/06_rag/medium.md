# RAG with DemoGPT: Building Document-Powered AI Systems

## Introduction

Large language models are incredibly powerful, but they have a fundamental limitation: they only know what they were trained on. They can't answer questions about your private documents, company data, or the latest information.

**Retrieval Augmented Generation (RAG)** solves this by combining document retrieval with LLM generation. DemoGPT's `BaseRAG` makes building RAG systems remarkably simple --- add your documents, ask questions, get accurate answers grounded in your data.

## How RAG Works

The RAG pipeline has five stages:

```
Documents -> Chunking -> Embedding -> Vector Store -> Query Time
                                                        |
                                              Retrieval + Generation
```

1. **Documents** --- Your files (PDF, TXT, CSV, JSON, URLs)
2. **Chunking** --- Documents are split into manageable pieces
3. **Embedding** --- Each chunk is converted to a numerical vector
4. **Vector Store** --- Vectors are stored for efficient similarity search
5. **Query** --- User's question is embedded, similar chunks are retrieved, and the LLM generates an answer using those chunks as context

DemoGPT's `BaseRAG` handles all of this automatically.

## Quick Start

```python
from demogpt_agenthub.rag import BaseRAG
from demogpt_agenthub.llms import OpenAIChatModel

llm = OpenAIChatModel(model_name="gpt-4o-mini")

rag = BaseRAG(
    llm=llm,
    vectorstore="chroma",
    persistent_path="my_rag",
    index_name="my_index",
    reset_vectorstore=True
)

# Add content
rag.add_texts(
    "DemoGPT is an open-source framework created by Melih Unsal. "
    "It generates Streamlit apps from natural language and provides "
    "tools for building AI agents."
)

# Query
response = rag.run("What is DemoGPT and who created it?")
print(response)
```

That's it. Five lines of setup, and you have a working RAG system.

## Adding Content

### Adding Text Directly

```python
rag.add_texts("Your text content here.")
rag.add_texts("You can add multiple pieces of text.")
```

### Adding Files

DemoGPT supports multiple file formats:

```python
rag.add_files([
    "report.pdf",         # PDF documents
    "notes.txt",          # Text files
    "data.csv",           # CSV data
    "config.json",        # JSON files
    "https://example.com" # Web pages
])
```

Supported formats:
| Format | Extension | Notes |
|--------|-----------|-------|
| PDF | `.pdf` | Uses pdfminer for extraction |
| Text | `.txt` | Direct text reading |
| CSV | `.csv` | Tabular data |
| JSON | `.json` | Structured data |
| URLs | `http(s)://` | Web page content |

## Embedding Models

Embeddings convert text into numerical vectors for similarity search. DemoGPT supports two types:

### Local Embeddings (Free, No API Key)

```python
rag = BaseRAG(
    llm=llm,
    vectorstore="chroma",
    persistent_path="local_rag",
    index_name="local_index",
    embedding_model_name="sentence-transformers/all-mpnet-base-v2"
)
```

This is the default. The model runs locally, so it's free and private.

### OpenAI Embeddings (Higher Quality)

```python
rag = BaseRAG(
    llm=llm,
    vectorstore="chroma",
    persistent_path="openai_rag",
    index_name="openai_index",
    embedding_model_name="text-embedding-3-small"
)
```

Available OpenAI embedding models:
- `text-embedding-3-small` --- Fast, cost-effective
- `text-embedding-3-large` --- Higher quality
- `text-embedding-ada-002` --- Legacy, still widely used

## Vector Store Options

DemoGPT supports three vector stores, each with different tradeoffs:

### Chroma (Default)

```python
rag = BaseRAG(
    llm=llm,
    vectorstore="chroma",
    persistent_path="chroma_store",
    index_name="my_index"
)
```

- Lightweight and easy to set up
- Persists to disk automatically
- Perfect for development and small-to-medium datasets
- No external services needed

### FAISS

```python
rag = BaseRAG(
    llm=llm,
    vectorstore="faiss",
    persistent_path="faiss_store",
    index_name="my_index"
)
```

- Facebook's efficient similarity search library
- Extremely fast for large datasets
- In-memory with disk persistence
- Great for production with large document collections

### Pinecone

```python
rag = BaseRAG(
    llm=llm,
    vectorstore="pinecone",
    persistent_path="pinecone_store",
    index_name="my_index"
)
```

- Cloud-hosted, fully managed
- Scales to billions of vectors
- Production-ready with high availability
- Requires a Pinecone API key

### Comparison

| Feature | Chroma | FAISS | Pinecone |
|---------|:------:|:-----:|:--------:|
| Setup complexity | Low | Low | Medium |
| Scalability | Small-Medium | Large | Very Large |
| Hosting | Local | Local | Cloud |
| Cost | Free | Free | Paid |
| Best for | Development | Large local datasets | Production |

## Configuring Retrieval

### Number of Results (k)

The `k` parameter controls how many document chunks are retrieved:

```python
rag = BaseRAG(
    llm=llm,
    vectorstore="chroma",
    persistent_path="rag_k",
    index_name="k_index",
    k=4  # Retrieve top 4 most relevant chunks
)
```

- **k=2-3** --- When you need precise, focused answers
- **k=4-5** --- Good default for most use cases
- **k=8-10** --- When comprehensive coverage matters

### Score Threshold

Filter out low-relevance results:

```python
rag = BaseRAG(
    llm=llm,
    vectorstore="chroma",
    persistent_path="rag_filtered",
    index_name="filtered_index",
    k=4,
    filter={"search_kwargs": {"score_threshold": 0.5}}
)
```

Only chunks with a similarity score above 0.5 will be included. This prevents the LLM from being confused by irrelevant context.

## Persistent Storage

### Building Up a Knowledge Base

```python
# First session: create and populate
rag = BaseRAG(
    llm=llm,
    vectorstore="chroma",
    persistent_path="knowledge_base",
    index_name="kb_index",
    reset_vectorstore=True  # Start fresh
)
rag.add_files(["doc1.pdf", "doc2.pdf"])

# Later session: add more without losing existing data
rag = BaseRAG(
    llm=llm,
    vectorstore="chroma",
    persistent_path="knowledge_base",
    index_name="kb_index",
    reset_vectorstore=False  # Keep existing data!
)
rag.add_files(["doc3.pdf"])
```

Key parameters:
- `persistent_path` --- Where the vector store is saved on disk
- `reset_vectorstore=True` --- Clear everything and start fresh
- `reset_vectorstore=False` --- Preserve existing data and add to it

## RAG as an Agent Tool

One of DemoGPT's most powerful features is using RAG as a tool inside a ReactAgent:

```python
from demogpt_agenthub.agents import ReactAgent
from demogpt_agenthub.tools import PythonTool

rag = BaseRAG(
    llm=llm,
    vectorstore="chroma",
    persistent_path="agent_rag",
    index_name="agent_index",
    reset_vectorstore=True
)
rag.add_texts(
    "The company revenue in 2024 was $5.2 million "
    "with a year-over-year growth rate of 35%."
)

agent = ReactAgent(
    tools=[rag, PythonTool()],
    llm=llm,
    verbose=True
)

response = agent.run(
    "What was the company revenue? "
    "Calculate the projected revenue for the next 3 years "
    "using compound growth."
)
```

The agent will:
1. Query RAG for revenue and growth data
2. Use PythonTool to calculate compound growth
3. Return a comprehensive answer with projections

This pattern is incredibly powerful for enterprise applications where you need both **knowledge retrieval** and **computational ability**.

## Real-World Use Cases

### Company Knowledge Base
```python
rag = BaseRAG(llm=llm, vectorstore="chroma", ...)
rag.add_files([
    "employee_handbook.pdf",
    "policies.pdf",
    "faq.txt"
])
rag.run("What is the vacation policy for new employees?")
```

### Research Assistant
```python
rag.add_files([
    "paper1.pdf",
    "paper2.pdf",
    "https://arxiv.org/abs/2106.01495"
])
rag.run("What are the key findings across these papers?")
```

### Customer Support
```python
rag.add_files(["product_docs.pdf", "troubleshooting.txt"])
rag.run("How do I reset my device to factory settings?")
```

## Best Practices

1. **Start with Chroma** --- It's the simplest to set up and works great for development. Switch to FAISS or Pinecone when you need scale.

2. **Use appropriate chunk sizes** --- DemoGPT handles chunking automatically, but be aware that very large documents are split into pieces.

3. **Set reset_vectorstore carefully** --- Use `True` during development, `False` in production to preserve your data.

4. **Adjust k based on your use case** --- More chunks provide more context but can also introduce noise.

5. **Use score_threshold in production** --- Filter out low-relevance results to improve answer quality.

6. **Combine RAG with agents** --- The RAG + ReactAgent + PythonTool pattern covers most enterprise use cases.

7. **Choose the right embedding model** --- Local embeddings are free and private; OpenAI embeddings are higher quality but cost money and send data to OpenAI.

## Conclusion

RAG is the bridge between general-purpose LLMs and domain-specific knowledge. DemoGPT's `BaseRAG` makes it remarkably simple to build document-powered AI systems --- from a quick prototype with Chroma to a production deployment with Pinecone.

Combined with DemoGPT's agents and tools, RAG enables you to build AI systems that can not only answer questions about your documents but also reason about the answers and perform computations on the extracted data.

---

*This article is part of a series on DemoGPT. Check out the companion Jupyter notebook for hands-on examples.*
