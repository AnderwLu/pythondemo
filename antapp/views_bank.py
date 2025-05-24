import logging
import asyncio
from django.http import StreamingHttpResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .agents.ams import main

logger = logging.getLogger(__name__)

@csrf_exempt
def bank_business(request):
    if request.method == "POST":
        images = request.FILES.getlist('images')
        keyword = request.POST.get("content")
        # 使用 asyncio.run 运行异步函数
        content = asyncio.run(main(keyword, images))
        return HttpResponse(content)
    return HttpResponse("清除成功")

@csrf_exempt
def ams_agent(request):
    if request.method == "POST":
        images = request.FILES.getlist('images')
        keyword = request.POST.get("content")
        # 使用 asyncio.run 运行异步函数
        content = asyncio.run(main(keyword, images))
        return HttpResponse(content)
    return HttpResponse("清除成功")