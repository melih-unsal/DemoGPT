import json
import re

ALL_TASKS = [
    {
        "name": "ui_input_text",
        "description": "Gets input from the user via a text field.",
        "good_at": "Retrieving text input from the user.",
        "input_data_type":"none",
        "output_data_type":"string",
        "purpose": "Collect user-entered text for further processing.",
    },
    {
        "name": "ui_input_file",
        "description": "Provide a mechanism for users to upload a file and return its content as string. The task involves creating a file upload widget, reading the uploaded file, and returning its content as string.",
        "good_at": "Enabling file uploads, reading file content, and making the content available for further analysis or processing by returning as string.",
        "input_data_type":"none",
        "output_data_type":"string",
        "purpose": "Facilitating the upload of files (e.g., documents, spreadsheets, images) and providing access to their content for various applications such as data analysis, content review, or question-answering.",
    },
    {
        "name": "ui_output_text",
        "description": "Shows text output to the user.",
        "good_at": "Showing text to the user.",
        "input_data_type":"string",
        "output_data_type":"none",
        "purpose": "Displaying textual information to the user.",
    },
    {
        "name": "prompt_chat_template",
        "description": "Generate intelligent text output, such as questions or responses, from a given context or input.",
        "good_at": "Creating context-aware questions, responses, role play, or instructions.",
        "input_data_type":"string",
        "output_data_type":"string",
        "purpose":"Generating smart text output to the user."
    },
    {
        "name": "doc_load",
        "description": "Load from txt or url or pdf file path or csv file path or powerpoint file path and generate docs",
        "good_at": "Loadding from external sources including url, pdf, csv, excel and powerpoint and generate a docs",
        "input_data_type":"string",
        "output_data_type":"Document",
        "purpose": "Loading external files",
    },
    {
        "name": "summarize",
        "description": "Summarize Document Objects",
        "good_at": "Summarizing long Document Objects into concise and relevant information.",
        "input_data_type":"Document",
        "output_data_type":"none",
        "purpose": "Creating shorter versions of lengthy docs",
    },
    {
        "name": "hub_question_answering",
        "description": "Answer questions related to the file.",
        "good_at": "Question answering on files or documents.",
        "input_data_type":["string", "file"],
        "output_data_type":"string",
        "purpose": "Extracting and providing specific information from files in response to questions.",
    },
    {
        "name": "memory",
        "description": "Returns memory that could be attached as an input to any prompt_chat_template.",
        "good_at": "Memorizing the conversation history or context.",
        "input_data_type":"none",
        "output_data_type":"Memory",
        "purpose": "Storing and retrieving conversation history or contextual information.",
    },
    {
        "name": "prompt_list_parser",
        "description": "Transform the input text into a list.",
        "good_at": "Transforming text into a list.",
        "input_data_type":"string",
        "output_data_type":"list",
        "purpose": "Converting textual data into structured list format.",
    },
    {
        "name": "router",
        "description": "When there are multiple prompt_chat_template objects, it uses the appropriate one to answer the question.",
        "good_at": "Handling different types of questions that require different abilities.",
        "input_data_type":["*prompt_chat_template"],
        "output_data_type":"string",
        "purpose": "Routing queries to the appropriate handler based on context or type.",
    },
    {
        "name": "react",
        "description": "Answer questions that require external search on the web.",
        "good_at": "Answering questions that require Google search or other web searches.",
        "input_data_type":"string",
        "output_data_type":"string",
        "purpose": "Finding information online to answer user queries.",
    },
    {
        "name": "cpal_chain",
        "description": "Solve math problems end to end",
        "good_at": "Directly solving any math problems",
        "input_data_type":"string",
        "output_data_type":"string",
        "purpose": "Performing mathematical calculations and solving problems based on the input question",
    },
    {
        "name": "hub_bash",
        "description": "Do operations on the bash by running needed scripts on the terminal to apply the command.",
        "good_at": "Executing bash commands and providing results.",
        "input_data_type":"string",
        "output_data_type":"string",
        "purpose": "Running scripts or commands on the terminal and returning the output.",
    },
    {
        "name": "hub_meteo",
        "description": "Gives weather-related information from the question.",
        "good_at": "Answering weather-related questions.",
        "input_data_type":"string",
        "output_data_type":"string",
        "purpose": "Providing weather forecasts, conditions, and related information.",
    },
]

TASKS = ALL_TASKS[:6]  # first 6 of them has been implemented yet.

TASK_DESCRIPTIONS = json.dumps(TASKS, indent=4)

tasks = re.findall(r"\{(?:[^{}]|(?:\{[^{}]*\}))*\}", TASK_DESCRIPTIONS)

# Printing each JSON object
for task in tasks:
    changed = "{" + task + "}"
    TASK_DESCRIPTIONS = TASK_DESCRIPTIONS.replace(task, changed)