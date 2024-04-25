# 使用 AWS Lambda 官方 Python 3.8 镜像作为基础镜像
FROM public.ecr.aws/lambda/python:3.8

# 将 Lambda 函数代码文件拷贝到容器中的 /var/task 目录下
COPY azure_pipeline/main.py /var/task/

# 设置 Lambda 函数入口为 lambda_function.lambda_handler
CMD ["azure_pipeline.main.lambda_handler"]
