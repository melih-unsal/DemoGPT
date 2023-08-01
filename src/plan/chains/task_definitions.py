import re,json

ALL_TASKS = [
    {
        "name":"ui_input_text",
        "description":"gets input from the user via text field",
        "good_at":"retrieving text input from the user",
        "input":"none",
        "output":"string"
    },
    {
        "name":"ui_input_file",
        "description":"gets file input from the user via file upload",
        "good_at":"retrieving file input from the user",
        "input":"none",
        "output":"file"
    },
    {
        "name":"ui_output_text",
        "description":"shows text output to the user",
        "good_at":"showing text to the user",
        "input":"string",
        "output":"none"
    },
    {
        "name":"prompt_chat_template",
        "description":"generate intelligent text output from a text input by making a role play",
        "good_at":"generating intelligent text by role play",
        "input":"string",
        "output":"string"
    },
    {
        "name":"prompt_list_parser",
        "description":"transform the input text to list",
        "good_at":"transforming text into a list",
        "input":"string",
        "output":"list"
    },
    {
        "name":"document",
        "description":"read the file and answer file related question defined in the string",
        "good_at":"answering question on the given file",
        "input":["file","string"],
        "output":"string"
    },
    {
        "name":"router",
        "description":"When there are multiple prompt_chat_template objects, it uses the appropriate one to answer the question",
        "good_at":"handling different types of questions which requires different abilities",
        "input":"list of prompt_chat_template, string",
        "output":"string"
    },
    {
        "name":"react",
        "description":"Answer question which requires external search in the web",
        "good_at":"answering google search required questions",
        "input":"string",
        "output":"string"
    },
    {
        "name":"memory",
        "description":"Returns memory which could be attached as an input to any prompt_chat_template",
        "good_at":"memorizing the conversation history",
        "input":"none",
        "output":"memory"
    },
    {
        "name":"hub_summarize",
        "description":"Summarize long text",
        "good_at":"summarizing long text",
        "input":"string",
        "output":"string"
    },
    {
        "name":"hub_question_answering",
        "description":"Answer question related to the file",
        "good_at":"question answering on file",
        "input":["string", "file"],
        "output":"memory"
    },
    {
        "name":"hub_pal_math",
        "description":"Solve and give answer for math a problem",
        "good_at":"solving complex math problem",
        "input":"string",
        "output":"string"
    },
    {
        "name":"hub_bash",
        "description":"Do operations on the bash by running needed scripts on terminal to apply the command",
        "good_at":"giving answer related to the terminal by executing needed bash commands",
        "input":"string",
        "output":"string"
    },
    {
        "name":"hub_meteo",
        "description":"Gives weather related information from the question",
        "good_at":"answering weather related question",
        "input":"string",
        "output":"string"
    }
]

TASKS = ALL_TASKS[:4] # first 4 of them has been implemented yet.

TASK_DESCRIPTIONS = json.dumps(TASKS,indent=4)

tasks = re.findall(r'\{(?:[^{}]|(?:\{[^{}]*\}))*\}', TASK_DESCRIPTIONS)

# Printing each JSON object
for task in tasks:
    changed = "{"+task+"}"
    TASK_DESCRIPTIONS = TASK_DESCRIPTIONS.replace(task,changed)