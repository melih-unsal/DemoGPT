import os
import logging
import torch
# 日志格式
LOG_FORMAT = "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s"
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.basicConfig(format=LOG_FORMAT)

llm_model_dict = {
    "chatglm-6b": {
        "model_name": "chatglm-6b",
        "local_model_path": "/opt/ChatGLM-6B/chatglm-6b/",
        "api_base_url": "http://localhost:8888/v1",  # "name"修改为fastchat服务中的"api_base_url"
        "api_key": "EMPTY"
    },

    "chatglm2-6b": {
        "model_name": "chatglm2-6b",
        "local_model_path": "/opt/ChatGLM2-6B/chatglm2-6b/",
        "api_base_url": "http://localhost:8888/v1",  # "name"修改为fastchat服务中的"api_base_url"
        "api_key": "EMPTY"
    },


    "vicuna-13b-hf": {
        "local_model_path": "vicuna-13b-hf",
        "api_base_url": "http://localhost:8888/v1",  # "name"修改为fastchat服务中的"api_base_url"
        "api_key": "EMPTY"
    },

    "gpt-3.5-turbo": {
        "local_model_path": "gpt-3.5-turbo",
        "api_base_url": "https://api.openai.com/v1",
        "api_key": os.environ.get("OPENAI_API_KEY")
    },

    "baichuan-7b": {
        "model_name": "baichuan-7b",
        "local_model_path": "/opt/baichuan-7B",
        "api_base_url": "http://localhost:8888/v1",  # "name"修改为fastchat服务中的"api_base_url"
        "api_key": "EMPTY"
    },
    "Baichuan-13b-Chat": {
        "model_name": "baichuan-13b",
        "local_model_path": "baichuan-inc/Baichuan-13b-Chat",
        "api_base_url": "http://localhost:8888/v1",  # "name"修改为fastchat服务中的"api_base_url"
        "api_key": "EMPTY"
    },

}

# LLM 名称
LLM_MODEL = "chatglm-6b"

# LLM 运行设备
LLM_DEVICE = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"

# 日志存储路径
LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)
