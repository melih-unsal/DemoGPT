import json
import os
import platform
import shutil
import sys
import tempfile
import threading
from subprocess import PIPE, Popen

from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (ChatPromptTemplate,
                                    HumanMessagePromptTemplate,
                                    SystemMessagePromptTemplate)
from pilmoji import Pilmoji
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2

def runThread(proc):
    proc.communicate()


def runStreamlit(code, openai_api_key):
    """
    Runs the provided code as a Streamlit application and returns the process ID.

    Args:
        code (str): The code of the Streamlit application.

    Returns:
        int: The process ID of the Streamlit application.
    """
    tmp = tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8")
    tmp.write(code)
    tmp.flush()
    environmental_variables = {
        "OPENAI_API_KEY": openai_api_key,
        "STREAMLIT_SERVER_PORT": "8502",
    }
    streamlit_path = shutil.which("streamlit")
    if True or platform.system() == "Windows":
        env = os.environ.copy()
        env["PYTHONPATH"] = ""
        env["OPENAI_API_KEY"] = openai_api_key
        env["STREAMLIT_SERVER_PORT"] = "8502"
        python_path = sys.executable
        process = Popen(
            [python_path, "-m", "streamlit", "run", tmp.name],
            env=env,
            stdout=PIPE,
            stderr=PIPE,
        )
        threading.Thread(target=runThread, args=(process,)).start()
    try:
        tmp.close()
    except PermissionError:
        pass

    return process.pid

system_template = """
You need to write an appropriate emoji for the description of the app idea
It needs to be a single emoji only
"""

human_template="""
Instruction:Create a system that can generate tweet from tweet tone
Emoji:🐦

Instruction:Create an app that can analyze pdf file
Emoji:📄

Instruction:{instruction}
Emoji:
"""

prompts = []
prompts.append(SystemMessagePromptTemplate.from_template(system_template))
prompts.append(HumanMessagePromptTemplate.from_template(human_template))
chat_prompt = ChatPromptTemplate.from_messages(prompts)

# Function to generate a random color
def random_color():
    return (np.random.randint(0, 256), np.random.randint(0, 256), np.random.randint(0, 256))

# Image dimensions
width, height = 220, 150

def generateImage(instruction, openai_api_key, openai_api_base):
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        openai_api_key=openai_api_key,
        openai_api_base=openai_api_base,
        temperature=0.3
        )
    chain =  LLMChain(llm=llm, prompt=chat_prompt)
    # Create a new image filled with zeros (black)
    image = np.zeros((height, width, 3), dtype=np.uint8)
    # Generate a random color
    color = random_color()
    # Fill the image with the random color
    image[:] = color
    """
    AI
    """
    # Text settings
    text = chain.run(instruction=instruction)

    image_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    draw = ImageDraw.Draw(image_pil)
    font = ImageFont.truetype('./src/prompt_based/arial.ttf', 48)
    
    # Step 1: Draw the emoji/text anywhere on the image
    with Pilmoji(image_pil) as pilmoji:
        pilmoji.text((100, 70), text, (0, 0, 0), font)
        
    # Convert back to numpy array for pixel operations
    image_np = np.array(image_pil)

    # Step 2: Find the bounding box of the emoji/text
    rows, cols = np.where(np.any(image_np != color[::-1], axis=2))
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)

    # Calculate text size from the bounding box
    textwidth = max_col - min_col
    textheight = max_row - min_row

    # Step 3: Calculate center position
    x = (width - textwidth) // 2
    y = (height - textheight) // 2

    # Clear the initial drawing and set the background color again
    image_np[:] = color

    # Step 4: Draw the emoji/text at the centered position
    image_pil = Image.fromarray(image_np)
    with Pilmoji(image_pil) as pilmoji:
        pilmoji.text((x, y), text, (0, 0, 0), font)

    image_with_text = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)

    return image_with_text


def getUrl(app_id):
    return f"https://demogpt.io/details?appID={app_id}"


"""

add this to the end of the streamlit_app.py for button press to redirect to the app page.

def callback():
    webbrowser.open_new_tab(st.session_state.url) 
if st.session_state.done: 
    st.button("Go To App", type="primary", on_click=callback)"""