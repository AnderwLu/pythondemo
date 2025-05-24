import asyncio

from pydantic import BaseModel

from agents import Agent, Runner, trace

"""
这个示例演示了一个确定性流，其中每个步骤都由一个代理执行。
1. 第一个代理生成一个故事大纲
2. 我们把大纲输入第二个特工
3. 第二个代理人检查大纲是否质量好，是否是一个科幻故事
4. 如果大纲质量不好或者不是科幻故事，我们就到此为止
5. 如果大纲质量好，而且是一个科幻故事，我们就把大纲输入第三个代理
6. 第三个特工写故事
"""

story_outline_agent = Agent(
    name="story_outline_agent",
    instructions="根据用户的输入生成一个非常短的故事大纲。",
)


class OutlineCheckerOutput(BaseModel):
    good_quality: bool
    is_scifi: bool


outline_checker_agent = Agent(
    name="outline_checker_agent",
    instructions="阅读给定的故事大纲，并判断其质量。另外，确定它是否是一个科幻故事。",
    output_type=OutlineCheckerOutput,
)

story_agent = Agent(
    name="story_agent",
    instructions="根据给定的大纲写一篇短篇故事。",
    output_type=str,
)


async def main():
    input_prompt = "三只小羊去外太空的故事"

    # Ensure the entire workflow is a single trace
    with trace("Deterministic story flow"):
        # 1. Generate an outline
        outline_result = await Runner.run(
            story_outline_agent,
            input_prompt,
        )
        print(outline_result.final_output)

        # 2. Check the outline
        outline_checker_result = await Runner.run(
            outline_checker_agent,
            outline_result.final_output,
        )

        # 3. Add a gate to stop if the outline is not good quality or not a scifi story
        assert isinstance(outline_checker_result.final_output, OutlineCheckerOutput)
        print(outline_checker_result.final_output)
        if not outline_checker_result.final_output.good_quality:
            print("提纲的质量不太好，所以我们就到此为止。")
            exit(0)

        if not outline_checker_result.final_output.is_scifi:
            print("《大纲》不是科幻小说，所以我们就讲到这里。")
            exit(0)

        print("《大纲》是一个质量很好的科幻故事，所以我们继续写这个故事。")

        # 4. Write the story
        story_result = await Runner.run(
            story_agent,
            outline_result.final_output,
        )
        print(f"Story: {story_result.final_output}")


if __name__ == "__main__":
    asyncio.run(main())