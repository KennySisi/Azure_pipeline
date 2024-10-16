# FROM python:3.9
FROM tiangolo/uvicorn-gunicorn:python3.9


# 设置工作目录
WORKDIR /app

COPY . . 

# 安装Python依赖
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 生成Python包的ZIP文件
RUN python setup.py sdist --formats=zip

# 复制生成的ZIP文件到适当的位置
RUN mv dist/azure_pipeline-1.zip .

RUN unzip azure_pipeline-1.zip && \
    rm azure_pipeline-1.zip

# Bash shell
SHELL ["/bin/bash", "-c"]

# set a virtualenv to run pip install

    # $$ add-apt-repository 'deb [arch=amd64] https://packages.microsoft.com/ubuntu/18.04/prod bionic main' \
    # && sudo su \

# RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
#     curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
#     && apt-get update \
#     && apt-get install -y unixodbc-dev \
#     && apt-get install -y msodbcsql17 

RUN pip install --upgrade pip \
    && pip install --upgrade virtualenv \
    && cd /app/azure_pipeline-1 \
    && virtualenv venv1 \
    && source venv1/bin/activate \
    && pip install -r requirements.txt

# # chmode
# RUN sudo chmod 777 ./azure_pipeline-1/azure_pipeline/scripts/run_script.sh

# # run server scripts
# RUN sudo ./azure_pipeline-1/azure_pipeline/scripts/run_script.sh

EXPOSE 80

ENV PATH="/app/azure_pipeline-1/venv1/bin:$PATH"

CMD ["uvicorn", "azure_pipeline-1.azure_pipeline.main:app", "--host", "0.0.0.0", "--port", "80"]
