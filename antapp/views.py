from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
from antproject.settings import BASE_DIR
from django.views.decorators.csrf import csrf_exempt
from django.http import StreamingHttpResponse
import antapp.openai.textAndPrompting as textAndPrompting  # type: ignore
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
        content = textAndPrompting.get_file_image(keyword, images)
        
        # 处理图片（如果需要的话）
        for image in images:
            print(image.name)

        return StreamingHttpResponse(content)
    
    return HttpResponse("清除欧克")

@csrf_exempt
def get_file_search(request):
    if request.method == "POST":
        images = request.FILES.getlist('images')
        keyword = request.POST.get("content")
        content = textAndPrompting.get_stream_response_to_file(keyword)

        return StreamingHttpResponse(content)
    
    return HttpResponse("清除欧克")



