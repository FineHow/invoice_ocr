import zipfile
from pathlib import Path

def handle_zip_uploaded(zip_path: Path, output_dir: Path):
    """
    解压 ZIP 文件到指定目录，并返回解压后的文件路径。
    
    Args:
        zip_path (Path): ZIP 文件的路径
        output_dir (Path): 输出目录路径
        
    Returns:
        List[Path]: 解压后的文件路径列表
    """
    if not zip_path.suffix == '.zip':
        raise ValueError("上传的文件不是一个 ZIP 文件！")
    
    # 确保输出目录存在
    output_dir.mkdir(parents=True, exist_ok=True)

    # 解压 ZIP 文件
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(output_dir)  # 将文件解压到输出目录中
    except zipfile.BadZipFile:
        raise ValueError("ZIP 文件无效或已损坏！")
    
    # 获取解压后的文件列表
    extracted_files = list(output_dir.iterdir())
    
    # 删除 ZIP 文件（删除行为可选，视具体需求）
    zip_path.unlink()
    return extracted_files


def handle_rar_uploaded(rar_path: Path, output_dir: Path):
    """
    解压 rar 文件到指定目录，并返回解压后的文件路径。
    
    Args:
        rar_path (Path): ZIP 文件的路径
        output_dir (Path): 输出目录路径
        
    Returns:
        List[Path]: 解压后的文件路径列表
    """
    if not rar_path.suffix == '.zip':
        raise ValueError("上传的文件不是一个 ZIP 文件！")
    
    # 确保输出目录存在
    output_dir.mkdir(parents=True, exist_ok=True)

    # 解压 ZIP 文件
    try:
        with zipfile.ZipFile(rar_path, 'r') as zip_ref:
            zip_ref.extractall(output_dir)  # 将文件解压到输出目录中
    except zipfile.BadZipFile:
        raise ValueError("rar 文件无效或已损坏！")
    
    # 获取解压后的文件列表
    extracted_files = list(output_dir.iterdir())
    
    # 删除 ZIP 文件（删除行为可选，视具体需求）
    rar_path.unlink()
    return extracted_files