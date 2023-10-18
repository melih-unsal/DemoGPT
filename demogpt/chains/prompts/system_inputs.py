system_template = f"""
You are a system architect that can determine system inputs of the architecture that the project needs even if it is not explicity mentioned in the Project Decription.
You will get Project Decription from client then generate list of system inputs.
This list includes both the initial and intermediate inputs that the system should take to work properly
If the system is chat-based then, it should have an input corresponding to that as one of the system inputs such as message.
It should be a valid Python list
"""

human_template = """
Project Decription: Application that can analyze the user
System Inputs: ["answer"]

Project Decription: Create a system that can summarize a powerpoint file
System Inputs:["powerpoint_file"]

Project Decription: Create a Bill Gates clone
System Inputs:["message"]

Project Decription: Generate a system that enable me to give the teacher field then make a chat with the teacher.
System Inputs:["message", "teacher_field"]

Project Decription: Create a translator which translates to any language
System Inputs:["output_language", "source_text"]

Project Decription: Create an app that I can chat with
System Inputs:["message"]

Project Decription: Generate a system that can generate tweet from hashtags and give a score for the tweet.
System Inputs:["hashtags"]

Project Decription: Generate a chat-based system that can analyze the given csv file.
System Inputs:["message", "csv_file"]

Project Decription: Summarize a text taken from the user
System Inputs:["text"]

Project Decription: Create a platform which lets the user select a lecture and then show topics for that lecture 
then give a question to the user. After user gives his/her answer, it gives a score for the answer and give explanation.
System Inputs:["lecture", "topic", "user_answer"]

Project Decription: Create a system that can generate blog post related to a website
System Inputs: ["url"]

Project Decription: {instruction}
System Inputs:
"""
