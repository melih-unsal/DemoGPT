import json
import re

ALL_TASKS = [
    {
        "name": "ui_input_text",
        "description": "Gets input from the user via a text field.",
        "good_at": "Retrieving text input from the user.",
        "input": "none",
        "output": "string",
        "purpose": "Collect user-entered text for further processing.",
    },
    {
        "name": "ui_input_file",
        "description": "Provide a mechanism for users to upload a file and return its content as string. The task involves creating a file upload widget, reading the uploaded file, and returning its content as string.",
        "good_at": "Enabling file uploads, reading file content, and making the content available for further analysis or processing by returning as string.",
        "input": "none",
        "output": "string",
        "purpose": "Facilitating the upload of files (e.g., documents, spreadsheets, images) and providing access to their content for various applications such as data analysis, content review, or question-answering.",
    },
    {
        "name": "ui_output_text",
        "description": "Shows text output to the user.",
        "good_at": "Showing text to the user.",
        "input": "string",
        "output": "none",
        "purpose": "Displaying textual information to the user.",
    },
    {
        "name": "prompt_chat_template",
        "description": "Generate intelligent text output, such as questions or responses, from a given context or input.",
        "good_at": "Creating context-aware questions, responses, role play, or instructions.",
        "input": "string, context",
        "output": "string",
    },
    {
        "name": "hub_summarize",
        "description": "Summarize long text.",
        "good_at": "Summarizing long text into concise and relevant information.",
        "input": "string",
        "output": "string",
        "purpose": "Creating shorter versions of lengthy content.",
    },
    {
        "name": "hub_question_answering",
        "description": "Answer questions related to the file.",
        "good_at": "Question answering on files or documents.",
        "input": ["string", "file"],
        "output": "memory",
        "purpose": "Extracting and providing specific information from files in response to questions.",
    },
    {
        "name": "memory",
        "description": "Returns memory that could be attached as an input to any prompt_chat_template.",
        "good_at": "Memorizing the conversation history or context.",
        "input": "none",
        "output": "memory",
        "purpose": "Storing and retrieving conversation history or contextual information.",
    },
    {
        "name": "prompt_list_parser",
        "description": "Transform the input text into a list.",
        "good_at": "Transforming text into a list.",
        "input": "string",
        "output": "list",
        "purpose": "Converting textual data into structured list format.",
    },
    {
        "name": "router",
        "description": "When there are multiple prompt_chat_template objects, it uses the appropriate one to answer the question.",
        "good_at": "Handling different types of questions that require different abilities.",
        "input": "list of prompt_chat_template, string",
        "output": "string",
        "purpose": "Routing queries to the appropriate handler based on context or type.",
    },
    {
        "name": "react",
        "description": "Answer questions that require external search on the web.",
        "good_at": "Answering questions that require Google search or other web searches.",
        "input": "string",
        "output": "string",
        "purpose": "Finding information online to answer user queries.",
    },
    {
        "name": "cpal_chain",
        "description": "Solve math problems end to end",
        "good_at": "Directly solving any math problems",
        "input": "math_question",
        "output": "string",
        "purpose": "Performing mathematical calculations and solving problems based on the input question",
    },
    {
        "name": "hub_bash",
        "description": "Do operations on the bash by running needed scripts on the terminal to apply the command.",
        "good_at": "Executing bash commands and providing results.",
        "input": "string",
        "output": "string",
        "purpose": "Running scripts or commands on the terminal and returning the output.",
    },
    {
        "name": "hub_meteo",
        "description": "Gives weather-related information from the question.",
        "good_at": "Answering weather-related questions.",
        "input": "string",
        "output": "string",
        "purpose": "Providing weather forecasts, conditions, and related information.",
    },
]

TASKS = ALL_TASKS[:4]  # first 4 of them has been implemented yet.

TASK_DESCRIPTIONS = json.dumps(TASKS, indent=4)

tasks = re.findall(r"\{(?:[^{}]|(?:\{[^{}]*\}))*\}", TASK_DESCRIPTIONS)

# Printing each JSON object
for task in tasks:
    changed = "{" + task + "}"
    TASK_DESCRIPTIONS = TASK_DESCRIPTIONS.replace(task, changed)
