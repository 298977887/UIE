# 使用官方的 Python 基础镜像
FROM python:3.10-slim

# 安装 libgomp1 依赖
RUN apt-get update && apt-get install -y libgomp1

# 设置工作目录
WORKDIR /app

# 复制 requirements.txt 并安装依赖
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 暴露端口（与你的 FastAPI 应用端口一致）
EXPOSE 8006

# 启动命令
CMD ["uvicorn", "test3:app", "--host", "0.0.0.0", "--port", "8006"]
