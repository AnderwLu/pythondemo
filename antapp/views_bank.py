import json
import os
import logging
import tempfile
import asyncio
from django.http import JsonResponse, StreamingHttpResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .agents.bank_agents import process_bank_business

logger = logging.getLogger(__name__)

@csrf_exempt
def bank_business(request):
    """处理银行业务请求，支持图片上传和文本指令"""
    try:
        if request.method == "POST":
            # 获取上传的图片文件
            images = request.FILES.getlist('images')
            # 获取用户指令
            message = request.POST.get("content", "").strip()
            
            logger.info(f"收到银行业务请求: {message}, 图片数量: {len(images)}")
            
            # 处理图片上传和业务指令
            if images and len(images) > 0:
                # 有图片上传，处理营业执照解析
                # 保存第一张图片到临时文件
                uploaded_file = images[0]
                with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
                    for chunk in uploaded_file.chunks():
                        temp_file.write(chunk)
                    temp_path = temp_file.name
                
                try:
                    # 解析营业执照图片
                    license_response = asyncio.run(process_bank_business("上传营业执照", image_path=temp_path))
                    
                    # 如果有开户指令，同时处理开户请求
                    if "开户" in message:
                        account_response = asyncio.run(process_bank_business("开户"))
                        response_text = f"{license_response}\n\n{account_response}"
                    else:
                        response_text = license_response
                finally:
                    # 确保临时文件被删除
                    if os.path.exists(temp_path):
                        os.unlink(temp_path)
            else:
                # 无图片上传，直接处理业务指令
                response_text = asyncio.run(process_bank_business(message))
            
            # 返回处理结果
            return JsonResponse({
                "success": True,
                "message": response_text
            }, json_dumps_params={'ensure_ascii': False})
        else:
            return HttpResponse("请通过POST方法提交银行业务请求")
            
    except Exception as e:
        logger.error(f"处理银行业务请求时发生错误: {str(e)}")
        return JsonResponse({
            "success": False,
            "message": f"系统处理请求时发生错误，请稍后重试或联系客服。错误: {str(e)}"
        }, json_dumps_params={'ensure_ascii': False}) 