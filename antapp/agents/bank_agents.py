from agents import Agent, Runner, InputGuardrail, GuardrailFunctionOutput
from pydantic import BaseModel, Field
import os
import base64
import json
import logging
import random
import string
from datetime import datetime
from typing import Optional, Dict, List, Any, Union

logger = logging.getLogger(__name__)

# 定义输出数据模型
class BusinessLicenseInfo(BaseModel):
    registration_number: Optional[str] = Field(None, description="注册号")
    company_name: Optional[str] = Field(None, description="企业名称")
    address: Optional[str] = Field(None, description="住所")
    legal_representative: Optional[str] = Field(None, description="法定代表人姓名")
    company_type: Optional[str] = Field(None, description="公司类型")
    registered_capital: Optional[str] = Field(None, description="注册资本")
    paid_in_capital: Optional[str] = Field(None, description="实收资本")
    business_scope: Optional[str] = Field(None, description="经营范围")
    establishment_date: Optional[str] = Field(None, description="成立日期")
    business_term: Optional[str] = Field(None, description="营业期限")
    annual_inspection: Optional[str] = Field(None, description="年检信息")

class AccountOpenResult(BaseModel):
    success: bool = Field(..., description="开户是否成功")
    message: str = Field(..., description="开户结果信息")
    account_info: Optional[Dict[str, str]] = Field(None, description="账户信息")

class AccountCloseResult(BaseModel):
    success: bool = Field(..., description="销户是否成功")
    message: str = Field(..., description="销户结果信息")
    service_status: Optional[str] = Field(None, description="服务状态")

class IntentOutput(BaseModel):
    intent: str = Field(..., description="用户意图")
    reasoning: str = Field(..., description="推理过程")

# 工具类：用于模拟银行系统接口
class BankTools:
    @staticmethod
    def generate_account_number():
        """生成模拟账号"""
        account_prefix = "1001"  # 银行账号前缀
        random_digits = ''.join(random.choice(string.digits) for _ in range(12))
        return account_prefix + random_digits
    
    @staticmethod
    def verify_business_license(license_info):
        """模拟验证营业执照信息"""
        logger.info(f"验证营业执照信息: {license_info.get('company_name', '未知企业')}")
        return {
            "verified": True,
            "message": "营业执照信息验证通过"
        }
    
    @staticmethod
    def check_blacklist(company_name, registration_number):
        """模拟黑名单检查"""
        logger.info(f"检查企业黑名单: {company_name}")
        return False

# 创建各个Agent
# 意图识别Agent
intent_agent = Agent(
    name="Intent Recognition Agent",
    instructions="""
    你是一个银行业务意图识别专家，负责分析用户的输入，确定他们想要执行什么银行业务。
    主要识别以下意图：
    1. open_account - 用户想开设银行账户
    2. close_account - 用户想销户
    3. upload_license - 用户想上传营业执照
    4. unknown - 无法确定用户意图
    
    仔细分析用户的表达和上下文，准确判断其意图。
    """,
    output_type=IntentOutput,
)

# 营业执照解析Agent
license_analysis_agent = Agent(
    name="Business License Analysis Agent",
    handoff_description="专门处理营业执照图片解析的专家",
    instructions="""
    你是一个专业的营业执照解析专家。
    你需要从营业执照图片中提取所有关键信息，包括：
    - 注册号/统一社会信用代码
    - 企业名称
    - 企业地址
    - 法定代表人
    - 注册资本
    - 公司类型
    - 经营范围
    - 成立日期
    - 营业期限
    
    确保提取的信息准确无误，并以结构化的方式返回。
    在解析过程中，注意图片质量可能不佳，需要尽力识别模糊或部分可见的文字。
    """,
    output_type=BusinessLicenseInfo,
)

# 开户Agent
account_open_agent = Agent(
    name="Account Opening Agent",
    handoff_description="处理企业开户业务的专家",
    instructions="""
    你是一个银行开户业务专家。
    
    你的职责是处理企业开户请求，包括：
    1. 验证企业信息的完整性和合法性
    2. 检查必要的开户条件
    3. 生成企业银行账号
    4. 返回开户结果
    
    在处理开户请求时，必须确保至少有以下信息：
    - 企业名称
    - 统一社会信用代码/注册号
    - 法定代表人姓名
    
    如果缺少必要信息，应该拒绝开户请求并给出明确的原因。
    如果企业信息满足要求，则创建账户并返回成功信息。
    """,
    output_type=AccountOpenResult,
)

# 销户Agent
account_close_agent = Agent(
    name="Account Closing Agent",
    handoff_description="处理企业销户业务的专家",
    instructions="""
    你是一个银行销户业务专家。
    
    目前销户业务尚未开放，你需要：
    1. 向用户说明当前销户服务的状态
    2. 提供客服热线信息，便于用户咨询紧急销户需求
    3. 解释销户服务暂未开放的原因
    
    客服热线: 400-123-4567
    """,
    output_type=AccountCloseResult,
)

