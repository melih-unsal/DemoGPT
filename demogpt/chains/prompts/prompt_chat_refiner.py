system_template = """
You will refine the given JSON and return exactly with the same keys according to the given feedback.
You will only change "system_template" and/or "template" depending on the feedback.
"""

human_template = """
Original JSON:
{templates}

Feedback: {feedback}

Refined JSON:
"""
