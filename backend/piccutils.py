import requests
import openpyxl
import json

from PIL import Image
import numpy as np
import re
import base64
import os
from dotenv import load_dotenv
# 加载环境变量
load_dotenv()
# UMIOCR_API_BASE_URL = os.getenv("UMIOCR_API_BASE_URL")
UMIOCR_API_BASE_URL = "http://192.168.11.170:1224"




def main():
    # 项目目录下图片文件夹路径
    root_folder = "./picc"  # 请替换为你的文件夹路径
    output_excel = "output333.xlsx"  # 输出的 Excel 文件名

    # 最终数据存储结构
    extracted_data_list = []

    # 遍历目录
    for folder_name, subfolders, filenames in os.walk(root_folder):
        # 遍历文件夹中的所有文件
        for filename in filenames:
            # 检查是否是图片文件（根据后缀名过滤）
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                image_path = os.path.join(folder_name, filename)  # 构造图片的完整路径
                print(f"Processing {image_path} ...")

                # 调用 umi_ocr 提取文字
                ocr_text = umi_ocr(image_path)

                # 使用 umi_data 提取结构化数据
                structured_data = umi_data(ocr_text)
                print(f"Extracted data: {structured_data}")

                # 将结果存入字典，附加图片的文件夹名称和文件名
                extracted_data = {
                    "folder_name": os.path.basename(folder_name),  # 文件夹名称
                    "file_name": filename,                        # 文件名
                    "time": structured_data.get("time_number"),    # 时间
                    "place": structured_data.get("local_date"),    # 地点
                    "name": structured_data.get("name"),           # 姓名
                    "dakatime": structured_data.get("time"),           # 姓名
                }
                extracted_data_list.append(extracted_data)

    # 保存结果到 Excel
    # 创建 Excel 数据
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "OCR Extracted Data"
    ws.append(["文件夹名称", "文件名", "时间", "地点", "姓名","打卡时间"])  # 写入标题行

    # 写入提取的数据
    for data in extracted_data_list:
        ws.append([data["folder_name"], data["file_name"], data["time"], data["place"], data["name"],data["dakatime"]])

    # 保存到文件
    wb.save(output_excel)
    print(f"Data successfully saved to {output_excel}")




def umi_ocr(image_path):
    """调用 umi-OCR API 识别图像"""
    try:
         with open(image_path, "rb") as image_file:
            image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

            url=UMIOCR_API_BASE_URL + "/api/ocr"
        
            data = {
                "base64": image_base64,
                # 可选参数示例
                "options": {
                    "data.format": "text",
                     "tbpu.ignoreArea": [[[0,0],[1080,700]]],  # 忽略区域示例
                     
                }
            }
            headers = {"Content-Type": "application/json"}
            data_str = json.dumps(data)   # 字典转为 JSON 字符串
            response = requests.post(url, data=data_str, headers=headers)
            response.raise_for_status()
            res_dict = json.loads(response.text)
            # print(response)
            print(res_dict)
            return  res_dict.get('data', "")
    except Exception as e:
        print("OCR 识别时发生错误:", e)
        return str(e)
    


    
def umi_data(ocr_text):
    """
    从 OCR 文本中提取结构化数据
    """
    extracted_data = {}

    try:
        # 提取时间
        time_number_match = re.search(r"间[:：\s]*(.+?)\n", ocr_text)
        extracted_data["time_number"] = time_number_match.group(1) if time_number_match else None

        time_match = re.search(r"打卡\n[:：\s]*(.+?)\n", ocr_text)
        extracted_data["time"] = time_match.group(1) if time_match else None

        # 提取地点
        # local_date_match = re.search(r"点[:：\s]*(.+?)\n", ocr_text)
        # extracted_data["local_date"] = local_date_match.group(1) if local_date_match else None


        location_match = re.search(r"点[:：\s]*(.+?)(?:\n(.+?))?\n", ocr_text)
        if location_match:
            # 合并两部分的地址
            extracted_location = location_match.group(1)
            if location_match.group(2):
                extracted_location += location_match.group(2)
                extracted_data["local_date"] = extracted_location.strip()
        else:
            extracted_location = None

        # 提取姓名
        name_match = re.search(r"名[:：\s]*(.+?)\n", ocr_text)
        extracted_data["name"] = name_match.group(1).strip() if name_match else None

       

    except Exception as e:
        print(f"结构化数据提取失败: {e}")
    
    return extracted_data

# def save_excel(data, output_file):
#     """将识别的文本保存到 Excel 文件"""
#     wb = openpyxl.Workbook()
#     ws = wb.active
#     ws.append(["File Name", "Page Number", "Extracted Text"])

#     for entry in data:
#         ws.append([
#             entry["file"],
#             entry["page"],
#             entry["text"]
#         ])

#     wb.save(output_file)




if __name__ == "__main__":
    main()
