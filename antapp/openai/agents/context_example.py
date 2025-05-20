from dataclasses import dataclass
from typing import List
import asyncio

# 定义一个简单的 Purchase 数据类
@dataclass
class Purchase:
    item_id: str
    amount: float

# 定义 UserContext 数据类
@dataclass
class UserContext:
    uid: str
    is_pro_user: bool

    async def fetch_purchases(self) -> List[Purchase]:
        # 模拟从数据库获取购买记录
        await asyncio.sleep(1)  # 模拟异步操作
        if self.is_pro_user:
            return [Purchase(item_id=f"item_{i}", amount=10.0 * i) for i in range(1, 4)]
        else:
            return [Purchase(item_id="basic_item", amount=5.0)]

# 定义一个简单的 Agent 类，接受 UserContext 作为泛型
class Agent:
    def __init__(self, name: str):
        self.name = name

    async def run(self, context: UserContext) -> str:
        # 根据上下文中的用户信息执行逻辑
        purchases = await context.fetch_purchases()
        if context.is_pro_user:
            return f"Agent {self.name} for PRO user {context.uid}: Found {len(purchases)} purchases: {[p.item_id for p in purchases]}"
        else:
            return f"Agent {self.name} for regular user {context.uid}: Found {len(purchases)} purchases: {[p.item_id for p in purchases]}"

# 主函数运行 demo
async def main():
    # 创建两个不同的上下文
    pro_user_context = UserContext(uid="user123", is_pro_user=True)
    regular_user_context = UserContext(uid="user456", is_pro_user=False)

    # 创建一个代理
    agent = Agent(name="ShoppingAgent")

    # 运行代理，传入不同的上下文
    pro_result = await agent.run(pro_user_context)
    regular_result = await agent.run(regular_user_context)

    print(pro_result)
    print(regular_result)

# 运行程序
if __name__ == "__main__":
    asyncio.run(main())