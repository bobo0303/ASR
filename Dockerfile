FROM python:3.8.10-slim

ARG DEBIAN_FRONTEND=noninteractive
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends libgl1 libglib2.0-0 vim ffmpeg zip unzip htop screen tree && apt-get clean && rm -rf /var/lib/apt/lists

RUN pip install --upgrade pip

# 將 requirements.txt 複製到 Docker 映像中  
COPY requirements.txt .  
COPY whl/wjy3-1.7.1-py3-none-any.whl whl/wjy3-1.7.1-py3-none-any.whl 
COPY whl/openai_whisper-20231117-py3-none-any.whl whl/openai_whisper-20231117-py3-none-any.whl

# python packages
RUN pip3 install -r requirements.txt && \
    pip3 install whl/wjy3-1.7.1-py3-none-any.whl && \
    pip3 install whl/openai_whisper-20231117-py3-none-any.whl

# app
WORKDIR /app

# 复制 app 资料夹到 Docker 映像中的 /app 目录  
COPY . /app  

# 设置环境变量  
ENV LC_ALL=C.UTF-8  
ENV LANG=C.UTF-8  
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility  
ENV NVIDIA_VISIBLE_DEVICES=all  
ENV LD_LIBRARY_PATH=/usr/local/cuda/lib64  

