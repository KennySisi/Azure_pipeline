#!/bin/bash
echo 'Script execution start'
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
# 显示 Docker 版本
sudo docker --version
# 安装 Python 3
sudo apt-get install -y python3
# 安装 Python 3 pip
sudo apt-get install -y python3-pip
# 安装 FastAPI 和 Uvicorn
pip3 install fastapi uvicorn
# 运行 FastAPI Docker 容器
sudo docker run -p 8000:8000 -d mly219blueheart/fastapi:latest
echo 'Script execution end'