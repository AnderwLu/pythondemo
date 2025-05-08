from openai import OpenAI
from dotenv import load_dotenv
from antapp.loggingMy import logger    
from antapp.openai.aiClient import client, DEFAULT_MODEL
import base64
from typing import List

'''
获取AI的响应, 返回字符串
'''
def get_ai_response(user_content, model=DEFAULT_MODEL):
    logger.info(f"开始处理用户请求: {user_content[:100]}...")  # 只记录前100个字符
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": user_content}
            ]
        )
        logger.info("成功获取AI响应")
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"获取AI响应时发生错误: {str(e)}")
        raise

"""
获取流式响应
并添加到生成器
"""
def get_stream_response(user_content, model=DEFAULT_MODEL):
    logger.info(f"开始处理流式请求: {user_content[:100]}...")
    try:
        stream = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": user_content}
            ],
            stream=True
        )
        for chunk in stream:
            content = getattr(chunk.choices[0].delta, 'content', None)
            if content:
                yield content
        logger.info("流式响应完成")
    except Exception as e:
        logger.error(f"处理流式响应时发生错误: {str(e)}")
        raise

def get_file_image(user_content, images, model=DEFAULT_MODEL):
    # 构建消息列表
    messages = []
    
    # 添加用户文本内容
    messages.append({
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": user_content
            }
        ]
    })
    
    # 添加图片内容
    for image in images:
        # 直接读取InMemoryUploadedFile的内容
        base64_image = base64.b64encode(image.read()).decode('utf-8')
        
        # 添加图片到消息中
        messages[0]["content"].append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
        })
    
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    
    return response.choices[0].message.content

'''
获取流式响应, 返回字符串，添加openai的file_search工具
'''
def get_stream_response_to_file(user_content, model=DEFAULT_MODEL):
    logger.info(f"开始处理流式请求: {user_content[:100]}...")
    response = client.chat.completions.create(
        model=model,
        tools=[
            {
                "type": "file_search",
                "vector_store_ids": ["vs_1234567890"],
                "max_num_results": 20
            }
        ],
        messages=[
            {"role": "user", "content": "What are the attributes of an ancient brown dragon?"}
        ]
    )
    logger.info("成功获取AI响应")
    return response.choices[0].message.content

# 测试代码
if __name__ == "__main__":
    test_content = "你是一个Java程序员写一个排序算法."
    result = get_stream_response_to_file(test_content)
    print(result)