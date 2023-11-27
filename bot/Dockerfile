# ========== requirements-stage ==========
# 从poetry.lock生成requirements.txt
FROM python:3.11 as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# ========== maimaidx-stage ==========
# 将maimaiDX与资源文件打成一个whl包
FROM python:3.11 AS maimaidx-stage

RUN apt update && apt install wget unzip git && pip install pdm

WORKDIR /tmp

RUN wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2

WORKDIR /tmp/maimaiDX

RUN echo '[project]\n\
name = "maimaiDX"\n\
version = "0.1.0"\n\
description = ""\n\
authors = [\n\
   {name = "ssttkkl", email = "huang.wen.long@hotmail.com"},\n\
]\n\
dependencies = [\n\
   "nonebot2>=2.0.0",\n\
   "pillow>=9.5.0",\n\
   "aiofiles>=23.1.0",\n\
   "aiohttp>=3.8.4",\n\
   "pyecharts>=2.0.3",\n\
   "snapshot-phantomjs>=0.0.3",\n\
   "pydantic>=1.10.9",\n\
]\n\
requires-python = ">=3.8,<4.0"\n\
license = {text = "MIT"}\n\
\n\
[build-system]\n\
requires = ["pdm-backend"]\n\
build-backend = "pdm.backend"\n\
' >> ./pyproject.toml

RUN git clone https://github.com/Yuri-YuzuChaN/maimaiDX -b nonebot2

RUN wget https://vote.yuzuai.xyz/download/static.zip && unzip -d ./maimaiDX static.zip

RUN pdm build

# ========== main ==========
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11-slim

ENV APP_MODULE=bot:app
ENV MAX_WORKERS=1

ENV TZ=Asia/Shanghai

ENV LANG zh_CN.UTF-8
ENV LANGUAGE zh_CN.UTF-8
ENV LC_ALL zh_CN.UTF-8

RUN ln -fs /usr/share/zoneinfo/${TZ} /etc/localtime

# 安装必要依赖（git、gcc、bzip2、playwright）
RUN apt update && apt install git gcc bzip2 -y && pip install playwright && playwright install chromium && playwright install-deps

# 安装phantomjs（maimaiDX依赖）
COPY --from=maimaidx-stage /tmp/phantomjs-2.1.1-linux-x86_64.tar.bz2 /tmp

RUN tar -C /usr/local -xvf /tmp/phantomjs-2.1.1-linux-x86_64.tar.bz2 && mv /usr/local/phantomjs-2.1.1-linux-x86_64 phantomjs && ln -s /usr/local/phantomjs/bin/phantomjs /usr/bin/phantomjs

# 安装whl包
COPY --from=maimaidx-stage /tmp/maimaiDX/dist/* /tmp

COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt && pip install /tmp/*.whl

COPY ./ /app/

WORKDIR /app
