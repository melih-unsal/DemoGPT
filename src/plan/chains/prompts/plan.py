from chains.task_definitions import TASK_DESCRIPTIONS, TASK_NAMES, TASK_DTYPES

system_template = f"""
Create a plan to fulfill the given instruction. 
The plan should be broken down into clear, logical steps that detail how to accomplish the task. 
Consider all necessary user interactions, system processes, and validations, 
and ensure that the steps are in a logical sequence that corresponds to the given instruction.
Don't generate impossible steps in the plan because only those tasks are available:
{TASK_DESCRIPTIONS}

Pay attention to the input_data_type and the output_data_type.
If one of the task's output is  input of another, then output_data_type of previous one
should be the same as input_data_type of successor.

Only those task types are allowed to be used:
{TASK_NAMES}

Highly pay attention to the input data type and the output data type of the tasks while creating the plan. These are the data types:

{TASK_DTYPES}

When you create a step in the plan, its input data type 
either should be none or the output data type of the caller step. 

"""

human_template = """
Don't generate redundant steps which is not meant in the instruction.


Instruction: Create a system that can analyze the user
Let’s think step by step.
1. Generate question to understand the personality of the user by 'prompt_chat_template'
2. Show the question to the user by 'ui_output_text'
3. Get answer from the user for the asked question by 'ui_input_text'
4. Analyze user's answer by 'prompt_chat_template'.
5. Show the analyze to the user by 'ui_input_text'.

Instruction: Create a translator which translates to any language
Let’s think step by step.
1. Get output language from the user by 'ui_input_text'
2. Get source text which will be translated from the user by 'ui_input_text'
3. If all the inputs are filled, use 'prompt_chat_template' to translate text to output language
4. If translated text is ready, show it to the user by 'ui_output_text'

Instruction: Generate a system that can generate tweet from hashtags and give a score for the tweet.
Let’s think step by step.
1. Get hashtags from the user by 'ui_input_text'
2. If hashtags are filled, use 'prompt_chat_template' to create tweet.
3. If tweet is created, use 'prompt_chat_template' to generate a score from the tweet.
4. If score is created, display tweet and score to the user by 'ui_output_text'.

Instruction: Create a platform which lets the user select a lecture and then show topics for that lecture 
then give a question to the user. After user gives his/her answer, it gives a score for the answer and give explanation.
Let’s think step by step.
1. Use 'prompt_chat_template' to generate lectures
2. Among those generated by prompt_chat_template, get lecture from the user by 'ui_input_text'.
3. After user selects a lecture, generate topics releated to that lecture by 'prompt_chat_template'.
4. Among those generated by prompt_chat_template, get topic from the user by 'ui_input_text' .
5. After user selects the topic, use 'prompt_chat_template' to generate a question related to that topic and lecture
6. Get answer from the user by 'ui_input_text'.
7. Use 'prompt_chat_template' to generate the real answer and score for the user's answer.
8. Display real and answer and score for the user's answer by 'ui_output_text'.

Instruction: Create a system that can generate blog post related to a website
Let’s think step by step.
1. Get website URL from the user by 'ui_input_text'
2. Use 'doc_loader' to load the website as Document from URL
3. Use 'doc_to_string' to convert Document to string content
4. If string content is generated, use 'prompt_chat_template' to generate a blog post related to that string content.
5. If blog post is generated, display it to the user by 'ui_output_text'.

Instruction: Create a system that can summarize a powerpoint file
Let’s think step by step.
1. Get file path from the user by 'ui_input_file' for the powerpoint file
2. Use 'doc_loader' to load the powerpoint file as Document from the file path.
3. Use 'doc_summarizer' to generate summarization from the Document. 
5. If summarization is ready, display it to the user by 'ui_output_text'.

Instruction: Summarize a text taken from the user
Let’s think step by step.
1. Get text from the user by 'ui_input_text' 
2. Use 'prompt_chat_template' to summarize the given text.
3. If summarization is ready, display it to the user by 'ui_output_text'.

Instruction: Summarize a powerpoint file taken from the user
Let’s think step by step.
1. Get powerpoint file path with 'ui_input_file' 
2. Use 'doc_summarizer' to summarize the file from file path.
3. If summarization is ready, display it to the user by 'ui_output_text'.

Instruction: {instruction}
Let’s think step by step.

"""
