# Automatic Streamlit App Generation with DemoGPT

## Introduction

What if you could describe an application in plain English and have it built for you automatically? That's the core promise of DemoGPT --- a framework that transforms natural language instructions into complete, runnable Streamlit applications.

In this article, we'll explore how DemoGPT's app generation pipeline works, the types of apps you can create, and how to get the best results from the system.

## The Generation Pipeline

DemoGPT generates applications through a sophisticated multi-stage pipeline:

```
Natural Language Instruction
         |
         v
    System Inputs  --> Detect required inputs (API keys, etc.)
         |
         v
       Plan        --> Create structured execution plan
         |
         v
       Tasks       --> Break plan into 14 task types
         |
         v
       Draft       --> Generate code for each task
         |
         v
       Final       --> Assemble complete Streamlit app
```

Each stage is powered by carefully crafted prompt chains that guide the LLM through the generation process.

## Basic Usage

```python
from demogpt import DemoGPT

demo = DemoGPT(model_name="gpt-4o-mini")

instruction = "Create an app that takes a topic and generates a summary"
title = "Topic Summarizer"

for phase in demo(instruction=instruction, title=title):
    print(f"[{phase['stage']}] {phase['percentage']}% - {phase['message']}")
    if phase["done"]:
        print("\n=== Generated Code ===")
        print(phase["code"])
```

The generator yields progress updates at each stage, letting you track the generation process in real-time.

## Understanding Each Stage

### Stage 1: System Inputs
Detects what system-level inputs the app needs:
- OpenAI API key
- Other API keys
- Environment variables

### Stage 2: Plan
Creates a structured execution plan from your instruction. For example, "Create a translator app" might produce:
1. Get text input from user
2. Get target language from user
3. Use AI to translate the text
4. Display the translation

### Stage 3: Tasks
Breaks the plan into concrete, executable tasks. DemoGPT has **14 built-in task types**:

| Task | Purpose |
|------|---------|
| `ui_input_text` | Text input widget |
| `ui_input_file` | File upload widget |
| `ui_input_chat` | Chat input for conversational apps |
| `ui_output_text` | Display text output |
| `ui_output_chat` | Display chat history |
| `prompt_template` | Single-turn AI text generation |
| `chat` | Multi-turn conversational AI |
| `doc_loader` | Load files (PDF, TXT, CSV, etc.) |
| `doc_to_string` | Convert documents to text |
| `string_to_doc` | Convert text to document format |
| `python` | Execute Python code |
| `plan_and_execute` | ReAct agent with internet search |
| `summarization` | Document summarization |
| `question_answering` | Document Q&A |

### Stage 4: Draft
Each task is converted into a Python code snippet. The system generates Streamlit-compatible code for each component.

### Stage 5: Final
All code snippets are assembled into a complete, runnable Streamlit application with proper imports, layout, and error handling.

## Types of Apps You Can Generate

### Form-Based Apps

Traditional input-output applications:

```python
instruction = "Create an app where users enter a topic and get a detailed summary about it"
```

```python
instruction = "Create an app that takes English text and translates it to French with pronunciation"
```

### Chat-Based Apps

Conversational applications with message history:

```python
instruction = "Create a chatbot that acts as a helpful coding assistant"
```

```python
instruction = "Create a chatbot that talks like Jeff Bezos and gives business advice"
```

DemoGPT automatically detects whether your instruction describes a chat-based app and adjusts the generation accordingly.

### Document-Based Apps

Applications that work with uploaded files:

```python
instruction = "Create an app where users can upload a PDF file and ask questions about its content"
```

```python
instruction = "Create an app that uploads a text file and generates a summary of it"
```

## Configuration Options

### Model Selection

```python
demo = DemoGPT(model_name="gpt-4o-mini")  # Fast, cost-effective
demo.setModel("gpt-4.1")  # Switch to GPT-4.1 for better quality
```

More capable models like `gpt-4.1` produce better app code but are slower and more expensive. `gpt-4o-mini` is a great starting point for most apps.

### Refinement Steps

