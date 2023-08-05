# src/plan Module

The `src/plan` module is the core directory of the DemoGPT project. It contains the main application and the modules for the different stages of the DemoGPT pipeline.

## Files in src/plan

- `app.py`: This is the main application file that starts the Streamlit application.
- `cli.py`: This file is responsible for initiating the Streamlit application.
- `model.py`: This file contains the modules corresponding to the plan, task, code generation, and code finalization stages of the DemoGPT pipeline.
- `test_cases.py`: This file contains test examples to test the model.
- `test.py`: This file contains the tests for the modules.
- `utils.py`: This file contains helper modules to assist the pipeline.

## [chains Folder](./src_plan_chains.md)

The `chains` folder contains the files related to the task chains and their definitions.

- `chains.py`: This file includes the model definitions which are plan, tasks, and final.
- `task_chains.py`: This file includes the implementations of all the available tasks.
- `task_definitions.py`: This file includes definitions of all the available tasks.

### prompts Folder

The `prompts` folder under `chains` contains all the necessary prompts for the models.

## Summary

The `src/plan` module is the heart of the DemoGPT project. It orchestrates the different stages of the pipeline, from planning to task creation, code snippet generation, and final code assembly. The `chains` folder within this module contains the definitions and implementations of the tasks, as well as the prompts for the models. The `test_cases.py` and `test.py` files provide a suite of tests to ensure the correct functioning of the modules.
