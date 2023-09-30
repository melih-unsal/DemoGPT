system_template = """
You are an AI assistant that can generate strict JSON in the following format:

{{
    "is_nlp":{{
        "reason:"$reason",
        "value" : "true/false"
    }},
    "is_chat":{{
        "reason:"$reason",
        "value" : "true/false"   
    }},
    "is_search":{{
        "reason:"$reason",
        "value" : "true/false"   
    }}
    
}}



is_nlp has 2 sub keys. 
    reason: shows why language understanding is needed or not
    value: shows that if the app idea requires GPT kind language model and cannot be accomplished by standard python libraries including data science related ones like numpy, scipy, sckit-learn.
    
is_chat has 2 sub keys. 
    reason: shows the reason of that decision. 
    value: shows that if the app idea requires chat-based system
    
is_search has 2 sub keys. 
    reason: shows the reason of that decision. 
    value: shows that if the app idea requires Google search
"""

human_template = """
App Idea:{instruction}
JSON:
"""