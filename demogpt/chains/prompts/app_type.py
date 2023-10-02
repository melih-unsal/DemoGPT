system_template = """
Please classify your app idea based on the following criteria and generate the appropriate JSON:

1. is_ai
    - True if the app requires functions beyond standard libraries (e.g., numpy, scipy, scikit-learn).
    - False if it can be accomplished using standard Python libraries.

2. is_chat
    - True if the app idea involves conversation or needs human feedback to generate a new response.
    - False otherwise.

3. is_search
    - True if the app idea requires a Google search.
    - False otherwise.
    
Example JSON Format:

{{
    "is_ai":"true/false",
    "is_chat":"true/false",
    "is_search":"true/false"
}}
"""

human_template = """
App Idea: an agent that can get analysis of CSV file then summarize it.
JSON:{{
    "is_ai":"true",
    "is_chat":"false",
    "is_search":"false"
}}

App Idea: an application that can get the word count of txt file.
JSON:{{
    "is_ai":"false",
    "is_chat":"false",
    "is_search":"false"
}}

App Idea: create an application that can talk like Jeff Bezos
JSON:{{
    "is_ai":"true",
    "is_chat":"true",
    "is_search":"false"
}}

App Idea: create an application that can find and list all the male names
JSON:{{
    "is_ai":"true",
    "is_chat":"false",
    "is_search":"false"
}}

App Idea: generate an agent that can give suggestions to the uploaded CV
JSON:{{
    "is_ai":"true",
    "is_chat":"false",
    "is_search":"false"
}}

App Idea: a system that can transform given one currency to another
JSON:{{
    "is_ai":"true",
    "is_chat":"false",
    "is_search":"true"
}}

App Idea:{instruction}
JSON:
"""