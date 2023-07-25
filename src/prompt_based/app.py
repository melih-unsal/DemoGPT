import logging
import os
import signal
import webbrowser
from time import sleep

import streamlit as st

from prompt_based.model import LogicModel, StreamlitModel


try:
    from dotenv import load_dotenv

    load_dotenv()
except Exception as e:
    logging.error("dotenv import error but no needed")


def main():

    num_of_iterations = 10


    def generate_response(txt):
        """
        Generate response using the LogicModel.

        Args:
            txt (str): The input text.

        Yields:
            dict: A dictionary containing response information.
        """
        for data in agent(txt, num_of_iterations):
            yield data


    # Page title
    title = "🧩 DemoGPT"

    st.set_page_config(page_title=title)
    st.title(title)
    # Text input

    openai_api_key = st.sidebar.text_input(
        "OpenAI API Key",
        placeholder="sk-...",
        value=os.getenv("OPENAI_API_KEY", ""),
        type="password",
    )
    demo_title = st.text_input("Enter your demo title", placeholder="Type your demo title")
    empty_idea = st.empty()
    demo_idea = empty_idea.text_area(
        "Enter your LLM-based demo idea", placeholder="Type your demo idea here", height=100
    )

    st.write("Examples")

    cols = st.columns([1, 1, 1.2])

    PROGRESS_BAR_TEXTS = {
        "start": "Generating Code...",
        "creating": "Creating App...",
        "refining": "Refining Code...",
        "failed": "Failed",
    }

    examples = [
        "Language Translator 📝",
        "Grammer Corrector 🛠",
        "Blog post generator from title 📔",
    ]

    if "pid" not in st.session_state:
        st.session_state["pid"] = -1

    example_submitted = False

    final_code_empty = st.empty()

    with st.form("a", clear_on_submit=True):
        submitted = st.form_submit_button("Submit")
        for col, example in zip(cols, examples):
            if col.button(example):
                example_submitted = True
                demo_idea = empty_idea.text_area(
                    "Enter your LLM-based demo idea", example, height=100
                )
                logging.info(f"Demo Idea:{demo_idea}")

        if submitted or example_submitted:

            if not openai_api_key.startswith("sk-"):
                st.warning("Please enter your OpenAI API Key!", icon="⚠️")
            else:
                agent = LogicModel(openai_api_key=openai_api_key)
                streamlit_agent = StreamlitModel(openai_api_key=openai_api_key)

                if st.session_state["pid"] != -1:
                    logging.info(f"Terminating the previous applicaton ...")
                    os.kill(st.session_state["pid"], signal.SIGTERM)
                    st.session_state["pid"] = -1

                bar = st.progress(25, PROGRESS_BAR_TEXTS["start"])
                for data in generate_response(demo_idea):
                    response = data["out"]
                    error = data["error"]
                    code = data["code"]
                    test_code = data["test_code"]
                    success = data["success"]
                    percentage = data["percentage"]

                    if success:
                        bar.progress(75, text=PROGRESS_BAR_TEXTS["creating"])
                        example_submitted = False
                        st.session_state["pid"], streamlit_code = streamlit_agent(
                            demo_idea,
                            demo_title,
                            code,
                            test_code,
                            bar.progress,
                            st.balloons,
                        )
                        with st.expander("Code"):
                            st.code(streamlit_code)
                        sleep(5)
                        webbrowser.open("http://localhost:8502")

                    else:
                        bar.progress(50, text=PROGRESS_BAR_TEXTS["refining"])

                    if success:
                        break
                else:
                    bar.progress(100, text=PROGRESS_BAR_TEXTS["failed"])

if __name__ == "__main__":
    main()