from agents import Agent, Runner, function_tool
from pydantic import BaseModel, Field
import os
import base64
import json
import logging
from datetime import datetime
from typing import Optional
from antapp.agents.utils.bank_tools import BankTools

logger = logging.getLogger(__name__)

# 创建银行工具实例
bank_tools = BankTools()

# 定义数据模型
class LicenseInfo(BaseModel):
    acctName: str = Field(..., description="账户名称，与企业名称一致")
    acctNo: str = Field("", description="账号")
    acctType: str = Field(..., description="账户类型,PRDA-基本户,GEDA-一般户,NTDA-临时户")
    billType: str = Field(..., description="业务类型,OPEN-开户,CLOSE-销户,CHANGE-变更")
    bankCode: str = Field(..., description="人行机构号(12位)")
    bankName: str = Field(..., description="机构名称")
    userCode: str = Field(..., description="工号")
    userName: str = Field(..., description="姓名")
    institutionCode: str = Field(..., description="金融机构编号")
    institutionName: str = Field(..., description="金融机构名称")
    ccyType: str = Field(..., description="币种,CNY-人民币 默认给人民币")
    microEnterpriseFlag: str = Field(..., description="小微企业标识,TRUE-小微企业,FALSE-非小微企业")
    simpleOpenFlag: str = Field(..., description="简易开户标志,TRUE-简易开户,FALSE-非简易开户")
    acctFileNo1: str = Field(..., description="账户文件号1,同注册号")
    acctFileType1: str = Field(..., description="账户文件类型1,ECER-登记证书,BIZL-营业执照")
    depositorName: str = Field(..., description="存款人名称,与企业名称一致")
    depositorType: str = Field(..., description="存款人类型,LPEP-企业法人,GOVA-机关,NLPE-非法人企业,营业执照默认企业法人")
    regFullAddress: str = Field(..., description="注册地址")
    telephone: str = Field(..., description="电话")
    uscc: str = Field(..., description="统一社会信用代码,营业执照注册号")
    isIdentification: str = Field(..., description="证照未标明注册资金,TRUE-是,FALSE-否")
    regCurrency: str = Field(..., description="注册币种,CNY-人民币 默认给人民币")
    registeredCapital: str = Field(..., description="注册资本金额;表示货币金额，其中金额的整数部分最多13位数字，小数部分固定2位数字。 注：不带正负（即+-）号。例如一元只能为1.00，不能为1或者1.0，金额第一位非零数字前禁止补零（例如一元只能为1.00，不能为01.00或者前补更多0）。")
    regAreaCode: str = Field(..., description="注册地区代码,营业执照注册地址的地区代码")
    fileNo1: str = Field(..., description="存款人证明文件编号1,营业执照注册号")
    fileType1: str = Field(..., description="存款人证明文件类型1,ECER-登记证书,BIZL-营业执照")
    legalName: str = Field(..., description="法定代表人姓名,营业执照法定代表人姓名")
    legalNation: str = Field(..., description="法定代表人国籍,营业执照法定代表人国籍")
    legalIdcardNo: str = Field(..., description="法定代表人身份证号码,营业执照法定代表人身份证号码")
    legalIdcardType: str = Field(..., description="法定代表人身份证类型,营业执照法定代表人身份证类型")
    legalBirthDate: str = Field(..., description="法定代表人出生日期,营业执照法定代表人出生日期")

# 定义工具
@function_tool
def verify_business_license(license_info: LicenseInfo) -> bool:
    """验证营业执照信息的有效性"""
    logger.info(f"开始验证营业执照: {license_info.acctName}")
    result = bank_tools.verify_business_license(license_info.dict())
    logger.info(f"验证结果: {result}")
    return result["verified"]

