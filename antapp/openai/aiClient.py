from openai import OpenAI
import os
from dotenv import load_dotenv
import logging
from antapp.loggingMy import get_logger
import base64


# 在模块级别初始化
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_API_BASE = os.getenv('OPENAI_API_BASE', 'https://api.openai.com/v1')  # 默认使用官方API
DEFAULT_MODEL = os.getenv('OPENAI_MODEL_41_MINI', 'gpt-4') 

# 获取logger
logger = get_logger('aiClient')

class AiClient:
    def __init__(self, model=DEFAULT_MODEL,messages=[]):
        self.model = model
        self.messages = messages
        self.client = OpenAI(
            api_key=OPENAI_API_KEY,
            base_url=OPENAI_API_BASE
        )
        logger.info("AiClient实例化成功，模型: %s", model)

    def get_ai_response(self, user_content):
        logger.info("当前消息列表: %s", self.messages)
        self.messages.append({"role": "user", "content": user_content})
        logger.info("用户消息: %s", user_content)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages = self.messages
            )
            ai_response = response.choices[0].message.content
            self.messages.append({"role": "assistant", "content": ai_response})
            logger.info("AI响应: %s", ai_response)
            return ai_response
        except Exception as e:
            logger.error("获取AI响应时出错: %s", str(e))
            raise

    def get_stream_response_old(self, user_content):
        logger.info("流式响应请求，用户消息: %s", user_content)
        self.messages.append({"role": "user", "content": user_content})
        
        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                stream=True
            )
            logger.info("开始接收流式响应")
            for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    logger.debug("流式响应片段: %s", content)
                    yield content
            logger.info("流式响应完成")
        except Exception as e:
            logger.error("获取流式响应时出错: %s", str(e))
            raise

    def get_stream_response(self, user_content):
        logger.info("流式响应请求，用户消息: %s", user_content)
        self.messages.append({"role": "user", "content": user_content})
        
        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages = [{"role": "user", "content": user_content}],
                stream=True
            )
            logger.info("开始接收流式响应")
            for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    logger.debug("流式响应片段: %s", content)
                    yield content
            logger.info("流式响应完成")
        except Exception as e:
            logger.error("获取流式响应时出错: %s", str(e))
            raise

    def get_file_image(self, user_content, images):
        logger.info("文件图片请求，用户消息: %s", user_content)
        try:
            # 构建包含base64图片的消息
            image_base64_list = []
            for image in images:
                # 读取图片数据并转换为base64
                image_data = image.read()  # 读取文件内容为字节
                base64_data = base64.b64encode(image_data).decode('utf-8')
                image_base64_list.append(base64_data)
                logger.info(f"图片 {image.name} 已转换为base64")
            
            # 构建新的消息对象，只包含当前图片和问题
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": user_content},
                        *[{"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_data}"}} 
                          for base64_data in image_base64_list]
                    ]
                }
            ]
            
            # 使用正确的API调用方式，不保存到历史消息中
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,  # 直接使用当前消息，不包含历史
                stream=True
            )
            
            logger.info("开始接收流式响应")
            for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    logger.debug("流式响应片段: %s", content)
                    yield content
            logger.info("流式响应完成")
            
        except Exception as e:
            logger.error("处理图片时出错: %s", str(e))
            yield f"处理图片时出错: {str(e)}"
        
    def get_reasoning(self, user_content):
        logger.info("推理请求，用户消息: %s", user_content)
        try:
            stream = self.client.chat.completions.create(
                model="o3-mini",
                messages=[
                    {
                        "role": "user", 
                        "content": user_content
                    }
                ],
                temperature=0.7,  # 控制输出的随机性，值越低输出越确定
                top_p=0.9,       # 控制输出的多样性，值越低输出越保守
                max_tokens=1000,  # 控制输出的最大长度
                stream=True
            )
            logger.info("开始接收流式响应")
            for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    logger.debug("流式响应片段: %s", content)
                    yield content
            logger.info("流式响应完成")
        except Exception as e:
            logger.error("获取流式响应时出错: %s", str(e))
            raise
        
