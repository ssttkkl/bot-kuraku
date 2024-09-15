# ========== requirements-stage ==========
# 从poetry.lock生成requirements.txt
FROM python:3.11 as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# ========== main ==========
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11-slim

ENV APP_MODULE=bot:app
ENV MAX_WORKERS=1

ENV TZ=Asia/Shanghai

ENV LANG zh_CN.UTF-8
ENV LANGUAGE zh_CN.UTF-8
ENV LC_ALL zh_CN.UTF-8

RUN ln -fs /usr/share/zoneinfo/${TZ} /etc/localtime
WORKDIR /app

# 安装必要依赖（git、gcc、bzip2、playwright、unzip、curl）
RUN apt update\
 && apt install git gcc bzip2 curl unzip -y\
 && pip install playwright\
 && playwright install chromium\
 && playwright install-deps

# 安装JDK17（mahjong-utils依赖）
RUN apt install -y wget apt-transport-https\
 && mkdir -p /etc/apt/keyrings\
 && wget -O - https://packages.adoptium.net/artifactory/api/gpg/key/public | tee /etc/apt/keyrings/adoptium.asc\
 && echo "deb [signed-by=/etc/apt/keyrings/adoptium.asc] https://packages.adoptium.net/artifactory/deb $(awk -F= '/^VERSION_CODENAME/{print$2}' /etc/os-release) main" | tee /etc/apt/sources.list.d/adoptium.list\
 && apt update\
 && apt install temurin-17-jdk -y

# 下载mahjong-utils-webapi
RUN curl -o mahjong-utils-webapi-all.jar https://github.com/ssttkkl/mahjong-utils/releases/download/v0.6.5/mahjong-utils-webapi-all.jar

# 安装whl包
COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# 下载maimaidx静态数据
RUN curl -o /tmp/static.zip https://share.yuzuchan.moe/d/aria/Update.zip?sign=PFnIZpgyB_HptU-hHIQ-S_qhuuGTNDlmEEtmaEpmJlA=:0
RUN mkdir -p /app/data/maimaidx && unzip /tmp/static.zip -d /app/data/maimaidx/static && rm /tmp/static.zip

COPY ./ /app/

