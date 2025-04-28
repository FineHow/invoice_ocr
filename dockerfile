# 使用官方 Python 基础镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 复制项目的依赖文件
COPY backend/requirements.txt /app/requirements.txt

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目代码到容器
COPY backend/ /app/backend/
COPY frontend/ /app/frontend/

# 暴露应用运行的端口（假设后端运行在 8000 端口）
EXPOSE 8000

# 安装 python-dotenv（如果需要）
RUN pip install python-dotenv

# 设置环境变量（从 .env 文件中加载）
ENV APP_PORT=${APP_PORT}
ENV APP_HOST=${APP_HOST}
ENV UMIOCR_API_BASE_URL=${UMIOCR_API_BASE_URL}

# 启动命令，使用环境变量
CMD ["python", "backend/main.py"]