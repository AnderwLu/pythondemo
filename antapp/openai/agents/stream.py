# 导入异步IO模块
import asyncio
# 导入随机数模块
import random
# 从agents模块导入所需的类和工具
from agents import Agent, ItemHelpers, Runner, function_tool
from django.http import StreamingHttpResponse
from asgiref.sync import sync_to_async

# 使用function_tool装饰器定义一个工具函数
@function_tool
def how_many_jokes() -> int:
    # 返回1到10之间的随机整数
    return "调用了工具接口how_many_jokes"

def stream_generator(agent, input_text):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    async def async_stream():
        result = Runner.run_streamed(
            agent,
            input=input_text
        )
        
        async for event in result.stream_events():
            if event.type == "raw_response_event":
                continue
            elif event.type == "agent_updated_stream_event":
                yield f"data: Agent updated: {event.new_agent.name}\n\n"
            elif event.type == "run_item_stream_event":
                if event.item.type == "tool_call_item":
                    yield f"data: -- Tool was called\n\n"
                elif event.item.type == "tool_call_output_item":
                    yield f"data: -- Tool output: {event.item.output}\n\n"
                elif event.item.type == "message_output_item":
                    yield f"data: {ItemHelpers.text_message_output(event.item)}\n\n"
    
    async_gen = async_stream()
    while True:
        try:
            chunk = loop.run_until_complete(async_gen.__anext__())
            yield chunk
        except StopAsyncIteration:
            break
    loop.close()

def main(input_text):
    agent = Agent(
        name="Joker",
        instructions="首先调用 how_many_jokes 工具，然后讲更多笑话.用中文回答所有问题",
        tools=[how_many_jokes],
    )
    
    return StreamingHttpResponse(
        stream_generator(agent, input_text),
        content_type='text/event-stream'
    )

# 程序入口点
if __name__ == "__main__":
    # 运行异步主函数
    asyncio.run(main("请给我讲 5 个笑话."))