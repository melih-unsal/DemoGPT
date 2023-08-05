# TestDemoGPT - Unit Testing

TestDemoGPT is a class that contains a series of unit tests to validate the functionality of our application.

## Test Scenario

- The test scenario involves planning, task generation, code generation and testing of various tasks in the application like UI input text, UI output text, etc. The test plan uses various test cases defined in `TEST_CASES` and `TOOL_EXAMPLES`.

## Test Methods

- `setUpClass`: This method is executed once at the start of the testing process. It sets up the environment required for testing.
- `writeToFile`: A helper method to write the test results to a file.
- `printRes`: A helper method to print the results in a colorful, formatted manner.
- `test_plan`: Tests the plan creation.
- `test_tasks`: Tests the task creation.
- `test_final`: Tests the final code generation.
- `test_task_ui_input_text`: Tests UI input text task.
- `test_task_ui_output_text`: Tests UI output text task.
- `test_task_prompt_chat_template`: Tests prompt chat template task.
- `test`: This method runs the entire workflow of the application, from plan creation to code generation.
- `test_all`: This method iterates over all the test cases in `TEST_CASES` and runs the `test` method for each of them.

## How to run tests

### Running all tests

To run all the tests, use the following command:

```bash
python -m unittest src.plan.test.TestDemoGPT.test_all
```
### Running a single test module

To run a specific test module, you can use the following command format:

```bash
python -m unittest src.plan.test.TestDemoGPT.$func_name
```