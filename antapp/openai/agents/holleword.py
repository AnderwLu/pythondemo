from agents import Agent, Runner

# 创建一个智能代理
agent = Agent(name="Assistant", instructions="你是一个智能代理，请根据用户的问题给出回答")

# 运行智能代理
result = Runner.run_sync(agent, "你是哪个模型.")
print(result.final_output)