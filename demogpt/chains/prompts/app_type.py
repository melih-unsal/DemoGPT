system_template = """
You are an AI assistant that can generate strict JSON in the following format:

{{
    "is_ai":{{
        "value" : "true/false",
        "explanation:"$explanation"   
    }},
    "is_chat":{{
        "value" : "true/false",
        "explanation:"$explanation"   
    }},
    "is_search":{{
        "value" : "true/false",
        "explanation:"$explanation"   
    }}
    
}}



is_ai has 2 sub keys. 
    value: shows that if the app idea requires AI-based language model
    explanation: shows the reason of that decision.
    
is_chat has 2 sub keys. 
    value: shows that if the app idea requires chat-based system
    explanation: shows the reason of that decision. 
    
is_search has 2 sub keys. 
    value: shows that if the app idea requires Google search
    explanation: shows the reason of that decision. 
"""

human_template = """
App Idea:{instruction}
JSON:
"""