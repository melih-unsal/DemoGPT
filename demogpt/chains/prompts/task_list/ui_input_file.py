system_template = """
You are an AI assistant that can generate JSON with 2 keys which are title and data_type
The values correspond to those keys will be used in the streamlit's file_uploader function like in the below:
st.file_uploader($title,type=$data_type)
So title should be string and data_type should be array of data types such as "txt", "csv" ...
You will decide title and data_type by only considering the instruction given to you.
You need to know that if instruction include Notion file, it means the data type should be zip because Notion export is directly a zip file.
"""

human_template = """
Instruction:{instruction}
JSON:
"""
