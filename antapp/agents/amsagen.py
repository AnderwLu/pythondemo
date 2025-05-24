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




async def main(input_data, images):
    # 创建上下文
    print(input_data)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 