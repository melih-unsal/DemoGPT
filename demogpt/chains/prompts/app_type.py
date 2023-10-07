system_template = """
Please classify your app idea based on the following criteria and generate the appropriate JSON:

1. explanation:
    Gives detailed explanation about the decision for each one is_ai, is_chat, is_search respectively.

2. is_ai:
    - True if:
        a. The app requires natural language understanding or generation.
        b. It requires complex computations or algorithms beyond standard Python libraries like 'numpy', 'pandas', or 'requests'.
    - False otherwise.

3. is_chat:
    - True if the primary function of the app is to engage in conversation.
    - False otherwise.

4. is_search:
    - True if:
        a. The app idea strictly requires information after cut off date and this information should be fetched in the whole web instead of specific websites.
    - False otherwise.
    
Example JSON Format:

{{
    "explanation":"string",
    "is_ai":"true/false",
    "is_chat":"true/false",
    "is_search":"true/false"
}}
"""

human_template = """
App Idea: an agent that can get analysis of CSV file then summarize it.
JSON:{{
    "explanation":"Making analysis requires ai. It does not include conversation. No up to date information is needed",
    "is_ai":"true",
    "is_chat":"false",
    "is_search":"false"
}}

App Idea: an application that can get the word count of txt file.
JSON:{{
    "explanation":"Word count is a simple python task so no ai is required. No conversation is expected. No up to date information is needed",
    "is_ai":"false",
    "is_chat":"false",
    "is_search":"false"
}}

App Idea: create an application that can talk like Jeff Bezos
JSON:{{
    "explanation":"To talk like Jeff Bezos, need generative text model so I need ai. Talking app includes conversation. No up to date information is needed",
    "is_ai":"true",
    "is_chat":"true",
    "is_search":"false"
}}

App Idea: create an application that can find and list all the male names
JSON:{{
    "explanation":"I need ai to filter the male names because it is not a simple Python task. It does not include conversation. No up to date information is needed",
    "is_ai":"true",
    "is_chat":"false",
    "is_search":"false"
}}

App Idea: generate an agent that can give suggestions to the uploaded CV
JSON:{{
    "explanation":"Giving suggestions is not a simple Python task so i need ai. Giving suggestions/advice does not require a conversation. No up to date information is needed",
    "is_ai":"true",
    "is_chat":"false",
    "is_search":"false"
}}

App Idea: a system that can transform given one currency to another
JSON:{{
    "explanation": "To transform from one currency to another, i need flexible analysis so i need ai. Currency transformation does not require conversation. I need to search the up to date currency information from web",
    "is_ai":"true",
    "is_chat":"false",
    "is_search":"true"
}}

App Idea:{instruction}
JSON:
"""
