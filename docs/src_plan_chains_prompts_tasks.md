# src/plan/chains/prompts/task_list Module

The `src/plan/chains/prompts/task_list` module is a subdirectory of the `src/plan/chains/prompts` module in the DemoGPT project. It contains the files related to the tasks and their definitions.

## Files in src/plan/chains/prompts/task_list

- `hub_bash.py`: Executes bash commands and provides results.
- `hub_meteo.py`: Provides weather forecasts, conditions, and related information.
- `hub_pal_math.py`: Solves complex math problems and equations.
- `hub_question_answering.py`: Extracts and provides specific information from files in response to questions.
- `hub_summarize.py`: Summarizes long text into concise and relevant information.
- `memory.py`: Stores and retrieves conversation history or contextual information.
- `prompt_chat_template.py`: Generates intelligent text output, such as questions or responses, from a given context or input.
- `prompt_list_parser.py`: Transforms the input text into a list.
- `react.py`: Finds information online to answer user queries.
- `router.py`: Routes queries to the appropriate handler based on context or type.
- `ui_input_file.py`: Provides a mechanism for users to upload a file and return its content as string.
- `ui_input_text.py`: Gets input from the user via a text field.
- `ui_output_text.py`: Shows text output to the user.

## Summary

The `src/plan/chains/prompts/task_list` module contains the definitions of all tasks used in the DemoGPT pipeline. Each task has a specific purpose and is good at performing a certain function. The tasks range from getting user input and showing output to the user, to generating intelligent text output, transforming text into a list, routing queries, answering questions that require external search on the web, summarizing long text, answering questions related to a file, solving math problems, executing bash commands, and providing weather-related information.
