"""
简化版动态指令演示 - Simple Dynamic Instructions Demo
不依赖外部库，直接展示动态指令的概念和效果
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any

# 定义用户上下文数据结构
@dataclass
class UserContext:
    name: str
    user_id: str
    vip_level: str  # "普通", "银卡", "金卡", "钻石"
    language: str   # "中文", "English"
    current_business: str  # "开户", "销户", "查询", "转账"
    account_balance: float
    login_time: datetime
    preferences: Dict[str, Any]

# 模拟 Agent 类
class SimpleAgent:
    def __init__(self, name: str, instructions_func):
        self.name = name
        self.instructions_func = instructions_func
    
    def get_instructions(self, context):
        """获取动态生成的指令"""
        return self.instructions_func(context, self)

# 动态指令函数定义

def basic_dynamic_instructions(context, agent):
    """基础的动态指令 - 根据用户姓名个性化"""
    user = context
    return f"你好！我是专为 {user.name} 服务的智能助手。请问有什么可以帮助您的吗？"

def vip_level_instructions(context, agent):
    """根据VIP等级提供不同服务质量"""
    user = context
    
    vip_messages = {
        "普通": f"您好 {user.name}，我是银行客服助手。",
        "银卡": f"尊敬的银卡客户 {user.name}，我是您的专属客服助手。",
        "金卡": f"尊敬的金卡贵宾 {user.name}，我是您的高级专属顾问。",
        "钻石": f"尊贵的钻石客户 {user.name}，我是您的私人银行顾问，随时为您提供最优质的服务。"
    }
    
    base_message = vip_messages.get(user.vip_level, vip_messages["普通"])
    
    # 根据VIP等级添加特殊服务说明
    if user.vip_level in ["金卡", "钻石"]:
        base_message += "\n我可以为您提供投资建议、理财规划等高端服务。"
    
    return base_message

def business_type_instructions(context, agent):
    """根据当前业务类型调整指令"""
    user = context
    
    business_instructions = {
        "开户": f"""您好 {user.name}，我是开户业务专员。

开户流程：
1. 请准备营业执照原件
2. 法定代表人身份证
3. 公司章程和股东会决议
4. 填写开户申请表

我会全程协助您完成开户手续。""",
        
        "销户": f"""您好 {user.name}，我是销户业务专员。

销户注意事项：
1. 确保账户余额为零
2. 处理完所有未完成交易
3. 准备相关证明文件
4. 法定代表人需要亲自办理

请确认您已了解销户流程。""",
        
        "查询": f"""您好 {user.name}，我是查询服务助手。

我可以帮您查询：
- 账户余额：{user.account_balance:.2f} 元
- 交易记录
- 账户状态
- 利率信息

请告诉我您需要查询什么信息。""",
        
        "转账": f"""您好 {user.name}，我是转账业务助手。

当前账户余额：{user.account_balance:.2f} 元

转账服务：
- 同行转账：实时到账
- 跨行转账：1-3个工作日
- 国际汇款：3-5个工作日

请提供转账详细信息。"""
    }
    
    return business_instructions.get(user.current_business, 
                                   f"您好 {user.name}，我是银行智能助手，请问需要什么帮助？")

def time_aware_instructions(context, agent):
    """根据时间提供不同服务"""
    user = context
    current_hour = datetime.now().hour
    
    if 9 <= current_hour <= 17:
        service_status = "工作时间，所有业务正常办理"
        available_services = "开户、销户、转账、查询等全部业务"
    elif 17 < current_hour <= 21:
        service_status = "延时服务时间，部分业务可办理"
        available_services = "查询、小额转账等基础业务"
    else:
        service_status = "非工作时间，仅提供紧急服务"
        available_services = "账户查询、紧急挂失等"
    
    return f"""您好 {user.name}！

当前时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
服务状态：{service_status}
可办理业务：{available_services}

