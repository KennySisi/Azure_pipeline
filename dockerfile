# FROM python:3.9
FROM tiangolo/uvicorn-gunicorn:python3.9


# 设置工作目录
WORKDIR /app

# 复制你的 Python 安装包到工作目录
COPY dist/azure_pipeline-1.1.zip .

RUN unzip azure_pipeline-1.1.zip && \
    rm azure_pipeline-1.1.zip

# Bash shell
SHELL ["/bin/bash", "-c"]

# set a virtualenv to run pip install
RUN pip install --upgrade pip \
    && pip install --upgrade virtualenv \
    && cd /app/azure_pipeline-1.1 \
    && virtualenv venv1 \
    && source venv1/bin/activate \
    && pip install -r requirements.txt

# # chmode
# RUN sudo chmod 777 ./azure_pipeline-1.1/azure_pipeline/scripts/run_script.sh

# # run server scripts
# RUN sudo ./azure_pipeline-1.1/azure_pipeline/scripts/run_script.sh

EXPOSE 80

ENV PATH="/app/azure_pipeline-1.1/venv1/bin:$PATH"

CMD ["uvicorn", "azure_pipeline-1.1.azure_pipeline.main:app", "--host", "0.0.0.0", "--port", "80"]
