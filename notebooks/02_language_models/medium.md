# Mastering Language Models in DemoGPT: A Complete Guide

## Introduction

At the heart of every AI agent is a language model. DemoGPT provides clean, modular wrappers around OpenAI's models through its `demogpt_agenthub.llms` module, making it easy to configure, swap, and use different LLMs across your applications.

In this article, we'll explore how to work with language models in DemoGPT --- from basic usage to advanced configuration.

## The LLM Architecture

DemoGPT's LLM system follows a simple hierarchy:

```
BaseLLM (Abstract)
    |
    +-- OpenAIChatModel (Chat Completion API)
    |
    +-- OpenAIModel (Text Completion API)
```

All LLMs implement a single `run(prompt)` method, making them interchangeable across agents, tools, and RAG systems.

## OpenAIChatModel: The Primary Choice

For most use cases, `OpenAIChatModel` is what you'll want. It wraps OpenAI's Chat Completion API:

```python
from demogpt_agenthub.llms import OpenAIChatModel

llm = OpenAIChatModel(model_name="gpt-4o-mini")
response = llm.run("What is machine learning?")
print(response)
```

### Configuring Parameters

You can fine-tune the model's behavior:

```python
# Creative output (higher temperature)
creative_llm = OpenAIChatModel(
    model_name="gpt-4o-mini",
    temperature=0.9,
    max_tokens=500
)

# Deterministic output (lower temperature)
precise_llm = OpenAIChatModel(
    model_name="gpt-4o-mini",
    temperature=0.1,
    max_tokens=500
)
```

**Temperature** controls randomness:
- `0.0` --- Deterministic, same output every time
- `0.7` --- Balanced (default)
- `1.0` --- Maximum creativity and variation

**max_tokens** limits the response length, helping control costs and response times.

## Supported Models

DemoGPT supports all current OpenAI models:

| Model | Type | Best For |
|-------|------|----------|
| `gpt-4.1` | Chat | Most capable, latest flagship model |
| `gpt-4.1-mini` | Chat | Balanced performance and cost |
| `gpt-4.1-nano` | Chat | Fastest, lowest cost |
| `gpt-4o` | Chat | Strong multimodal model |
| `gpt-4o-mini` | Chat | Compact and cost-effective |
| `o3` | Reasoning | Best for complex reasoning tasks |
| `o4-mini` | Reasoning | Cost-effective reasoning |

For most agent tasks, **gpt-4o-mini** offers the best balance of quality, speed, and cost. For complex reasoning chains, consider **gpt-4.1** or the reasoning models (**o3**, **o4-mini**).

## Custom API Base URLs

If you're using a self-hosted model, an API proxy, or a compatible third-party service, you can set a custom base URL:

```python
llm = OpenAIChatModel(
    model_name="my-local-model",
    api_base="http://localhost:8000/v1"
)
```

This is particularly useful for:
- **Self-hosted models** via vLLM, Ollama, or text-generation-inference
- **API proxies** for rate limiting or caching
- **Alternative providers** that offer OpenAI-compatible APIs

## Using LLMs with Agents

The real power comes when you connect LLMs to agents:

```python
from demogpt_agenthub.agents import ToolCallingAgent
from demogpt_agenthub.tools import TavilySearchTool
from demogpt_agenthub.llms import OpenAIChatModel

llm = OpenAIChatModel(model_name="gpt-4o-mini")

agent = ToolCallingAgent(
    tools=[TavilySearchTool()],
    llm=llm,
    verbose=True
)

response = agent.run("What are the latest AI trends?")
```

The LLM acts as the "brain" of the agent --- it decides which tools to use, how to interpret results, and how to formulate answers.

## Using LLMs with RAG

LLMs also power the generation step in RAG systems:

```python
from demogpt_agenthub.rag import BaseRAG
from demogpt_agenthub.llms import OpenAIChatModel

llm = OpenAIChatModel(model_name="gpt-4o-mini")

rag = BaseRAG(
    llm=llm,
    vectorstore="chroma",
    persistent_path="my_docs",
    index_name="doc_index",
    reset_vectorstore=True
)
```

The LLM receives retrieved document chunks as context and generates answers grounded in your data.

## Best Practices

1. **Start with gpt-4o-mini** --- It's fast, cheap, and surprisingly capable for most agent tasks.

2. **Use low temperature for agents** --- Agents need reliable, deterministic tool selection. Use temperature 0.1--0.3.

3. **Use higher temperature for creative tasks** --- Poem generation, story writing, brainstorming benefit from temperature 0.7--0.9.

4. **Set max_tokens appropriately** --- Don't pay for tokens you don't need. Short answers? Set max_tokens=200.

5. **Upgrade to gpt-4.1 or o3 for complex reasoning** --- If your agent struggles with multi-step reasoning, upgrading the model often helps more than adding tools.

## Conclusion

DemoGPT's LLM wrappers provide a clean, consistent interface for working with OpenAI models. Whether you're building a simple chatbot or a complex multi-agent system, understanding how to configure and use these models effectively is the foundation of everything else in DemoGPT.

In the next article, we'll explore DemoGPT's **built-in tools** and learn how to create custom tools for your agents.

---

*This article is part of a series on DemoGPT. Check out the companion Jupyter notebook for hands-on examples.*
