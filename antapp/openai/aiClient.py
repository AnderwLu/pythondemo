from openai import OpenAI
import os
from dotenv import load_dotenv


# 在模块级别初始化
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_API_BASE = os.getenv('OPENAI_API_BASE', 'https://api.openai.com/v1')  # 默认使用官方API
DEFAULT_MODEL = os.getenv('OPENAI_MODEL_41_MINI', 'gpt-4') 

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_API_BASE
)