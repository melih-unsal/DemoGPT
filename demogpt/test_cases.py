INSTRUCTIONS = [
    "generate a system that reads uploaded text file and translates its content into the language that user prompted",
    "Create a system that can translate from any language to any language",
    "Create a system that can generate blog post related to a website then summarize the generated blog post and show only the summarization",
    "create lyrics from a song title",
    "Create a system that answers question related to the uploaded pdf.",
    "Create an application that gets csv file as an input then shows the summarization of that file.",
    "Create a system that generates random programming related humors when 'laugh' button is clicked without any user input by AI",
]

CODE_SNIPPETS = [
    {
        "instruction": "generate a system that reads uploaded text file and translates its content into the language that user prompted",
        "plan": """
1. Get the file path from the user by 'ui_input_file'
2. Use 'doc_loader' to load the text file as Document from the file path.
3. Use 'doc_to_string' to convert Document to string
4. Get the output language from the user by 'ui_input_text'
5. If all inputs are filled, use 'prompt_template' to translate the text to the output language.
6. If the translation is ready, display it to the user by 'ui_output_text'.
""",
        "code_snippets": """
#Get the file path from the user
file = st.file_uploader("Upload file", type=["txt", "pdf", "docx"])
if file is not None:
    file_path = file.name
    st.session_state['file_path'] = file_path
else:
    st.warning("Please upload a file.")
    
# Return the file path as a string
if 'file_path' in st.session_state:
    file_path = st.session_state['file_path']
    st.write(f"File path: {file_path}")
    st.write(f"Type: {type(file_path).__name__}")



#Load the text file as Document from the file path
from langchain.document_loaders import TextLoader

def load_document(file_path):
    loader = TextLoader(file_path)
    docs = loader.load()
    return docs



#Convert Document to string
text = str(document)



#Get the output language from the user
output_language = st.text_input("Enter the output language:")



#Translate the text to the output language
def translator(text,output_language):
    chat = ChatOpenAI(
        temperature=0
    )
    system_template = "You are a language translator. Your task is to translate text to {output_language}."
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = "Please translate the following text to {output_language}: '{text}'."
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(text=text, output_language=output_language)
    return result # returns string   


if text and output_language:
    translation = translator(text,output_language)
else:
    translation = ""



#Display the translated text to the user
if translation:
    st.markdown(f"Translated Text: {translation}")
""",
    },
    {
        "instruction": "Create a system that can generate blog post related to a website then summarize it",
        "plan": """
1. Get website URL from the user by 'ui_input_text'
2. Use 'doc_loader' to load the website as Document from URL
3. Use 'doc_to_string' to convert Document to string
4. If doc_to_string generated the content as string, use 'prompt_template' to generate a blog post related to that content.
5. If blog post is generated, use 'prompt_template' to summarize the blog post.
6. If summarization is ready, display it to the user by 'ui_output_text'.
""",
        "code_snippets": """
#Get website url from the user
url = st.text_input('Enter website URL:')

#Load the document from the website url
from langchain.document_loaders import WebBaseLoader

def doc_loader(url):
    loader = WebBaseLoader(url)
    docs = loader.load()
    return docs

#Convert docs to string
docs_string = str(docs)

#Write blog post related to the context of docs_string
def blogPostWriter(docs_string):
    chat = ChatOpenAI(
        temperature=0.7
    )
    system_template = "You are a blogger tasked with writing a blog post related to the following topic: '{docs_string}'."
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = "Please write a blog post related to the following topic: '{docs_string}'."
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(docs_string=docs_string)
    return result # returns string   


if docs_string:
    blog = blogPostWriter(docs_string)
else:
    blog = ""

#Summarize the blog post
def blogSummarizer(blog):
    chat = ChatOpenAI(
        temperature=0
    )
    system_template = "You are an AI assistant tasked with summarizing a blog post."
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = "Please summarize the following blog post: '{blog}'."
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(blog=blog)
    return result # returns string   


if blog:
    summarization = blogSummarizer(blog)
else:
    summarization = ""

#Display the generated summarization to the user
def show_summarization(summarization):
    if summarization:
        st.markdown(f"## Summarization:\n{summarization}")
    else:
        st.markdown("Please enter a valid input to generate a summarization.")

show_summarization(summarization)
    """,
    },
]

