import requests
import openpyxl
import json
import re
import base64
from backend.core.config import settings
# 加载环境变量
UMIOCR_API_BASE_URL = settings.UMIOCR_API_BASE_URL
OCR_API_BASE_URL= settings.OCR_API_BASE_URL

# OCR 和 Ollama 的 API 地址配置


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
    

def umi_ocr(image_path):
    """调用 umi-OCR API 识别图像"""
    try:
         with open(image_path, "rb") as image_file:
            image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

            url=UMIOCR_API_BASE_URL + "/api/ocr"
            print(url)
            data = {
                "base64": image_base64,
                # 可选参数示例
                "options": {
                    "data.format": "text",
                     "tbpu.ignoreArea": [[[0,0],[2000,938]],[[0,1300],[4000,3000]]]    
                    ,
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
    


    
def umi_invoice_data(ocr_text):
    """
    从 OCR 文本中提取发票的结构化数据
    """
    extracted_data = {}

    try:
        # 提取发票号码
        invoice_number_match = re.search(r"发票号码[:：\s]*(\d+)", ocr_text)
        extracted_data["invoice_number"] = invoice_number_match.group(1) if invoice_number_match else None

        # 提取开票日期
        invoice_date_match = re.search(r"开票日期[:：\s]*(\d{4}年\d{2}月\d{2}日|\d{4}-\d{2}-\d{2})", ocr_text)
        extracted_data["invoice_date"] = invoice_date_match.group(1) if invoice_date_match else None

        # 提取名称（购买方信息）
        buyer_name_match = re.search(r"名称[:：\s]*(.+?)\n", ocr_text)
        extracted_data["buyer_name"] = buyer_name_match.group(1).strip() if buyer_name_match else None

        # 提取统一社会信用代码／纳税人识别号
        buyer_tax_match = re.search(r"统一社会信用代码／纳税人识别号[:：\s]*(\S+)", ocr_text)
        extracted_data["buyer_tax_number"] = buyer_tax_match.group(1) if buyer_tax_match else None

        # 提取金额
        amount_match = re.search(r"金额[:：\s]*(\d+\.\d+)", ocr_text)
        extracted_data["amount"] = amount_match.group(1) if amount_match else None

        # 提取税率/征收率
        tax_rate_match = re.search(r"税率/征收率[:：\s]*(\d+%?)", ocr_text)
        extracted_data["tax_rate"] = tax_rate_match.group(1) if tax_rate_match else None

        # 提取税额
        tax_amount_match = re.search(r"税额[:：\s]*(\d+\.\d+)", ocr_text)
        extracted_data["tax_amount"] = tax_amount_match.group(1) if tax_amount_match else None

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


def extract_invoice_data_with_gemma(image_path):
    try:
        # 读取并编码图片为 Base64
        with open(image_path, "rb") as image_file:
            image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

        # 构造 JSON 请求
        payload = {
            "model": "gemma3:4b",
            "prompt": (
                "我上传了一张图片，图片是一张发票。请分析图片内容并提取发票相关信息，以 JSON 格式输出："
                "格式要求："
                "{"
                "  \"invoice_number\": \"<发票号码>\","
                "  \"invoice_date\": \"<开票日期>\","
                "  \"total_amount\": \"<总金额>\","
                "  \"seller\": \"<卖方名称>\","
                "  \"buyer\": \"<买方名称>\""
                "}"
                "如果某些字段无法提取，请用 null 表示，但必须返回 JSON。"
                "请严格按照json格式输出，不要在{}以外增加任何内容。"
            ),
            "stream": False  ,# 非流式请求
            "images": [image_base64]
        }

        # POST 请求
        response = requests.post(f"http://192.168.11.170:11434/api/generate", json=payload)
        
        # 处理响应
        if response.status_code == 200:
            print("Gemma3:4b 模型解析成功:", response.json())
             # 返回JSON中的消息内容
            response_data = response.json()
            final_response = response_data.get('response', '')  # 根据服务器返回的 JSON 直接取 response
            print("提取的 response:", final_response)
            return final_response
        else:
            print("Gemma3:4b 模型解析失败:", response.status_code, response.text)
            return f"Error: {response.status_code} {response.text}"
    except Exception as e:
        print("调用 Gemma3:4b 模型时发生错误:", e)
        return str(e)
    
def test_gemma_chat(str):
    try:
        # 构建简单的对话请求
        payload = {
            "model": "gemma3:4b",
            "prompt": "{str}",
            "stream": False  # 非流式请求
        }
        
        # 发送 POST 请求到服务端，明确非流式请求
        response = requests.post("http://192.168.11.170:11434/api/generate", json=payload)
        
        # 检查响应状态码
        if response.status_code == 200:
            try:
                # 解析 JSON 响应数据
                response_data = response.json()
                print("Gemma3:4b 模型响应成功:", response_data)
                
                # 返回JSON中的消息内容
                final_response = response_data.get('response', '')  # 根据服务器返回的 JSON 直接取 response
                print("提取的 response:", final_response)
                return final_response
            except ValueError:
                # 若响应不可解析为 JSON 格式
                print("Gemma3:4b 模型响应非 JSON 格式:", response.text)
                return "Error: Response is not in JSON format"
        else:
            # 响应状态码非 200
            print("Gemma3:4b 模型响应失败:", response.status_code, response.text)
            return f"Error: {response.status_code} {response.text}"

    except Exception as e:
        # 捕获其他调用错误
        print("调用 Gemma3:4b 模型时发生错误:", e)
        return str(e)

def process_invoice(image_path):
    """
    综合处理图片，直接调用 Gemma3:4b 进行发票信息识别并格式化返回。
    """
    invoice_data = extract_invoice_data_with_gemma(image_path)
    if not invoice_data or "Error" in invoice_data:
        return {"error": f"Gemma3:4b 提取失败: {invoice_data}"}

    return invoice_data


def extract_invoice_data(ocr_text):
    """
    从 OCR 文本中提取发票的结构化数据
    """
    extracted_data = {}

    try:
        # 提取发票号
        invoice_number_match = re.search(r"号码[:：\s]*(\d+)", ocr_text)
        extracted_data["invoice_number"] = invoice_number_match.group(1) if invoice_number_match else None

        # 提取开票日期
        invoice_date_match = re.search(r"日期[:：\s]*(\d{4}年\d{2}月\d{2}日|\d{4}-\d{2}-\d{2})", ocr_text)
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

