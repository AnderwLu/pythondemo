# 动态指令演示 - Dynamic Instructions Demo

这个目录包含了动态指令（Dynamic Instructions）的演示代码，展示如何根据用户上下文动态调整 AI Agent 的行为和指令。

## 文件说明

### 1. `simple_dynamic_demo.py` - 简化演示（推荐）

-   ✅ **无外部依赖**，可以直接运行
-   🎯 展示动态指令的核心概念
-   🎮 提供交互式体验
-   📚 包含概念说明

### 2. `dynamic_instructions_demo.py` - 完整演示

-   🔧 需要 `agents` 库支持
-   🚀 更接近实际项目使用
-   🎯 展示完整的 Agent 集成

## 快速开始

### 运行简化演示

```bash
cd antapp/openai/demo
python simple_dynamic_demo.py
```

### 运行完整演示（需要 agents 库）

```bash
cd antapp/openai/demo
python dynamic_instructions_demo.py
```

## 演示内容

### 🎯 动态指令类型

1. **基础动态指令**

    - 根据用户姓名个性化问候
    - 展示最简单的动态指令概念

2. **VIP 等级指令**

    - 普通客户：标准服务
    - 银卡客户：专属客服
    - 金卡客户：高级顾问 + 投资建议
    - 钻石客户：私人银行顾问

3. **业务类型指令**

    - 开户：提供开户流程指导
    - 销户：说明销户注意事项
    - 查询：展示账户信息和查询选项
    - 转账：显示转账服务和余额

4. **时间感知指令**

    - 工作时间（9-17 点）：全业务服务
    - 延时服务（17-21 点）：基础业务
    - 非工作时间：仅紧急服务

5. **多语言指令**

    - 中文：中文服务界面
    - English：英文服务界面

6. **综合动态指令**
    - 结合所有因素的复合指令
    - 最接近实际应用场景

### 🎮 演示模式

#### 1. 自动演示

展示 3 个预设用户的所有动态指令效果：

-   张三（普通客户，开户业务）
-   李四（金卡客户，转账业务）
-   John Smith（钻石客户，查询业务，英文）

#### 2. 交互演示

用户可以自定义：

-   👤 用户姓名
-   💎 VIP 等级
-   🌍 语言偏好
-   💼 业务类型
-   💰 账户余额

#### 3. 概念说明

详细解释动态指令的：

-   核心概念
-   与静态指令的区别
-   优势和应用场景
-   在银行系统中的实际应用

## 核心概念

### 静态指令 vs 动态指令

```python
# 静态指令（传统方式）
agent = Agent(
    name="Static Agent",
    instructions="你是一个银行客服，请帮助用户。"  # 固定不变
)

# 动态指令（灵活方式）
def dynamic_instructions(context, agent):
    user = context.context
    return f"你好 {user.name}，我是专为您服务的{user.vip_level}客服。"

agent = Agent(
    name="Dynamic Agent",
    instructions=dynamic_instructions  # 根据上下文动态生成
)
```

### 执行流程

1. **Agent 初始化**：保存指令函数引用
2. **运行时调用**：传入用户上下文
3. **动态生成**：根据上下文生成个性化指令
4. **Agent 执行**：使用生成的指令处理请求

## 在银行项目中的应用

### 集成到现有系统

```python
# 在你的 antapp/agents/ams.py 中
def bank_dynamic_instructions(context, agent):
    user = context.context
    business_type = user.current_business_type

    if business_type == "开户":
        return f"""
        您好 {user.name}，我是开户业务专员。
        请准备好营业执照等相关材料...
        """
    elif business_type == "销户":
        return f"""
        您好 {user.name}，我是销户业务专员。
        请注意销户前需要确保账户余额为零...
        """
    # ... 更多业务类型

bank_agent = Agent(
    name="Bank Service Agent",
    instructions=bank_dynamic_instructions
)
```

### 扩展建议

1. **数据库集成**

    ```python
    def db_aware_instructions(context, agent):
        user = context.context
        # 从数据库查询用户历史
        history = get_user_history(user.user_id)
        # 根据历史调整指令
        return generate_personalized_instruction(user, history)
    ```

2. **地理位置感知**

    ```python
    def location_aware_instructions(context, agent):
        user = context.context
        if user.location == "北京":
            return "欢迎来到北京分行..."
        elif user.location == "上海":
            return "欢迎来到上海分行..."
    ```

3. **风险等级适配**
    ```python
    def risk_aware_instructions(context, agent):
        user = context.context
        if user.risk_level == "高风险":
            return "基于您的风险等级，我们需要额外验证..."
    ```

## 优势总结

-   🎯 **个性化服务**：根据用户信息定制体验
-   🕒 **上下文感知**：考虑时间、地点等环境因素
-   💼 **业务适配**：不同业务类型使用专业指令
-   🌍 **多语言支持**：自动适配用户语言偏好
-   🔐 **权限控制**：根据用户权限提供差异化服务
-   📊 **数据驱动**：可结合用户历史数据优化服务

## 下一步

1. 运行演示体验效果
2. 理解动态指令原理
3. 考虑在你的银行项目中的应用场景
4. 根据实际需求定制动态指令逻辑