TEST_CASES = [
    {
        "instruction": "Create a system that can generate blog post related to a website then summarize it"
    },
    {
        "instruction": """
        create a system that can predict horoscope by asking intelligent question 
        to the user and analyzing user's answer without birth date or explicit question directly related to horoscope.
        """,
        "plan": """
        1. Generate intelligent questions related to horoscope using AI.
        2. Show the question to the user.
        3. Get answer from the user for the asked question.
        4. Analyze user's answer using AI to predict horoscope.
        5. Show the horoscope prediction to the user.
        """,
        "task": """
        [
            {
                "step": 1,
                "task_type": "prompt_template",
                "task_name": "generate_intelligent_questions",
                "input_key": "none",
                "output_key": "generated_questions",
                "description": "Generate intelligent questions related to horoscope using AI."
            },
            {
                "step": 2,
                "task_type": "ui_output_text",
                "task_name": "show_question_to_user",
                "input_key": "generated_questions",
                "output_key": "none",
                "description": "Show the question to the user."
            },
            {
                "step": 3,
                "task_type": "ui_input_text",
                "task_name": "get_user_answer",
                "input_key": "none",
                "output_key": "user_answer",
                "description": "Get answer from the user for the asked question."
            },
            {
                "step": 4,
                "task_type": "prompt_template",
                "task_name": "analyze_user_answer",
                "input_key": "user_answer, context",
                "output_key": "horoscope_prediction",
                "description": "Analyze user's answer using AI to predict horoscope."
            },
            {
                "step": 5,
                "task_type": "ui_output_text",
                "task_name": "show_horoscope_prediction",
                "input_key": "horoscope_prediction",
                "output_key": "none",
                "description": "Show the horoscope prediction to the user."
            }
        ]
        """,
        "code_snippets": """
        import streamlit as st
        from langchain import LLMChain
        from langchain.chat_models import ChatOpenAI
        from langchain.prompts.chat import (ChatPromptTemplate,
                                            HumanMessagePromptTemplate,
                                            SystemMessagePromptTemplate)


        st.title(My App)
        def horoscopeQuestionGenerator():
            chat = ChatOpenAI(
                temperature=0.7
            )
            system_template = "You are an AI assistant designed to generate intelligent questions related to horoscopes."
            system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
            human_template = "Please generate an intelligent question related to horoscopes."
            human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
            chat_prompt = ChatPromptTemplate.from_messages(
                [system_message_prompt, human_message_prompt]
            )

            chain = LLMChain(llm=chat, prompt=chat_prompt)
            result = chain.run({})
            return result # returns string   

        generated_questions = horoscopeQuestionGenerator()
        def show_question(generated_questions):
            if generated_questions != "":
                st.markdown("Question: " + generated_questions)

        show_question(generated_questions)
        user_answer = st.text_input("Enter your answer")
        def horoscopePredictor(user_answer,context):
            chat = ChatOpenAI(
                temperature=0
            )
            system_template = "You are skilled at predicting horoscopes based on analyzed traits and characteristics."
            system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
            human_template = "The user's answer is: {user_answer}. The context is: {context}. Please predict their horoscope based on this information."
            human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
            chat_prompt = ChatPromptTemplate.from_messages(
                [system_message_prompt, human_message_prompt]
            )

            chain = LLMChain(llm=chat, prompt=chat_prompt)
            result = chain.run(user_answer=user_answer, context=context)
            return result # returns string   

        horoscope_prediction = horoscopePredictor(user_answer,context)
        import streamlit as st

        def show_horoscope_prediction(horoscope_prediction):
            if horoscope_prediction != "":
                st.markdown("## Horoscope Prediction")
                st.markdown(horoscope_prediction)

        show_horoscope_prediction(horoscope_prediction)
        """,
    },
    {
        "instruction": """
        create a system that can translate a text to any determined language by the user
        """,
        "plan": """
        1. Get the source text from the user.
        2. Get the desired output language from the user.
        3. If both inputs are filled, use AI to translate the text to the output language.
        4. If the translation is ready, return it to the user.
        """,
        "task": """
        [
            {
                "step": 1,
                "task_type": "ui_input_text",
                "task_name": "get_source_text",
                "input_key": "none",
                "output_key": "source_text",
                "description": "Get the source text from the user."
            },
            {
                "step": 2,
                "task_type": "ui_input_text",
                "task_name": "get_output_language",
                "input_key": "none",
                "output_key": "output_language",
                "description": "Get the desired output language from the user."
            },
            {
                "step": 3,
                "task_type": "prompt_template",
                "task_name": "translate_text",
                "input_key": [
                    "source_text",
                    "output_language"
                ],
                "output_key": "translated_text",
                "description": "Use AI to translate the text to the output language."
            },
            {
                "step": 4,
                "task_type": "ui_output_text",
                "task_name": "display_translation",
                "input_key": "translated_text",
                "output_key": "none",
                "description": "Return the translated text to the user."
            }
        ]
        """,
        "code_snippets": """
        import streamlit as st
        from langchain import LLMChain
        from langchain.chat_models import ChatOpenAI
        from langchain.prompts.chat import (ChatPromptTemplate,
                                            HumanMessagePromptTemplate,
                                            SystemMessagePromptTemplate)


        st.title(My App)
        source_text = st.text_area("Enter the source text")
        button = st.button("Submit")
        output_language = st.text_input("Enter desired output language")
        button = st.button("Submit")
        def languageTranslator(source_text,output_language):
            chat = ChatOpenAI(
                temperature=0
            )
            system_template = "You are an AI language translator. Your task is to translate text to {output_language}."
            system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
            human_template = "Please translate the following text to {output_language}: '{source_text}'."
            human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
            chat_prompt = ChatPromptTemplate.from_messages(
                [system_message_prompt, human_message_prompt]
            )

            chain = LLMChain(llm=chat, prompt=chat_prompt)
            result = chain.run(source_text=source_text, output_language=output_language)
            return result # returns string   

        translated_text = languageTranslator(source_text,output_language)
        def show_translated_text(translated_text):
            if translated_text != "":
                st.markdown("Translated Text: " + translated_text)

        show_translated_text(translated_text)
        """,
    },
    {
        "instruction": """
        create lyrics from a song title
        """,
        "plan": """
        1. Get song title from the user.
        3. Use AI to generate lyrics appropriate for the song title.
        4. If lyrics is ready, display it to the user.
        """,
        "task": """
        [
            {
                "step": 1,
                "task_type": "ui_input_text",
                "task_name": "get_song_title",
                "input_key": "none",
                "output_key": "song_title",
                "description": "Gets song title from the user."
            },
            {
                "step": 2,
                "task_type": "prompt_template",
                "task_name": "generate_lyrics",
                "input_key": "song_title",
                "output_key": "lyrics",
                "description": "Use AI to generate lyrics for the song."
            },
            {
                "step": 3,
                "task_type": "ui_output_text",
                "task_name": "return_song",
                "input_key": "lyrics",
                "output_key": "none",
                "description": "If lyrics is ready, return it to the user."
            }
        ]
        """,
        "code_snippets": """
        import streamlit as st
        from langchain import LLMChain
        from langchain.chat_models import ChatOpenAI
        from langchain.prompts.chat import (ChatPromptTemplate,
                                            HumanMessagePromptTemplate,
                                            SystemMessagePromptTemplate)


        st.title(My App)
        song_title = st.text_input("Enter song title")
        button = st.button("Submit")
        def melodyGenerator(song_title):
            chat = ChatOpenAI(
                temperature=0.7
            )
            system_template = "You are an AI music composer. Your task is to generate a melody for the song '{song_title}'."
            system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
            human_template = "Please use AI to generate a melody for the song '{song_title}'."
            human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
            chat_prompt = ChatPromptTemplate.from_messages(
                [system_message_prompt, human_message_prompt]
            )

            chain = LLMChain(llm=chat, prompt=chat_prompt)
            result = chain.run(song_title=song_title)
            return result # returns string   

        melody = melodyGenerator(song_title)
        def lyricGenerator(song_title):
            chat = ChatOpenAI(
                temperature=0.7
            )
            system_template = "You are an AI songwriter. Your task is to generate lyrics for a song with the title: '{song_title}'."
            system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
            human_template = "Please generate lyrics for a song titled '{song_title}'."
            human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
            chat_prompt = ChatPromptTemplate.from_messages(
                [system_message_prompt, human_message_prompt]
            )

            chain = LLMChain(llm=chat, prompt=chat_prompt)
            result = chain.run(song_title=song_title)
            return result # returns string   

        lyrics = lyricGenerator(song_title)
        import streamlit as st

        def show_text(melody, lyrics):
            if melody != "" and lyrics != "":
                st.markdown("Melody: {}".format(melody))
                st.markdown("Lyrics: {}".format(lyrics))
            else:
                st.markdown("Please provide both melody and lyrics.")

        if melody != "" and lyrics != "":
            show_text(melody, lyrics)
        """,
    },
    {
        "instruction": """
        generate a system that reads uploaded text file and translates its content into the language that user prompted
        """,
        "plan": """
        1. Get the input language from the user.
        2. Get the output language from the user.
        3. Get the text file from the user.
        4. Read the content of the text file.
        5. Use AI to translate the content from the input language to the output language.
        6. If the translation is successful, return the translated content to the user.
        """,
        "task": """
        [
            {
                "step": 1,
                "task_type": "ui_input_text",
                "task_name": "get_input_language",
                "input_key": "none",
                "output_key": "input_language",
                "description": "Get the input language from the user."
            },
            {
                "step": 2,
                "task_type": "ui_input_text",
                "task_name": "get_output_language",
                "input_key": "none",
                "output_key": "output_language",
                "description": "Get the output language from the user."
            },
            {
                "step": 3,
                "task_type": "ui_input_file",
                "task_name": "get_text_file",
                "input_key": "none",
                "output_key": "text_file",
                "description": "Get the text file from the user."
            },
            {
                "step": 4,
                "task_type": "ui_output_text",
                "task_name": "read_text_file",
                "input_key": "text_file",
                "output_key": "file_content",
                "description": "Read the content of the text file."
            },
            {
                "step": 5,
                "task_type": "prompt_template",
                "task_name": "translate_content",
                "input_key": "file_content, input_language, output_language",
                "output_key": "translated_content",
                "description": "Use AI to translate the content from the input language to the output language."
            },
            {
                "step": 6,
                "task_type": "ui_output_text",
                "task_name": "return_translated_content",
                "input_key": "translated_content",
                "output_key": "none",
                "description": "If the translation is successful, return the translated content to the user."
            }
        ]
        """,
        "code_snippets": """
        import streamlit as st
        from langchain import LLMChain
        from langchain.chat_models import ChatOpenAI
        from langchain.prompts.chat import (ChatPromptTemplate,
                                            HumanMessagePromptTemplate,
                                            SystemMessagePromptTemplate)


        st.title(My App)
        input_language = st.text_input("Enter the input language")
        output_language = st.text_input("Enter the output language")
        if st.button("Submit"):
            # Perform some action with the output_language variable
        uploaded_file = st.file_uploader("Choose a file", type="txt")
        if uploaded_file is not None:
            text_file = uploaded_file.read().decode('utf-8')
            st.write(text_file)
        import streamlit as st

        def show_text(text_file):
            if text_file != "":
                with open(text_file, "r") as file:
                    text = file.read()
                st.markdown(text)

        show_text(text_file)
        def languageTranslator(file_content,input_language,output_language):
            chat = ChatOpenAI(
                temperature=0
            )
            system_template = "You are an AI language translator. Your task is to translate content from {input_language} to {output_language}."
            system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
            human_template = "Translate the following content from {input_language} to {output_language}:

        {file_content}"
            human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
            chat_prompt = ChatPromptTemplate.from_messages(
                [system_message_prompt, human_message_prompt]
            )

            chain = LLMChain(llm=chat, prompt=chat_prompt)
            result = chain.run(file_content=file_content, input_language=input_language, output_language=output_language)
            return result # returns string   

        translated_content = languageTranslator(file_content,input_language,output_language)
        import streamlit as st

        def show_text(translated_content):
            if translated_content != "":
                st.markdown(translated_content)

        show_text(translated_content)
        """,
    },
]

TOOL_EXAMPLES = {
    "ui_input_text": [
        {
            "instruction": "Get answer from the user for the asked question",
            "variable": "answer",
        },
        {"instruction": "Get song title from the user", "variable": "song_title"},
        {"instruction": "Get the source text from the user", "variable": "source_text"},
    ],
    "ui_output_text": [
        {
            "instruction": "Show the predicted horoscope to the user",
            "args": "horoscope",
        },
        {
            "instruction": "Return the translated text to the user",
            "args": "translated_text",
        },
        {"instruction": "Show the generated questions to the user", "args": "question"},
    ],
    "prompt_template": [
        {
            "instruction": "Generate intelligent questions related to horoscope",
            "inputs": "user",
        },
        {
            "instruction": "Analyze user's answers using AI to predict their horoscope",
            "inputs": "answer",
        },
        {
            "instruction": "Translate the text to the output language using AI",
            "inputs": """[
                "source_text",
                "output_language"
            ]""",
        },
    ],
}
