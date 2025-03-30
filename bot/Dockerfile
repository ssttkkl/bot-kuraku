# ========== requirements-stage ==========
# 从poetry.lock生成requirements.txt
FROM python:3.11 as requirements-stage

WORKDIR /tmp

RUN pip install poetry==1.8.5

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
 && apt install git gcc bzip2 curl unzip p7zip-full -y\
 && pip install playwright\
 && playwright install chromium\
 && playwright install-deps

# 安装whl包
COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

 # 下载maimaidx静态数据
RUN curl -o /tmp/static.7z "https://share.yuzuchan.moe/p/Resource.7z?sign=EvCwaGwJrneyD1Olq00NG3HXNK7fQKpx_sa3Ck9Uzjs=:0"\
 && 7z x /tmp/static.7z -o/app/data/maimaidx\
 && rm /tmp/static.zip

COPY ./ /app/

