# from .task_definitions import TASK_DESCRIPTIONS, TASK_NAMES

system_template = """
Create a Python list of task objects that align with the provided instruction and plan. Task objects must be Python dictionaries, and the output should strictly conform to a Python list of JSON objects.

You must use only the tasks provided in the description:

{TASK_DESCRIPTIONS}

task_name could be only one of the task names below:
{TASK_NAMES}
"""

human_template = """
Create a Python list of task objects that align with the provided instruction and all steps of the plan.

Task objects must be Python dictionaries, and the output should strictly conform to a Python list of JSON objects.

Follow these detailed guidelines:

Task Objects: Create a Python dictionary for each task using the following keys:

step: It represents the step number corresponding to which plan step it matches
task_type: Should match one of the task names provided in task descriptions.
task_name: Define a specific name for the task that aligns with the corresponding plan step.
input_key: List the "output_key" values from parent tasks used as input or "none" if there's no input or if it comes from the user.
input_data_type: The list of data types of the inputs
output_key: Designate a unique key for the task's output. It is compatible with the output type if not none
output_data_type: The data type of the output
description: Provide a brief description of the task's goal, mirroring the plan step.

Ensure that each task corresponds to each step in the plan, and that no step in the plan is omitted.
Ensure that output_key is unique for each task.
Ensure that each task corresponds to each step in the plan
Ensure that an output type of task does not change.

##########################
Instruction: Create a system that can generate blog post related to a website
Plan:
1. Get website URL from the user with 'ui_input_text'
2. Use 'doc_loader' to load the page as Document
3. Use 'doc_to_string' to convert Document to string
4. Use 'prompt_template' to generate a blog post using the result of doc_to_string
5. If blog post is generated, show it to the user with 'ui_output_text'.
List of Task Objects (Python List of JSON):
[
    {{
        "step": 1,
        "task_type": "ui_input_text",
        "task_name": "get_url",
        "input_key": "none",
        "input_data_type": "none",
        "output_key": "url",
        "output_data_type": "string",
        "description": "Get website url from the user"
    }},
    {{
        "step": 2,
        "task_type": "doc_loader",
        "task_name": "doc_loader",
        "input_key": "url",
        "input_data_type": "string",
        "output_key": "docs",
        "output_data_type": "Document",
        "description": "Load the document from the website url"
    }},
    {{
        "step": 3,
        "task_type": "doc_to_string",
        "task_name": "convertDocToString",
        "input_key": "docs",
        "input_data_type": "Document",
        "output_key": "docs_string",
        "output_data_type": "string",
        "description": "Convert docs to string"
    }},
    {{
        "step": 4,
        "task_type": "prompt_template",
        "task_name": "writeBlogPost",
        "input_key": ["docs_string"],
        "input_data_type": ["string"],
        "output_key": "blog",
        "output_data_type": "string",
        "description": "Write blog post related to the context of docs_string"
    }},
    {{
        "step": 5,
        "task_type": "ui_output_text",
        "task_name": "show_blog",
        "input_key": "blog",
        "input_data_type": "string",
        "output_key": "none",
        "output_data_type": "none",
        "description": "Display the generated blog post to the user"
    }}
]
##########################
Instruction:{instruction}
Plan : {plan}
List of Task Objects (Python List of JSON):
"""
