imports = """
from langchain.docstore.document import Document
"""
outputs = """
{variable} =  [Document(page_content={argument}, metadata={{'source': 'local'}})]
"""

outputs = """
if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
    {variable} = ""
elif {argument}:
    {variable} = {function_name}({argument})
else:
    variable = ""
"""