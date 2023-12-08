# 使用官方 Python 镜像作为基础镜像
FROM python:3.9

# 设置工作目录
WORKDIR /app

# 复制你的 Python 安装包到工作目录
COPY dist/azure_pipeline-1.zip .

# 解压你的安装包
RUN unzip azure_pipeline-1.zip

# 安装依赖
RUN pip install -r azure_pipeline-1/requirements.txt

# chmode
RUN sudo chmod 777 ./azure_pipeline-1/azure_pipeline/scripts/run_script.sh

# run server scripts
RUN sudo ./azure_pipeline-1/azure_pipeline/scripts/run_script.sh


# 暴露应用程序的端口（如果有需要）
EXPOSE 8000

# 设置启动命令
CMD ["uvicorn", "azure_pipeline-1.azure_pipeline.main:app", "--host", "0.0.0.0"]
