system_template = """
You will refine the given JSON and return exactly with the same keys according to the given feedback.
You will only change "system_template" and/or "template" depending on the feedback.
In the templates, you are supposed to put strings in curly braces only in the "Inputs" list
"""

human_template = """
Original JSON:
{templates}

Inputs:{inputs}

Feedback: {feedback}

Refined JSON:
"""
