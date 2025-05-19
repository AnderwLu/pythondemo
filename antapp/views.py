from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
from antproject.settings import BASE_DIR
from django.views.decorators.csrf import csrf_exempt
from django.http import StreamingHttpResponse
from antapp.openai.aiClient import AiClient  # type: ignore
import base64
# Create your views here.
def hello(request): 
    return HttpResponse("Hello, World!")

def index(request):
    return render(request,"index.html")

def show_excel(request):
    df = pd.read_excel(BASE_DIR /"datas/数据-学生成绩表.xlsx")
    if request.method == "POST":
        keyword = request.POST.get("keyword")
        df = df[df["姓名"].str.contains(keyword.strip())]
        return render(request, "show_excel.html", {"df": df,"keyword": keyword})
    else:
        return render(request, "show_excel.html", {"df": df})

def userManage(request):
    return render(request, "userManage.html")

@csrf_exempt
def deepseek(request):
    if request.method == "POST":
        images = request.FILES.getlist('images')
        keyword = request.POST.get("content")
        aiClient = AiClient()
        content = aiClient.get_stream_response(keyword)
        
        # 处理图片（如果需要的话）
        for image in images:
            print(image.name)

        return StreamingHttpResponse(content)
    
    return HttpResponse("清除成功")

@csrf_exempt
def deepseek_old(request):
    aiClient = AiClient()
    if request.method == "POST":
        images = request.FILES.getlist('images')
        keyword = request.POST.get("content")
        content = aiClient.get_stream_response_old(keyword)
        
        # 处理图片（如果需要的话）
        for image in images:
            print(image.name)

        return StreamingHttpResponse(content)
    
    return HttpResponse("清除成功")

@csrf_exempt
def deepseek_ams(request):
    aiClient = AiClient()
    if request.method == "POST":
        images = request.FILES.getlist('images')
        keyword = request.POST.get("content")
        content = aiClient.get_file_image(keyword, images)
        return StreamingHttpResponse(content)
    
    return HttpResponse("清除成功")

@csrf_exempt
def deepseek_reasoning(request):
    aiClient = AiClient()
    if request.method == "POST":
        images = request.FILES.getlist('images')
        keyword = request.POST.get("content")
        content = aiClient.get_reasoning(keyword)
        return StreamingHttpResponse(content)
    
    return HttpResponse("清除成功")

