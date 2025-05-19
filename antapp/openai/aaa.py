import img2pdf
import camelot
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# 输入和输出文件路径
image_path = BASE_DIR / "datas/table.png"  # 替换为你的图片路径
pdf_path = BASE_DIR / "datas/有限空间管控流程图.pdf"
excel_path = BASE_DIR / "datas/output.xlsx"

# 步骤1：将图片转换为PDF
def image_to_pdf(image_path, pdf_path):
    try:
        # 检查图片是否存在
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"图片文件 {image_path} 不存在")
        
        # 转换图片为PDF
        with open(pdf_path, "wb") as f:
            f.write(img2pdf.convert(image_path))
        print(f"成功将 {image_path} 转换为 {pdf_path}")
    except Exception as e:
        print(f"图片转PDF失败: {e}")
        return False
    return True

# 步骤2：使用Camelot提取表格并保存为Excel
def extract_table_to_excel(pdf_path, excel_path):
    try:
        # 检查PDF是否存在
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF文件 {pdf_path} 不存在")
        
        # 使用Camelot读取PDF中的表格
        tables = camelot.read_pdf(
            pdf_path,
            flavor='stream'  # 只保留 flavor 参数
        )
        
        # 检查是否提取到表格
        if not tables:
            raise ValueError("未在PDF中检测到表格")
        
        # 保存第一个表格到Excel
        tables[0].df.to_excel(excel_path, index=False, engine='openpyxl')
        print(f"成功将表格保存到 {excel_path}")
        
        # 可选：打印表格内容以检查
        print("提取的表格内容：")
        print(tables[0].df)
        
    except Exception as e:
        print(f"表格提取或保存失败: {e}")
        return False
    return True

# 主程序
def main():
    # 确保依赖已安装
    # try:
    #     import img2pdf
    #     import camelot
    # except ImportError:
    #     print("请安装依赖：pip install img2pdf camelot-py[cv] openpyxl")
    #     return
    
    # # 转换图片为PDF
    # if not image_to_pdf(image_path, pdf_path):
    #     return
    
    # 提取表格并保存为Excel
    print('BASE_DIR是：', pdf_path)

    extract_table_to_excel(pdf_path, excel_path)

if __name__ == "__main__":
    main()