from openai import OpenAI
import os
from dotenv import load_dotenv

# 获取 AI 的响应
def get_ai_response(user_content):
    load_dotenv()
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": user_content}
        ]
    )

    return response.choices[0].message.content

# 获取 AI 的响应
def get_stream_response(user_content):
    load_dotenv()
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    client = OpenAI()
    stream = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": user_content}
        ],
        stream=True
    )
    for chunk in stream:
        # 有的 chunk 可能没有 content，需要判空
        content = getattr(chunk.choices[0].delta, 'content', None)
        if content:
            # 创建了生成器，这里的逻辑是，外面调用遍历时候，驱动这里遍历遇到yield就返回，
            # 然后继续遍历，直到遍历结束。生成器会抛出 StopIteration 异常（调用方for 循环会自动捕获，不会报错）。
            # 核心逻辑是，调用get_stream_response时候才会驱动这里遍历返回
            yield content


# 测试代码
if __name__ == "__main__":
    test_content = "你是一个Java程序员写一个排序算法."
    result = get_stream_response(test_content)
    for event in result:
        print(event)