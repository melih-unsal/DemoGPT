# Contributing to DemoGPT

Thank you for your interest in contributing to DemoGPT! This document provides guidelines and instructions for contributing to the project. Whether you're adding new features, fixing bugs, or improving documentation, your contributions are welcome.

## System Overview

DemoGPT works through the following steps:
1. A plan is generated based on the incoming instruction from the user.
2. Tasks are generated based on the plan.
3. Code generation is made for each task.
4. Each generated code is combined, and the final code is generated as a Streamlit app.
5. The generated Streamlit code is executed with the Streamlit command.

## Project Structure

### Root Folder

- `src`: Contains the source code of the project.
  - `plan`: Main folder for planning and task generation.
    - `app.py`: Initial application where users can write down the demo idea (instruction) and the demo title (app title).
    - `cli.py`: For starting Streamlit at the beginning.
    - `model.py`: Includes the model corresponding to each step.
    - `utils.py`: Helper functions for the system.
    - `test.py`: Important to test the system components.
    - `test_cases.py`: Source includes test cases for `test.py`.
    - `chains`: Contains module definitions and task implementations.
      - `chains.py`: Module definitions.
      - `__init__.py`: Includes the modules.
      - `task_chains.py`: Implementations of all available tasks.
      - `task_definitions.py`: Definitions of all available tasks.
      - `prompts`: Folder containing task files.

### Task List Folder (`demogpt/plan/chains/prompts`)

Contains task files. Only `prompt_chat_template.py`, `ui_input_file.py`, `ui_input_text.py`, `ui_output_text.py` are filled. Others need to be filled according to their needs.

## Adding a New Task

To add a new task, follow these steps:

1. **Fill the Corresponding File:** Fill the corresponding file in `demogpt/plan/chains/prompts` with the implementation of the new task.
2. **Update Task Definitions:** Change the "TASKS" variable in `demogpt/plan/chains/task_definitions.py` to include the new task.
3. **Add the New Task to Task Chains:** Add the new task in `demogpt/plan/chains/task_chains.py`.
4. **Modify `__init__.py`:** Modify `demogpt/plan/chains/prompts/__init__.py` in a way that the new task becomes available.
5. **Add the New Task Call to `demogpt/plan`:** Add new task to getCodeSnippet function like in the following:
```python
elif task_type == $task_name:
    code = TaskChains.$task_name(task=task,code_snippets=code_snippets)
```

6. **Update Test Cases:** Update the `TOOL_EXAMPLES` variable in `demogpt/plan/test_cases.py` and add at least one test case to test the new tool.
7. **Add Test Script:** Add the corresponding test script in `demogpt/plan/test.py` like the following:

   ```python
   def test_$new_task_name(self):
       for example in TOOL_EXAMPLES[$new_task_name]:
           instruction = example["instruction"]
           inputs = example["inputs"]
           res = TaskChains.$new_task_name(instruction=instruction, inputs=inputs)
           self.writeToFile($APPROPRIATE_TASK_NAME, res, instruction)
   ```
**Test the New Task**: To test the new task, in the root, run the corresponding module like in the below:
```bash
python -m unittest src.plan.test.TestDemoGPT.$function_name
```
Then, the test result will be available in the **test.log**.

## Modifying The Main Prompts.

Main prompts are inside of `demogpt/plan/chains/prompts` folder whose names are `combine.py`, `feedback.py`, `plan.py`, `refine.py`, `tasks.py` and `final.py`

You can also modify those prompts according to their goal which you can check their usage in `demogpt/plan/model.py`

## Upcoming Tasks
We are planning to integrate 🦍 Gorilla, a model specifically designed for API calls, as a task. Stay tuned for more details on this exciting addition.

## Conclusion
Your contributions are vital to the success and growth of DemoGPT. Whether you're a seasoned developer or just starting, your insights, creativity, and hard work are appreciated. If you have any questions or need further assistance, please don't hesitate to reach out.

Thank you for being a part of the DemoGPT community!