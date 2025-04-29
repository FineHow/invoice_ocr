import openpyxl
from pathlib import Path

def save_excel(data, output_file):
    """将识别的文本保存到 Excel 文件"""
    wb = openpyxl.Workbook()
    ws = wb.active

    # 创建表头
    ws.append([
        "文件名", "总页数",
        "发票编号", "开票日期",
        "购买方", "购买方税号",
        "总价", "税率", "税额"
    ])

    # 循环写入数据
    for entry in data:
        file_name = entry.get("file", "Unknown")
        page_number = entry.get("page", "Unknown")
        text_data = entry.get("text", {})

        # 从 text 字段获取详细信息，提供默认值避免 KeyError
        invoice_number = text_data.get("invoice_number", "Unknown")
        invoice_date = text_data.get("invoice_date", "Unknown")
        buyer_name = text_data.get("buyer_name", "Unknown")
        buyer_tax_number = text_data.get("buyer_tax_number", "Unknown")
        amount = text_data.get("amount", "Unknown")
        tax_rate = text_data.get("tax_rate", "Unknown")
        tax_amount = text_data.get("tax_amount", "Unknown")

        # 将数据写入 Excel 行
        ws.append([
            file_name, page_number,
            invoice_number, invoice_date,
            buyer_name, buyer_tax_number,
            amount, tax_rate, tax_amount
        ])

    # 确保输出目录存在
    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # 保存 Excel 文件
    wb.save(output_file)