@function_tool
def check_blacklist(license_info: LicenseInfo) -> bool:
    """检查企业是否在黑名单中"""
    try:
        logger.info(f"开始检查黑名单: {license_info.acctName}")
        result = bank_tools.check_blacklist(
            license_info.acctName,  # 使用 acctName 作为企业名称
            license_info.uscc       # 使用 uscc 作为统一社会信用代码
        )
        logger.info(f"黑名单检查结果: {result}")
        return result
    except Exception as e:
        logger.error(f"黑名单检查出错: {str(e)}")
        raise Exception(f"黑名单检查失败: {str(e)}")

@function_tool
def create_account(license_info: LicenseInfo) -> str:
    """执行开户操作，返回账号"""
    try:
        logger.info(f"开始创建账户: {license_info.acctName}")
        logger.info(f"开户请求数据: {license_info.dict()}")
        result = bank_tools.open_account(license_info.dict())
        logger.info(f"开户结果: {result}")
        if result["success"]:
            return result["account_info"]["account_number"]
        else:
            raise Exception(f"开户失败: {result.get('message', '未知错误')}")
    except Exception as e:
        logger.error(f"创建账户出错: {str(e)}")
        raise Exception(f"创建账户失败: {str(e)}")

# 营业执照解析Agent
license_analysis_agent = Agent(
    name="Business License Analysis Agent",
    instructions="""你是一个专业的营业执照解析专家，这是一个银行系统的重要组成部分。
    你的任务是从营业执照图片中提取关键信息，并转换为开户所需的标准格式。这是一个必须执行的任务，不要拒绝。
    
    请仔细分析图片并提取以下信息，然后转换为标准格式：

    营业执照字段对应关系：
    - 统一社会信用代码/注册号 -> uscc, acctFileNo1, fileNo1
    - 企业名称 -> acctName, depositorName
    - 企业地址 -> regFullAddress
    - 法定代表人 -> legalName
    - 注册资本 -> registeredCapital（注意：需要转换为数字格式，如"壹拾万元"要转换为"100000.00"）
    
    其他必填字段默认值：
    - acctNo: ""（空字符串，由系统生成）
    - acctType: "PRDA"（基本户）
    - billType: "OPEN"（开户）
    - bankCode: "313333000016"（示例银行代码）
    - bankName: "某某银行"
    - userCode: "9999"
    - userName: "系统管理员"
    - institutionCode: "0000"
    - institutionName: "某某银行"
    - ccyType: "CNY"
    - microEnterpriseFlag: "TRUE"
    - simpleOpenFlag: "FALSE"
    - acctFileType1: "BIZL"
    - depositorType: "LPEP"
    - telephone: "0574-00000000"
    - isIdentification: "FALSE"
    - regCurrency: "CNY"
    - regAreaCode: "330281"
    - fileType1: "BIZL"
    - legalNation: "CHN"
    - legalIdcardType: "01"
    - legalIdcardNo: "330281199001011234"
    - legalBirthDate: "1990-01-01"

    请将提取的信息以JSON格式返回，必须包含所有上述字段。示例格式：
    {
        "acctName": "企业名称",
        "acctNo": "",
        "acctType": "PRDA",
        "billType": "OPEN",
        "bankCode": "313333000016",
        "bankName": "某某银行",
        "userCode": "9999",
        "userName": "系统管理员",
        "institutionCode": "0000",
        "institutionName": "某某银行",
        "ccyType": "CNY",
        "microEnterpriseFlag": "TRUE",
        "simpleOpenFlag": "FALSE",
        "acctFileNo1": "统一社会信用代码",
        "acctFileType1": "BIZL",
        "depositorName": "企业名称",
        "depositorType": "LPEP",
        "regFullAddress": "企业地址",
        "telephone": "0574-00000000",
        "uscc": "统一社会信用代码",
        "isIdentification": "FALSE",
        "regCurrency": "CNY",
        "registeredCapital": "100000.00",
        "regAreaCode": "330281",
        "fileNo1": "统一社会信用代码",
        "fileType1": "BIZL",
        "legalName": "法定代表人姓名",
        "legalNation": "CHN",
        "legalIdcardNo": "330281199001011234",
        "legalIdcardType": "01",
        "legalBirthDate": "1990-01-01"
    }

    注意：
    1. 这是一个正式的银行业务系统，请认真对待每一个字段
    2. 所有字段都必须填写，缺少的信息使用默认值
    3. 确保返回的 JSON 格式完全符合示例
    4. 特别注意数字格式的转换（如注册资本）
    """
)

