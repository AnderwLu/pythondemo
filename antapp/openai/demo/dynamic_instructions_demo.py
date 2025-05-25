"""
超简化版动态指令演示 - Ultra Simple Dynamic Instructions Demo
展示如何让大模型自动判断用户国家并修改上下文
"""

import asyncio
from dataclasses import dataclass
from typing import Any
from agents import Agent, Runner, function_tool, ModelSettings

# 定义用户上下文数据结构
@dataclass
class UserContext:
    name: str
    language: str   # "中文", "English"
    country: str = ""  # 添加国家字段
    greeting: str = ""  # 添加问候语字段

# 定义设置国家的工具函数
@function_tool
def set_user_country(country: str, context: UserContext) -> str:
    """设置用户的国家
    
    Args:
        country: 要设置的国家名称
        context: 用户上下文对象
    """
    # 直接修改上下文中的用户国家
    print(f"contextsssssss: {context}")
    context.country = country
    print(f"contextsssssss*****: {context}")
    print(f"已设置用户国家为：{country}")
    return f"已设置用户国家为：{country}"

# 定义设置问候语的工具函数
@function_tool
def set_user_greeting(greeting: str, context: UserContext) -> str:
    """设置用户的问候语
    
    Args:
        greeting: 要设置的问候语
        context: 用户上下文对象
    """
    # 直接修改上下文中的用户问候语
    context.greeting = greeting
    print(f"已设置用户问候语为：{greeting}")
    return f"已设置用户问候语为：{greeting}"

# 动态指令函数
def greeting_instructions(context, agent):
    """让模型根据用户语言判断国家并设置"""
    user = context.context
    
    if user.language == "English":
        return f"""You are an AI assistant. Please follow these rules:
1. Always respond in English
2. Be polite and professional
3. Address the user as {user.name}
4. Provide clear and concise answers
5. Based on the user's language preference, determine their most likely country
6. IMPORTANT: You must use the set_user_country function to set the user's country
7. For example, if you determine the user is from the UK, call: set_user_country("United Kingdom", context)
8. You can also use set_user_greeting to set a personalized greeting
9. In your response, mention the country you've determined for the user"""
    else:
        return f"""你是一个AI助手。请遵循以下规则：
1. 始终用中文回答
2. 保持礼貌和专业
3. 称呼用户为{user.name}
4. 提供清晰简洁的回答
5. 根据用户的语言偏好，判断他们最可能来自哪个国家
6. 重要：你必须使用 set_user_country 函数来设置用户的国家
7. 例如，如果你判断用户来自中国，就调用：set_user_country("中国", context)
8. 必须使用 set_user_greeting 来设置个性化的问候语
9. 在回答中提及你为用户确定的国家"""

# 创建 Agent 实例
greeting_agent = Agent(
    name="Greeting Agent",
    instructions=greeting_instructions,
    tools=[set_user_country, set_user_greeting],  # 添加多个工具函数
    model_settings=ModelSettings(tool_choice="set_user_country")  # 强制模型必须调用工具函数，但可以选择调用哪个
)

# 演示函数
async def demo_dynamic_instructions():
    """演示动态指令效果"""
    
    # 创建测试用户
    test_users = [
        UserContext(
            name="张三",
            language="中文"
        ),
        UserContext(
            name="John",
            language="English"
        )
    ]
    
    print("=" * 40)
    print("🎯 超简化版动态指令演示")
    print("=" * 40)
    
    for user in test_users:
        print(f"\n👤 用户：{user.name} ({user.language})")
        print("-" * 30)
        
        try:
            # 使用 Runner.run 运行 Agent
            result = await Runner.run(
                greeting_agent,
                "请介绍一下你自己，并告诉我你了解到的用户信息",  # 用户输入的消息
                context=user  # 用户上下文
            )
            print(f"\n🤖 回答：\n{result.final_output}")
            print(f"\n📝 用户信息")
            # 直接使用user对象，因为它已经被模型修改了
            print(f"姓名：{user.name}")
            print(f"语言：{user.language}")
            print(f"国家：{user.country}")
            print(f"问候语：{user.greeting}")
            
        except Exception as e:
            print(f"❌ 错误：{str(e)}")
        
        print("\n" + "=" * 40)

# 主函数
async def main():
    """主演示函数"""
    print("🚀 欢迎使用超简化版动态指令演示！")
    await demo_dynamic_instructions()
    print("\n✅ 演示完成！")

if __name__ == "__main__":
    asyncio.run(main()) 