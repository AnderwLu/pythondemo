from agents import Agent, InputGuardrail, GuardrailFunctionOutput, Runner
from pydantic import BaseModel
import asyncio

class HomeworkOutput(BaseModel):
    is_homework: bool
    reasoning: str

guardrail_agent = Agent(
    name="Guardrail check",
    instructions="检查用户是否在询问作业。",
    output_type=HomeworkOutput,
)

math_tutor_agent = Agent(
    name="Math Tutor",
    handoff_description="数学问题的专家代理",
    instructions="你提供数学问题的帮助。解释你每一步的推理，并举例说明",
)

history_tutor_agent = Agent(
    name="History Tutor",
    handoff_description="历史问题的专家代理",
    instructions="你提供历史问题的帮助。解释你每一步的推理，并举例说明",
)


async def homework_guardrail(ctx, agent, input_data):
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(HomeworkOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_homework,
    )

triage_agent = Agent(
    name="Triage Agent",
    instructions="根据用户的问题决定使用哪个代理",
    handoffs=[history_tutor_agent, math_tutor_agent],
    input_guardrails=[
        InputGuardrail(guardrail_function=homework_guardrail),
    ],
)

async def main():
    result = await Runner.run(triage_agent, "中国的首都是哪里？")
    print(result.final_output)

    result = await Runner.run(triage_agent, "1+1=?")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())