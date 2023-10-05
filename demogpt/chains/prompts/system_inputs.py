system_template = f"""
You are a helpful assistant that can determine all the inputs the system should take from the user to accomplish the given instruction.
This list includes both the initial and intermediate inputs that the system should take to work properly
If the system is chat-based then, it should have an input corresponding to that as one of the system inputs.
It should be a valid Python list
"""

human_template = """
Instruction: Application that can analyze the user
System Inputs: ["answer"]

Instruction: Create a system that can summarize a powerpoint file
System Inputs:["powerpoint_file"]

Instruction: Generate a system that enable me to give the teacher field then make a chat with the teacher.
System Inputs:["message", "teacher_field"]

Instruction: Create a translator which translates to any language
System Inputs:["output_language", "source_text"]

Instruction: Create an app that I can chat with
System Inputs:["message"]

Instruction: Generate a system that can generate tweet from hashtags and give a score for the tweet.
System Inputs:["hashtags"]

Instruction: Generate a chat-based system that can analyze the given csv file.
System Inputs:["message", "csv_file"]

Instruction: Summarize a text taken from the user
System Inputs:["text"]

Instruction: Create a platform which lets the user select a lecture and then show topics for that lecture 
then give a question to the user. After user gives his/her answer, it gives a score for the answer and give explanation.
System Inputs:["lecture", "topic", "user_answer"]

Instruction: Create a system that can generate blog post related to a website
System Inputs: ["url"]

Instruction: {instruction}
System Inputs:
"""
