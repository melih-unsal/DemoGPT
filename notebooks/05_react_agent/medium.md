# ReactAgent in DemoGPT: Multi-Step Reasoning for Complex AI Tasks

## Introduction

Some problems can't be solved in a single step. When you need to search the web, process the results, perform calculations, and synthesize everything into an answer, you need an agent that can **reason and act iteratively**.

DemoGPT's `ReactAgent` implements the **ReAct (Reasoning + Acting) pattern** --- a powerful approach where the agent alternates between thinking and doing, chaining multiple tool calls until the task is complete.

## The ReAct Pattern

The ReactAgent follows an iterative loop:

```
Query
  |
  v
Decision: Is the task complete?
  |
  No -> Reasoning: What tool should I use next?
           |
           v
         Tool Call -> Tool Result
           |
           v
         Back to Decision
  |
  Yes -> Final Answer
```

Each iteration includes:
1. **Decision** --- Evaluate whether enough information has been gathered
2. **Reasoning** --- Determine the next best action
3. **Tool call** --- Execute the chosen tool
4. **Tool result** --- Receive and process the output
5. **Repeat** until the task is complete or `max_iter` is reached

## Basic Example

```python
from demogpt_agenthub.agents import ReactAgent
from demogpt_agenthub.tools import TavilySearchTool, PythonTool
from demogpt_agenthub.llms import OpenAIChatModel

llm = OpenAIChatModel(model_name="gpt-4o-mini")

agent = ReactAgent(
    tools=[TavilySearchTool(), PythonTool()],
    llm=llm,
    verbose=True,
    max_iter=10
)

response = agent.run(
    "What is the population of France? Calculate its square root."
)
print(response)
```

The agent will:
1. **Search** for the population of France
2. **Extract** the number from search results
3. **Calculate** the square root using PythonTool
4. **Return** the final answer

## Multi-Step Problem Solving

Here's where the ReactAgent truly shines --- complex queries that require multiple tools and reasoning steps:

```python
agent = ReactAgent(
    tools=[TavilySearchTool(), PythonTool()],
    llm=llm,
    verbose=True,
    max_iter=10
)

response = agent.run(
    "Search for the height of the Eiffel Tower in meters. "
    "Then calculate how many 1.8m tall people would need to "
    "stack on top of each other to reach that height."
)
```

**Agent's execution:**
1. Search for "Eiffel Tower height" -> Finds 330 meters
2. Run Python code: `330 / 1.8` -> Gets ~183.33
3. Synthesize: "You would need approximately 184 people..."

## Controlling Iterations

The `max_iter` parameter prevents infinite loops:

```python
# Conservative: stop after 3 iterations
agent = ReactAgent(tools=tools, llm=llm, max_iter=3)

# Default: up to 10 iterations
agent = ReactAgent(tools=tools, llm=llm, max_iter=10)

# Complex tasks: allow more iterations
agent = ReactAgent(tools=tools, llm=llm, max_iter=15)
```

When `max_iter` is reached, the agent returns the best answer it has assembled so far.

**Guidelines:**
- **3-5 iterations** --- Simple multi-step tasks
- **10 iterations** --- Standard complex tasks (default)
- **15+ iterations** --- Research-heavy tasks with many lookups

## ReactAgent with RAG

One of the most powerful combinations is using RAG as a tool within the ReactAgent:

```python
from demogpt_agenthub.rag import BaseRAG

# Create a RAG tool with your documents
rag = BaseRAG(
    llm=llm,
    vectorstore="chroma",
    persistent_path="company_docs",
    index_name="company_index",
    reset_vectorstore=True
)

# Add company data
rag.add_texts(
    "The company revenue in 2024 was $5.2 million "
    "with a growth rate of 35%."
)
rag.add_texts(
    "The company has 45 employees across 3 offices "
    "in New York, London, and Tokyo."
)

# Create agent that can query documents AND compute
agent = ReactAgent(
    tools=[rag, PythonTool()],
    llm=llm,
    verbose=True
)

response = agent.run(
    "What was the company revenue? "
    "Calculate the projected revenue for next year "
    "using the growth rate."
)
```

