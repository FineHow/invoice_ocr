import requests
import openpyxl

from PIL import Image
import numpy as np
import re


OCR_API_BASE_URL = "http://192.168.11.170:5430"

def perform_ocr(image_path, language="chi_sim"):
    """调用 OCR API 识别图像"""
    try:
        with open(image_path, "rb") as file:
            files = {'file': file}
            data = {'language': language}
            response = requests.post(f"{OCR_API_BASE_URL}/ocr", files=files, data=data)
            if response.status_code == 200:
                print("OCR 识别成功:", response.json())
                return response.json().get('data', "")
            else:
                print("OCR 识别失败:", response.status_code, response.text)
                return f"Error: {response.status_code} {response.text}"
    except Exception as e:
        print("OCR 识别时发生错误:", e)
        return str(e)
        

def save_excel(data, output_file):
    """将识别的文本保存到 Excel 文件"""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["File Name", "Page Number", "Extracted Text"])

    for entry in data:
        ws.append([
            entry["file"],
            entry["page"],
            entry["text"]
        ])

    wb.save(output_file)



def extract_invoice_data(ocr_text):
    """
    从 OCR 文本中提取发票的结构化数据
    """
    extracted_data = {}

    try:
        # 提取发票号
        invoice_number_match = re.search(r"发票号码[:：\s]*(\d+)", ocr_text)
        extracted_data["invoice_number"] = invoice_number_match.group(1) if invoice_number_match else None

        # 提取开票日期
        invoice_date_match = re.search(r"开票日期[:：\s]*(\d{4}年\d{2}月\d{2}日|\d{4}-\d{2}-\d{2})", ocr_text)
        extracted_data["invoice_date"] = invoice_date_match.group(1) if invoice_date_match else None

        # 提取购买方信息
        buyer_name_match = re.search(r"购买方信息.*?名称[:：\s]*(.+?)\n", ocr_text, re.DOTALL)
        extracted_data["buyer_name"] = buyer_name_match.group(1).strip() if buyer_name_match else None

        buyer_tax_match = re.search(r"统一社会信用代码/纳税人识别号[:：\s]*(\w+)", ocr_text)
        extracted_data["buyer_tax_number"] = buyer_tax_match.group(1) if buyer_tax_match else None

        # 提取销售方信息
        seller_name_match = re.search(r"销售方信息.*?名称[:：\s]*(.+?)\n", ocr_text, re.DOTALL)
        extracted_data["seller_name"] = seller_name_match.group(1).strip() if seller_name_match else None

        seller_tax_match = re.search(r"统一社会信用代码/纳税人识别号[:：\s]*(\w+)", ocr_text)
        extracted_data["seller_tax_number"] = seller_tax_match.group(1) if seller_tax_match else None

    except Exception as e:
        print(f"结构化数据提取失败: {e}")
    
    return extracted_data


from PIL import Image

def crop_image(image_path, crop_area):
    """
    裁剪图像中指定位置的区域
    :param image_path: 图像文件路径
    :param crop_area: 裁剪区域 (x1, y1, x2, y2)
    :return: crop后的PIL Image
    """
    try:
        with Image.open(image_path) as img:
            cropped_img = img.crop(crop_area)
            return cropped_img
    except Exception as e:
        print(f"裁剪图像失败: {e}")
        return None