import requests
import openpyxl
import json

from PIL import Image
import numpy as np
import re
import base64
import os

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