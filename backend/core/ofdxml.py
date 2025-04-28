import uuid
import zipfile
import aiofiles
import fitz  # PyMuPDF，处理 PDF 文件
from pathlib import Path
from xml.etree import ElementTree as ET
from fpdf import FPDF  # 用于生成 PDF
import base64
from easyofd import OFD 


async def process_zip_file(file, output_dir):
    # 确保输出目录存在
    output_dir.mkdir(parents=True, exist_ok=True)

    # 生成唯一文件名保存 ZIP 文件
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    zip_path = output_dir / unique_filename
    
    # 异步存储上传的 ZIP 文件
    async with aiofiles.open(zip_path, mode="wb") as f:
        await f.write(await file.read())
    
    # 解压 ZIP 文件
    extracted_dir = output_dir / f"{unique_filename}_extracted"
    extracted_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as zf:
        zf.extractall(extracted_dir)
    
    # 遍历解压后的文件夹，处理所有文件
    for extracted_file in extracted_dir.iterdir():
        if extracted_file.suffix.lower() == '.pdf':
            # 如果是 PDF 文件，直接进入后续处理逻辑
            handle_pdf(extracted_file)
        elif extracted_file.suffix.lower() == '.ofd':
            # 如果是 OFD 文件，转换为 PDF
            pdf_path = convert_ofd_to_pdf(extracted_file)
            if pdf_path:
                handle_pdf(pdf_path)
        elif extracted_file.suffix.lower() == '.xml':
            # 如果是 XML 文件，解析并生成 PDF
            pdf_path = convert_xml_to_pdf(extracted_file)
            if pdf_path:
                handle_pdf(pdf_path)

async def handle_pdf(pdf_file):
    # PDF 文件的后续处理逻辑，如转换为图像
    # 以下示例是基于 PyMuPDF 的简单操作
    doc = fitz.open(pdf_file)
    for page_num in range(len(doc)):
        page = doc[page_num]
        pix = page.get_pixmap()
        output_image_path = pdf_file.with_suffix(f".page{page_num}.png")
        pix.save(output_image_path)
    doc.close()

def convert_ofd_to_pdf(ofd_file):
    """
    使用 easyofd 将 OFD 转换为 PDF。
    """
    try:
        file_prefix = ofd_file.stem  # 文件名前缀
        pdf_path = ofd_file.with_suffix(".pdf")  # 定义输出 PDF 的路径
        
        # 读取 OFD 文件并编码为 Base64
        with open(ofd_file, "rb") as f:
            ofdb64 = str(base64.b64encode(f.read()), "utf-8")
        
        # 初始化 OFD 工具类，并转换为 PDF
        ofd = OFD()
        ofd.read(ofdb64, save_xml=False)  # 忽略生成 XML
        pdf_bytes = ofd.to_pdf()  # 将 OFD 转为 PDF 二进制数据
        ofd.del_data()  # 清理临时数据
        
        # 保存 PDF 文件到指定路径
        with open(pdf_path, "wb") as f:
            f.write(pdf_bytes)
        
        return pdf_path
    except Exception as e:
        print(f"Failed to convert OFD to PDF: {e}")
        return None

def convert_xml_to_pdf(xml_file):
    """
    将 XML 文件转换为 PDF。
    假设 XML 文件表示了一些结构化数据，这里我们简单将其格式化为 PDF 文档。
    """
    try:
        pdf_path = xml_file.with_suffix(".pdf")
        tree = ET.parse(xml_file)
        root = tree.getroot()

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # 遍历 XML 节点，写入 PDF
        def write_node(node, level=0):
            pdf.cell(200, 10, txt=f"{'  ' * level}{node.tag}: {node.text}", ln=True)
            for child in node:
                write_node(child, level + 1)
        
        write_node(root)
        pdf.output(str(pdf_path))
        return pdf_path
    except Exception as e:
        print(f"Failed to convert XML to PDF: {e}")
        return None