# 主要的银行业务代理
bank_agent = Agent(
    name="Bank Business Agent",
    instructions="""
    你是银行业务智能代理系统，能够处理企业开户和销户相关业务。
    
    根据用户的请求，你需要正确理解用户意图，并调用相应的专业代理来处理具体业务。
    
    主要业务流程：
    1. 开户流程: 用户上传营业执照 -> 解析企业信息 -> 处理开户 -> 返回账号信息
    2. 销户流程: 用户请求销户 -> 检查服务状态 -> 返回销户结果
    
    注意事项：
    - 开户前必须先上传并解析营业执照
    - 目前销户业务尚未开放，需要引导用户联系客服
    - 用户可能使用不同的表达方式描述同一业务需求，需要准确识别
    """,
    handoffs=[license_analysis_agent, account_open_agent, account_close_agent],
)

# 全局状态存储
business_data = {
    "license_info": None
}

# 创建业务处理函数
async def process_bank_business(user_input, image_path=None):
    """
    处理银行业务请求
    
    Args:
        user_input: 用户输入文本
        image_path: 可选的营业执照图片路径
        
    Returns:
        str: 处理结果
    """
    # 识别用户意图
    intent_result = await Runner.run(intent_agent, user_input)
    intent_output = intent_result.final_output_as(IntentOutput)
    
    # 根据意图分发到相应的Agent
    if intent_output.intent == "open_account":
        # 检查是否已有营业执照信息
        if not business_data["license_info"]:
            return "请先上传您的营业执照图片进行解析。"
        
        # 处理开户请求
        open_result = await Runner.run(account_open_agent, json.dumps(business_data["license_info"]))
        open_output = open_result.final_output_as(AccountOpenResult)
        
        if open_output.success:
            account_info = open_output.account_info
            company_name = account_info.get("company_name", "您的企业")
            account_number = account_info.get("account_number", "")
            return f"恭喜您！{company_name}开户成功！\n账号：{account_number}\n请妥善保管您的账户信息。"
        else:
            return open_output.message
    
    elif intent_output.intent == "close_account":
        # 处理销户请求
        close_result = await Runner.run(account_close_agent, user_input)
        close_output = close_result.final_output_as(AccountCloseResult)
        return close_output.message
    
    elif intent_output.intent == "upload_license":
        # 检查是否提供了图片路径
        if not image_path:
            return "请上传您的营业执照图片以便系统解析企业信息。"
        
        # 解析营业执照
        try:
            license_result = await Runner.run(license_analysis_agent, f"解析图片路径: {image_path}")
            license_output = license_result.final_output_as(BusinessLicenseInfo)
            
            # 保存解析结果
            business_data["license_info"] = license_output.dict(exclude_none=True)
            
            # 格式化返回信息
            company_name = license_output.company_name or "未知企业"
            registration_number = license_output.registration_number or "未知注册号"
            legal_representative = license_output.legal_representative or "未知"
            
            message = f"""营业执照解析成功！
公司名称：{company_name}
统一社会信用代码：{registration_number}
法定代表人：{legal_representative}

如果信息无误，请输入"开户"继续办理开户业务。"""
            return message
        except Exception as e:
            logger.error(f"解析营业执照失败: {str(e)}")
            return f"营业执照解析失败，请重新上传清晰的图片。错误: {str(e)}"
    
    else:
        # 未知意图或欢迎消息
        return """您好，欢迎使用银行业务代理系统。您可以输入"开户"办理企业开户业务，或者"销户"查询销户业务状态。如需上传营业执照，请输入"上传营业执照"。"""

# 实现营业执照分析功能
async def analyze_business_license_image(image_path):
    """
    分析营业执照图片
    
    Args:
        image_path: 图片路径
        
    Returns:
        Dict: 包含企业信息的字典
    """
    try:
        # 读取图片并转换为base64
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        
        # 这里可以调用OpenAI的Vision API或其他图像识别服务
        # 为简化示例，这里省略实际API调用
        
        # 返回模拟的解析结果
        return {
            "company_name": "示例科技有限公司",
            "registration_number": "91110123456ABCDEF",
            "legal_representative": "张三",
            "address": "北京市海淀区xxxxx路xx号",
            "company_type": "有限责任公司",
            "registered_capital": "1000万元",
            "business_scope": "计算机软件开发与销售",
            "establishment_date": "2020-01-01"
        }
        
    except Exception as e:
        logger.error(f"解析营业执照失败: {str(e)}")
        return {"error": str(e)}

# 示例用法
async def main():
    # 模拟用户对话
    print("用户: 我想开户")
    response = await process_bank_business("我想开户")
    print(f"系统: {response}")
    
    print("\n用户: 上传营业执照")
    # 这里应该是实际上传图片的逻辑，这里用模拟数据
    response = await process_bank_business("上传营业执照", image_path="mock_license.jpg")
    print(f"系统: {response}")
    
    print("\n用户: 开户")
    response = await process_bank_business("开户")
    print(f"系统: {response}")
    
    print("\n用户: 销户")
    response = await process_bank_business("销户")
    print(f"系统: {response}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 