```python
demo = DemoGPT(
    model_name="gpt-4.1-mini",
    max_steps=15,      # More refinement iterations (default: 10)
    plan_max_steps=5   # More plan refinement iterations (default: 3)
)
```

More steps mean more chances to catch and fix errors, but also longer generation times.

### Custom API Base

```python
demo = DemoGPT(
    model_name="gpt-4o-mini",
    openai_api_base="http://localhost:8000/v1"  # Self-hosted model
)
```

## Handling the Generation Output

Each phase yields a dictionary with useful information:

```python
for phase in demo(instruction=instruction, title=title):
    # Progress tracking
    stage = phase["stage"]       # Current stage name
    pct = phase["percentage"]    # Progress percentage
    msg = phase["message"]       # Status message

    # Completion check
    if phase["done"]:
        code = phase["code"]     # The generated Streamlit code!

    # Error handling
    if phase.get("failed"):
        print(f"Failed at stage: {stage}")
        break
```

## Running the Generated App

Once you have the generated code, you can run it:

### Option 1: Save and Run
```python
# Save the generated code
with open("my_app.py", "w") as f:
    f.write(phase["code"])
```

```bash
streamlit run my_app.py
```

### Option 2: Use the Web Interface
```bash
demogpt  # Launches the built-in Streamlit UI
```

The web interface provides a user-friendly way to enter instructions and see the generated app in real-time.

## Self-Refinement

DemoGPT includes a self-refinement strategy that iteratively improves the generated code:

1. **Plan validation** --- Checks if the plan is logical and complete
2. **Task validation** --- Verifies tasks can be executed in order
3. **Code validation** --- Ensures generated code follows Python and Streamlit conventions
4. **Auto PEP8** --- Automatically formats code to PEP 8 standards

This refinement loop runs up to `max_steps` times, catching and fixing errors that would otherwise break the app.

## Tips for Better Results

1. **Be specific in your instructions** --- "Create a language translator" is good, but "Create an app that takes English text input and translates it to Spanish, showing both the original and translated text side by side" is better.

2. **Start simple** --- Begin with straightforward apps and gradually add complexity. DemoGPT handles simple apps more reliably than complex ones.

3. **Use gpt-4.1 for complex apps** --- If gpt-4o-mini produces broken code, try gpt-4.1. The quality improvement is significant for complex applications.

4. **Check the generated code** --- Always review the generated code before deploying. DemoGPT is a tool to accelerate development, not replace code review.

5. **Iterate on your instructions** --- If the first attempt doesn't produce what you want, refine your instruction rather than starting from scratch.

## Example Gallery

### Poem Generator
```python
instruction = "Create an app that takes a topic from the user and generates a creative poem about it"
```

### Language Translator
```python
instruction = "Create an app that translates text between English and Spanish with a text input and output display"
```

### Document Summarizer
```python
instruction = "Create an app where users upload a PDF document and get a concise summary"
```

### Chatbot
```python
instruction = "Create a friendly chatbot that helps users brainstorm startup ideas"
```

### Q&A System
```python
instruction = "Create an app where users upload a text file and can ask questions about its content"
```

## The Bigger Picture

DemoGPT's app generation is more than just a convenience --- it represents a new paradigm in software development. By combining:

- **Plan generation** from natural language
- **Task decomposition** into reusable components
- **Code generation** with self-refinement
- **Automatic assembly** into working applications

DemoGPT demonstrates that the gap between an idea and a working prototype can be bridged in minutes, not days.

## Conclusion

DemoGPT's automatic app generation transforms natural language descriptions into complete Streamlit applications. Whether you're prototyping a new idea, building a demo for a presentation, or learning how to structure LLM-powered applications, DemoGPT accelerates the entire process.

Combined with DemoGPT AgentHub's agents, tools, and RAG capabilities, you have a complete ecosystem for building AI-powered applications --- from the simplest chatbot to complex document-powered agent systems.

---

*This article is the final installment in our DemoGPT series. Check out all the companion Jupyter notebooks for hands-on examples covering every aspect of the framework.*