请问有什么可以帮助您的？"""

def multilingual_instructions(context, agent):
    """根据用户语言偏好调整指令"""
    user = context
    
    if user.language == "English":
        return f"""Hello {user.name}! I'm your personal banking assistant.

VIP Level: {user.vip_level}
Current Business: {user.current_business}
Account Balance: ${user.account_balance:.2f}

How can I assist you today?"""
    else:
        return f"""您好 {user.name}！我是您的专属银行助手。

VIP等级：{user.vip_level}
当前业务：{user.current_business}
账户余额：{user.account_balance:.2f} 元

请问有什么可以为您服务的？"""

def comprehensive_instructions(context, agent):
    """综合考虑多个因素的动态指令"""
    user = context
    current_hour = datetime.now().hour
    
    # 基础问候
    if user.language == "English":
        greeting = f"Dear {user.name}"
        vip_title = {"普通": "Customer", "银卡": "Silver Member", 
                    "金卡": "Gold Member", "钻石": "Diamond Member"}[user.vip_level]
    else:
        greeting = f"尊敬的{user.name}"
        vip_title = user.vip_level + "客户"
    
    # 时间状态
    if 9 <= current_hour <= 17:
        time_status = "工作时间" if user.language == "中文" else "Business Hours"
    else:
        time_status = "非工作时间" if user.language == "中文" else "After Hours"
    
    # 构建完整指令
    if user.language == "English":
        instruction = f"""{greeting}, {vip_title}!

Current Status: {time_status}
Business Type: {user.current_business}
Account Balance: ${user.account_balance:.2f}

As your dedicated banking assistant, I'm here to provide you with 
personalized service based on your {user.vip_level} membership level.

How may I assist you today?"""
    else:
        instruction = f"""{greeting}，{vip_title}！

当前状态：{time_status}
业务类型：{user.current_business}
账户余额：{user.account_balance:.2f} 元

作为您的专属银行助手，我将根据您的{user.vip_level}会员等级
为您提供个性化的优质服务。

请问有什么可以为您效劳的？"""
    
    return instruction

# 创建不同的 Agent 实例
agents = {
    "基础动态指令": SimpleAgent("Basic Dynamic Agent", basic_dynamic_instructions),
    "VIP等级指令": SimpleAgent("VIP Service Agent", vip_level_instructions),
    "业务类型指令": SimpleAgent("Business Type Agent", business_type_instructions),
    "时间感知指令": SimpleAgent("Time Aware Agent", time_aware_instructions),
    "多语言指令": SimpleAgent("Multilingual Agent", multilingual_instructions),
    "综合动态指令": SimpleAgent("Comprehensive Agent", comprehensive_instructions)
}

def demo_dynamic_instructions():
    """演示不同的动态指令效果"""
    
    # 创建测试用户上下文
    test_users = [
        UserContext(
            name="张三",
            user_id="001",
            vip_level="普通",
            language="中文",
            current_business="开户",
            account_balance=50000.0,
            login_time=datetime.now(),
            preferences={"notification": True}
        ),
        UserContext(
            name="李四",
            user_id="002", 
            vip_level="金卡",
            language="中文",
            current_business="转账",
            account_balance=500000.0,
            login_time=datetime.now(),
            preferences={"investment_advice": True}
        ),
        UserContext(
            name="John Smith",
            user_id="003",
            vip_level="钻石",
            language="English", 
            current_business="查询",
            account_balance=1000000.0,
            login_time=datetime.now(),
            preferences={"private_banking": True}
        )
    ]
    
    print("=" * 80)
    print("🎯 动态指令演示 - Dynamic Instructions Demo")
    print("=" * 80)
    
    for user in test_users:
        print(f"\n👤 用户：{user.name} ({user.vip_level}, {user.language})")
        print(f"💼 业务：{user.current_business}")
        print(f"💰 余额：{user.account_balance:.2f}")
        print("-" * 60)
        
        for agent_name, agent in agents.items():
            try:
                print(f"\n🤖 {agent_name}:")
                instruction = agent.get_instructions(user)
                print(instruction)
                
            except Exception as e:
                print(f"❌ 错误：{str(e)}")
        
        print("\n" + "=" * 80)

def interactive_demo():
    """交互式演示，让用户自定义参数"""
    print("\n🎮 交互式动态指令演示")
    print("请输入用户信息来体验动态指令效果：")
    
    # 获取用户输入
    name = input("👤 用户姓名: ") or "测试用户"
    vip_level = input("💎 VIP等级 (普通/银卡/金卡/钻石): ") or "普通"
    language = input("🌍 语言 (中文/English): ") or "中文"
    business = input("💼 业务类型 (开户/销户/查询/转账): ") or "查询"
    
    try:
        balance = float(input("💰 账户余额: ") or "10000")
    except ValueError:
        balance = 10000.0
    
    # 创建用户上下文
    user = UserContext(
        name=name,
        user_id="interactive_001",
        vip_level=vip_level,
        language=language,
        current_business=business,
        account_balance=balance,
        login_time=datetime.now(),
        preferences={}
    )
    
    print(f"\n📋 用户信息确认：")
    print(f"姓名：{user.name}")
    print(f"VIP等级：{user.vip_level}")
    print(f"语言：{user.language}")
    print(f"业务：{user.current_business}")
    print(f"余额：{user.account_balance:.2f}")
    
    # 展示综合动态指令效果
    print(f"\n🤖 综合动态指令生成结果：")
    print("-" * 60)
    
    comprehensive_agent = agents["综合动态指令"]
    instruction = comprehensive_agent.get_instructions(user)
    print(instruction)

def show_concept():
    """展示动态指令的核心概念"""
    print("\n📚 动态指令核心概念：")
    print("-" * 40)
    
    print("""