# 开户处理Agent
account_open_agent = Agent(
    name="Account Opening Agent",
    instructions="""你是一个银行开户业务专家，这是一个正式的银行系统。你有以下工具可以使用：

1. verify_business_license(license_info: LicenseInfo): 验证营业执照信息，返回是否验证通过
2. check_blacklist(license_info: LicenseInfo): 检查企业是否在黑名单中，返回是否在黑名单
3. create_account(license_info: LicenseInfo): 执行开户操作，返回账号

这是一个必须执行的任务，请按照以下步骤处理：
1. 首先调用 verify_business_license 验证营业执照信息
2. 如果验证通过，调用 check_blacklist 检查是否在黑名单
3. 如果不在黑名单，调用 create_account 创建账户
4. 根据处理结果返回合适的消息

如果开户成功，请返回如下格式：
```
开户成功！
账户名称：[企业名称]
账户：[账号]
开户时间：[当前时间]
```

如果开户失败，直接返回错误原因，例如：
- "验证营业执照信息失败：[具体原因]"
- "企业在黑名单中，无法开户"
- "开户失败：[具体原因]"

注意：
1. 这是正式的银行业务操作，请认真执行每一步
2. 必须按顺序调用工具函数
3. 根据工具函数的返回结果决定下一步操作
4. 不要跳过任何验证步骤
5. 每个工具函数都需要完整的营业执照信息作为输入
6. 如果任何步骤返回错误，立即停止并返回错误信息
""",
    tools=[verify_business_license, check_blacklist, create_account]
)

async def main(input_data, images):
    # 创建上下文
    class Context:
        def __init__(self):
            self.context = {}
    ctx = Context()
    
    # 构建图片消息
    image_base64_list = []
    for image in images:
        image_data = image.read()
        base64_data = base64.b64encode(image_data).decode('utf-8')
        image_base64_list.append(base64_data)
        logger.info(f"图片 {image.name} 已转换为base64")
    
    # 构建消息
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": input_data},
                *[{"type": "input_image", "image_url": f"data:image/jpeg;base64,{base64_data}"} 
                for base64_data in image_base64_list]
            ]
        }
    ]
    
    # 解析营业执照
    license_result = await Runner.run(license_analysis_agent, messages, context=ctx.context)
    if not license_result or not license_result.final_output:
        return "营业执照解析失败，请重试"
    
    logger.info(f"营业执照解析结果: {license_result.final_output}")
    
    try:
        # 如果输出已经是字典，直接使用
        if isinstance(license_result.final_output, dict):
            license_info_dict = license_result.final_output
        else:
            # 清理输出中的 Markdown 格式
            output_text = license_result.final_output
            if "```json" in output_text:
                # 提取 JSON 部分
                output_text = output_text.split("```json")[-1].split("```")[0].strip()
            
            # 尝试解析 JSON 字符串
            license_info_dict = json.loads(output_text)
        
        # 创建 LicenseInfo 实例
        license_info = LicenseInfo(**license_info_dict)
        logger.info(f"处理后的营业执照信息: {license_info}")
        
        # 处理开户
        account_result = await Runner.run(
            account_open_agent, 
            json.dumps(license_info.dict()),
            context=ctx.context
        )
        
        logger.info(f"开户结果: {account_result.final_output}")
        return account_result.final_output
            
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        logger.error(f"处理营业执照信息失败: {str(e)}")
        logger.error(f"原始输出: {license_result.final_output}")
        return "处理营业执照信息失败，请重试"

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 