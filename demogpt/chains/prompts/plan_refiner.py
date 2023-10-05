system_template = """
Create a new plan which does the given instruction that does not have the problems of the old plan

Each step can only use one of the functions below:

{TASK_NAMES}

These are the explanations of those functions:

{TASK_PURPOSES}

The plan should be in the same format as the Problematic Plan but it cannot include the problem in the "Problems" section.

It is extremely important that all reasoning steps should be in the following format:
$step_num. $description [$task_type($arguments) ---> $result]

$step_num: is positive integer showing the order of the reasoning step.
$description : says the responsibility of the task.
$task_type : one of the available functions in {TASK_NAMES}
$arguments: input variable(s) for the function (it should be output of the one of the previous functions)
$result : output variable for the function
"""

human_template = """
Instruction:{instruction}

Problematic Plan:
{plan}

Problems: {feedback}

New Refined Plan:
"""
