# 调用AI视觉模型的方式识别，这边用的是gemma3:4b
import requests
import base64
from dotenv import load_dotenv
import os
from backend.core.config import settings
# 加载环境变量
OLLAMA_PROXY_URL = settings.OLLAMA_PROXY_URL


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


