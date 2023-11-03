system_template = """
You are a helpful assistant that can transform the given description similar to the given examples.
This description is part of the plan so while generating the new description, consider this plan.
Please make it similar to the examples below in terms of the style and length.
Also make it concise, 1 sentence long.

Examples:
1- Generate a blog post from a title
2- Implement a language translation app from one language to another
3- Answer question related to the uploaded powerpoint file
4- Generate an appropriate name for an animal
5- Create a programming-related humor machine
"""

human_template = """
Plan:{plan}

Description:{description}

New Description:
"""