**Agent's execution:**
1. Query RAG: "company revenue and growth rate" -> $5.2M, 35%
2. Run Python: `5.2 * 1.35` -> $7.02M
3. Answer: "The projected revenue for next year is $7.02 million"

## Understanding Verbose Output

With `verbose=True`, the ReactAgent provides detailed, color-coded output:

```
[Decision] Task not complete - need to find population data
[Reasoning] I'll search for the current population
[Tool Call] TavilySearchTool("population of Japan 2024")
[Tool Result] Japan's population is approximately 123 million...
[Decision] Have population, now need to calculate
[Reasoning] I'll use PythonTool to compute the statistics
[Tool Call] PythonTool("import math\nprint(math.sqrt(123000000))")
[Tool Result] 11090.536...
[Decision] Task complete
[Answer] The population of Japan is approximately 123 million,
         and its square root is approximately 11,091.
```

## Adding Multiple Tools

The ReactAgent handles large tool sets well:

```python
from demogpt_agenthub.tools import (
    TavilySearchTool,
    WikipediaTool,
    PythonTool,
    BashTool,
    ArxivTool
)

agent = ReactAgent(
    tools=[
        TavilySearchTool(),
        WikipediaTool(),
        PythonTool(),
        BashTool(),
        ArxivTool()
    ],
    llm=llm,
    verbose=True,
    max_iter=10
)

response = agent.run(
    "Find the latest research paper about transformer architectures "
    "on arXiv, then search Wikipedia for the original 'Attention is "
    "All You Need' paper's citation count."
)
```

## Real-World Use Cases

### Research Assistant
```python
agent = ReactAgent(
    tools=[TavilySearchTool(), WikipediaTool(), ArxivTool()],
    llm=llm,
    verbose=True
)

agent.run(
    "Research the current state of nuclear fusion energy. "
    "Find the latest breakthroughs and key research institutions."
)
```

### Data Analysis Agent
```python
agent = ReactAgent(
    tools=[rag, PythonTool()],
    llm=llm,
    verbose=True
)

agent.run(
    "From our sales data, find the top-performing product category "
    "and calculate the year-over-year growth percentage."
)
```

### Multi-Source Fact Checker
```python
agent = ReactAgent(
    tools=[TavilySearchTool(), WikipediaTool()],
    llm=llm,
    verbose=True
)

agent.run(
    "Verify whether the claim 'The Great Wall of China is visible "
    "from space' is true. Check multiple sources."
)
```

## Best Practices

1. **Choose the right max_iter** --- Too low and the agent might not complete complex tasks. Too high and you waste tokens on unnecessary iterations.

2. **Provide focused tools** --- Give the agent only the tools it needs. A ReactAgent with 3 relevant tools outperforms one with 15 mostly-irrelevant tools.

3. **Use verbose mode for development** --- The reasoning trace is invaluable for understanding and debugging agent behavior.

4. **Write clear queries** --- Break complex requests into clear steps in your prompt. "Find X, then calculate Y" is better than "Tell me about X and Y."

5. **Combine with RAG for domain-specific tasks** --- RAG + ReactAgent is a powerful pattern for enterprise applications where you need both document knowledge and computational ability.

6. **Monitor token usage** --- Each iteration costs tokens. For cost-sensitive applications, set conservative `max_iter` values.

## ReactAgent vs ToolCallingAgent

| Scenario | Best Agent |
|----------|-----------|
| "What's the weather in Paris?" | ToolCallingAgent |
| "Calculate 42 * 17" | ToolCallingAgent |
| "Find GDP of France, convert to EUR, calculate per capita" | ReactAgent |
| "Research a topic from multiple sources and summarize" | ReactAgent |
| "Look up a fact on Wikipedia" | ToolCallingAgent |
| "Query our documents then compute statistics on the results" | ReactAgent |

## Conclusion

The ReactAgent is DemoGPT's most powerful agent type. Its iterative reasoning loop allows it to tackle complex, multi-step problems that require planning, tool chaining, and synthesis. Combined with RAG and custom tools, it becomes a versatile problem-solver for real-world applications.

Whether you're building a research assistant, a data analyst, or a customer support system, the ReactAgent provides the reasoning capabilities to handle complex workflows autonomously.

---

*This article is part of a series on DemoGPT. Check out the companion Jupyter notebook for hands-on examples.*
