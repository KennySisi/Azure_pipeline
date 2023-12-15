#!/bin/bash

# 下载 Docker 安装脚本
curl -fsSL https://get.docker.com -o get-docker.sh

# 运行安装脚本
sudo sh get-docker.sh

# Run FastAPI Docker container
if [$# -eq 1]; then
    sudo docker run -p 8000:8000 -d $1

