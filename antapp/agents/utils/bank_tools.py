import logging
import random
import string
from datetime import datetime
import requests
import json

logger = logging.getLogger(__name__)

class BankTools:
    """银行业务工具类，用于调用行内其他系统接口"""
    
    def __init__(self, api_base_url=None, api_key=None):
        """
        初始化银行业务工具
        
        Args:
            api_base_url: 行内API基础URL
            api_key: 行内API密钥
        """
        self.api_base_url = api_base_url or "http://localhost:4200"
        self.api_key = api_key
        # 在实际项目中，这里会初始化与行内系统的连接
    
    def call_remote_api(self, data):
        """
        调用远程开户接口
        Args:
            data: 开户数据
        Returns:
            dict: 接口响应结果
        """
        try:
            url = f"{self.api_base_url}/ams/ucamTest/save"
            headers = {
                'Content-Type': 'application/json'
            }
            
            logger.info(f"发送开户请求到: {url}")
            logger.info(f"请求数据: {json.dumps(data, ensure_ascii=False)}")
            
            response = requests.post(
                url=url,
                headers=headers,
                json=data,
                timeout=30
            )
            
            response.raise_for_status()
            response_data = response.json()
            logger.info(f"开户接口响应: {response_data}")
            return response_data
            
        except Exception as e:
            logger.error(f"调用远程接口失败: {str(e)}")
            raise Exception(f"调用远程接口失败: {str(e)}")
    
    def verify_business_license(self, license_info):
        """
        调用行内系统验证营业执照信息
        
        Args:
            license_info: 营业执照信息
            
        Returns:
            dict: 验证结果
        """
        logger.info(f"验证营业执照信息: {license_info.get('depositorName', '未知企业')}")
        
        # 实际项目中应调用行内验证接口
        # 这里模拟验证结果
        return {
            "verified": True,
            "message": "营业执照信息验证通过"
        }
    
    def check_blacklist(self, depositorName, fileNo1):
        """
        检查企业是否在黑名单中
        
        Args:
            company_name: 企业名称
            registration_number: 注册号/统一社会信用代码
            
        Returns:
            bool: 是否在黑名单中
        """
        logger.info(f"检查企业黑名单: {depositorName}")
        
        # 实际项目中应调用行内黑名单查询接口
        # 这里模拟查询结果
        return False
    
    def open_account(self, business_info):
        """执行开户操作"""
        try:
            logger.info(f"开户请求数据: {business_info}")
            # 生成账号
            account_number = self._generate_account_number()
            # 添加账号到业务数据中
            business_info['acctNo'] = account_number
            
            # 调用远程接口并等待结果
            remote_result = self.call_remote_api(business_info)
            
            # 返回结果
            result = {
                "success": True,
                "message": "开户成功",
                "account_info": {
                    "account_number": account_number,
                    "company_name": business_info['acctName'],
                    "open_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            }
            if(remote_result.get("rtncode") == "000000"):
                result["success"] = True
                result["message"] = "开户成功"
                logger.info(f"开户成功: {result}")
            else:
                result["success"] = False
                result["message"] = remote_result.get("rtnmsg", "开户失败，未知错误")
                logger.error(f"开户失败: {result}")
            return result
            
        except Exception as e:
            error_result = {
                "success": False,
                "message": f"开户失败：{str(e)}"
            }
            logger.error(f"开户操作异常: {error_result}")
            return error_result
    
    def close_account(self, account_info):
        """
        调用行内销户系统接口（当前未实现，为未来扩展预留）
        
        Args:
            account_info: 账户信息
            
        Returns:
            dict: 销户结果
        """
        logger.info(f"调用销户接口: {account_info.get('account_number', '未知账号')}")
        
        # 实际项目中应调用行内销户接口
        # 当前未实现
        return {
            "success": False,
            "message": "销户服务当前未开放"
        }
    
    def _generate_account_number(self):
        """模拟生成账号"""
        account_prefix = "1001"  # 假设银行账号前缀
        random_digits = ''.join(random.choice(string.digits) for _ in range(12))
        return account_prefix + random_digits 