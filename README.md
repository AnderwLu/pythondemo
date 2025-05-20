# 银行业务代理系统

这是一个基于 Django 和 OpenAI Agent SDK 的银行业务代理系统，可以处理企业开户和销户业务。

## 功能特点

-   **影像解析 Agent**：解析营业执照图片，提取企业信息
-   **开户 Agent**：处理企业开户业务
-   **销户 Agent**：处理企业销户业务（当前未开放）

## 系统结构

```
bank_agent_system/
├── agents/
│   ├── bank_agents.py  # 银行业务代理系统主文件
├── views_bank.py       # 银行业务代理视图
```

## 使用方法

1. 通过 API 调用银行业务功能：

    - POST `/api/bank/business` - 统一处理银行业务请求，支持文本指令和图片上传

2. 请求示例：

```
// 纯文本指令（如销户查询）
POST /api/bank/business
Content-Type: multipart/form-data

content: 我想销户
```

```
// 上传营业执照
POST /api/bank/business
Content-Type: multipart/form-data

content: 上传营业执照
images: [图片文件]
```

```
// 上传营业执照并同时开户（一体化流程）
POST /api/bank/business
Content-Type: multipart/form-data

content: 我想开户
images: [营业执照图片文件]
```

## 业务流程

1. **分步开户流程**：

    - 首先上传营业执照：`content="上传营业执照", images=[图片]`
    - 系统解析并返回企业信息
    - 然后请求开户：`content="开户"`
    - 系统完成开户并返回账号信息

2. **一体化开户流程**：

    - 一步完成：`content="我想开户", images=[营业执照图片]`
    - 系统解析营业执照并自动处理开户请求
    - 系统返回解析结果和开户结果

3. **销户流程**：
    - 发送销户请求：`content="销户"`
    - 系统提示销户业务未开放，并提供客服联系方式

## Agent 架构

系统使用 OpenAI Agent SDK 构建了多个专门的 Agent：

1. **Intent Recognition Agent**：识别用户意图
2. **Business License Analysis Agent**：营业执照解析
3. **Account Opening Agent**：处理开户业务
4. **Account Closing Agent**：处理销户业务
5. **Bank Business Agent**：主 Agent，协调各专门 Agent

## 示例对话

```
用户: 我想开户
系统: 请先上传您的营业执照图片进行解析。

用户: 上传营业执照
系统: 请上传您的营业执照图片以便系统解析企业信息。
// 用户上传图片
系统: 营业执照解析成功！
公司名称：示例科技有限公司
统一社会信用代码：91110123456ABCDEF
法定代表人：张三

如果信息无误，请输入"开户"继续办理开户业务。

用户: 开户
系统: 恭喜您！示例科技有限公司开户成功！
账号：10011234567890
请妥善保管您的账户信息。

用户: 销户
系统: 尊敬的客户，很抱歉，目前销户业务尚未开放。
如有紧急销户需求，请联系我行客服热线：400-123-4567。
```

## 配置要求

-   Python 3.8+
-   Django 3.2+
-   OpenAI API 密钥（需在环境变量中设置`OPENAI_API_KEY`）
