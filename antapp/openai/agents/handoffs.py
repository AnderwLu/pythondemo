import asyncio
from agents import GuardrailFunctionOutput, Agent, Runner
from pydantic import BaseModel

history_tutor_agent = Agent(
    name="History Tutor",
    handoff_description="历史问题的专家代理人",
    instructions="您为历史查询提供帮助。清楚地解释重要事件和背景.",
)

math_tutor_agent = Agent(
    name="Math Tutor",
    handoff_description="数学问题的专家代理",
    instructions="数学问题的专家代理你提供数学问题的帮助。解释你每一步的推理，并举例说明",
)
# 定义你的交接代理
triage_agent = Agent(
    name="Triage Agent",
    instructions="您可以根据用户的家庭作业问题来决定使用哪个代理",
    handoffs=[history_tutor_agent, math_tutor_agent]
)

# 运行代理业务流程
async def main():
    result = await Runner.run(triage_agent, "中国的首都是哪里？")
    print(result.final_output)

class HomeworkOutput(BaseModel):
    is_homework: bool
    reasoning: str

guardrail_agent = Agent(
    name="Guardrail check",
    instructions="检查用户是否在询问作业。",
    output_type=HomeworkOutput,
)

# 检查用户是否在询问作业，按照指定结果返回
async def homework_guardrail(ctx, agent, input_data):
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(HomeworkOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_homework,
    )

async def main1():
    # 创建所需的参数
    agent = Agent(name="Assistant", instructions="你是一个帮助检查作业的助手")
    
    # 创建上下文对象（这里需要根据实际的 Context 类来调整）
    class Context:
        def __init__(self):
            self.context = {}
    
    ctx = Context()
    
    # 测试输入
    input_data = "这是一道数学题：1+1=?"
    
    # 调用 homework_guardrail
    result = await homework_guardrail(ctx, agent, input_data)
    print("结果：", result)
if __name__ == "__main__":
    asyncio.run(main1())