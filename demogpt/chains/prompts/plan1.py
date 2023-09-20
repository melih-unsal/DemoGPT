from .task_definitions import TASK_DESCRIPTIONS, TASK_DTYPES, TASK_NAMES

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

If you use a task in a step, highly pay attention to the input data type and the output data type of the task because it should be compatible with the step.

"""

human_template = """
Don't generate redundant steps which is not meant in the instruction.


Instruction: Application that can analyze the user
System Inputs: []
Let’s think step by step.
1. Generate question to understand the personality of the user by [prompt_template() ---> question]
2. Show the question to the user [ui_output_text(question)]
3. Get answer from the user for the asked question by [ui_input_text(question) ---> answer]
4. Analyze user's answer by [prompt_template(question,answer) ---> analyze]
5. Show the result to the user by [ui_output_text(analyze)].

Instruction: Create a system that can summarize a powerpoint file
System Inputs:[powerpoint_file]
Let’s think step by step.
1. Get file path from the user for the powerpoint file [ui_input_file() ---> file_path]
2. Load the powerpoint file as Document from the file path [doc_loader(file_path) ---> file_doc]
3. Generate summarization from the Document [doc_summarizer(file_doc) ---> summarized_text] 
5. If summarization is ready, display it to the user [ui_output_text(summarized_text)]

Instruction: Create a translator which translates to any language
System Inputs:[output_language, source_text]
Let’s think step by step.
1. Get output language from the user [ui_input_text() ---> output_language]
2. Get source text which will be translated from the user [ui_input_text() ---> source_text]
3. If all the inputs are filled, use translate text to output language [prompt_template(output_language, source_text) ---> translated_text]
4. If translated text is ready, show it to the user [ui_output_text(translated_text)]

Instruction: Generate a system that can generate tweet from hashtags and give a score for the tweet.
System Inputs:[hashtags]
Let’s think step by step.
1. Get hashtags from the user [ui_input_text() ---> hashtags]
2. If hashtags are filled, create the tweet [prompt_template(hashtags) ---> tweet]
3. If tweet is created, generate a score from the tweet [prompt_template(tweet) ---> score]
4. If score is created, display tweet and score to the user [ui_output_text(score)]

Instruction: Summarize a text taken from the user
System Inputs:[text]
Let’s think step by step.
1. Get text from the user [ui_input_text() ---> text] 
2. Summarize the given text [prompt_template(text) ---> summarized_text]
3. If summarization is ready, display it to the user [ui_output_text(summarized_text)]

Instruction: Create a system that can generate blog post related to a website
System Inputs: [url]
Let’s think step by step.
1. Get website URL from the user [ui_input_text() ---> url]
2. Load the website as Document from URL [doc_loader(url) ---> web_doc]
3. Convert Document to string content [doc_to_string(web_doc) ---> web_str ]
4. If string content is generated, generate a blog post related to that string content [prompt_template(web_str) ---> blog_post]
5. If blog post is generated, display it to the user [ui_output_text(blog_post)]

Instruction: {instruction}
System Inputs:{system_inputs}
Let’s think step by step.
"""
