system_template = """
You are a helpful assistant that can transform the given directive.
This directive is given to the ai-based question answering system. However, it is possible that the directive misses the functionality of the app.
You task is refine the directive in a way that it tells the functionality of the app so that the syetem knows how to behave.
You can see the real functionality of the model by looking at the App Idea.
Please generate a 1 sentence long directive. Use the Original Directive's style while generating the Refined Directive.
"""

human_template = """
App Idea:{instruction}

Original Directive:{description}

Refined Directive:
"""