🔄 动态指令 vs 静态指令：

静态指令（传统方式）：
```python
agent = Agent(
    name="Static Agent",
    instructions="你是一个银行客服，请帮助用户。"  # 固定不变
)
```

动态指令（灵活方式）：
```python
def dynamic_instructions(context, agent):
    user = context.context
    return f"你好 {user.name}，我是专为您服务的{user.vip_level}客服。"

agent = Agent(
    name="Dynamic Agent", 
    instructions=dynamic_instructions  # 根据上下文动态生成
)
```

🎯 优势：
1. 个性化服务 - 根据用户信息定制
2. 上下文感知 - 考虑时间、地点等因素
3. 业务适配 - 根据不同业务类型调整
4. 多语言支持 - 自动适配用户语言
5. 权限控制 - 根据用户权限提供不同服务

🏦 在银行系统中的应用：
- VIP客户享受专属服务话术
- 不同业务类型使用专业指令
- 工作时间外提供有限服务
- 多语言客户自动切换语言
- 根据账户状态调整服务内容
    """)

def main():
    """主演示函数"""
    print("🚀 欢迎使用动态指令演示系统！")
    
    while True:
        print("\n请选择演示模式：")
        print("1. 自动演示 - 展示所有预设场景")
        print("2. 交互演示 - 自定义用户参数")
        print("3. 概念说明 - 了解动态指令原理")
        print("4. 退出")
        
        choice = input("\n请输入选择 (1-4): ").strip()
        
        if choice == "1":
            demo_dynamic_instructions()
        elif choice == "2":
            interactive_demo()
        elif choice == "3":
            show_concept()
        elif choice == "4":
            print("👋 感谢使用！")
            break
        else:
            print("❌ 无效选择，请重新输入")
    
    print("\n💡 提示：在实际项目中，你可以：")
    print("1. 将这些动态指令集成到你的银行 Agent 系统中")
    print("2. 根据实际业务需求调整指令逻辑")
    print("3. 添加更多的上下文因素（如地理位置、历史行为等）")
    print("4. 结合数据库查询实现更复杂的个性化服务")

if __name__ == "__main__":
    main() 