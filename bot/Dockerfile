# ========== requirements-stage ==========
# 从poetry.lock生成requirements.txt
FROM python:3.11 as requirements-stage

WORKDIR /tmp

RUN pip install poetry && poetry update

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

# 安装必要依赖（git、gcc、bzip2、playwright）
RUN apt update\
 && apt install git gcc bzip2 -y\
 && pip install playwright\
 && playwright install chromium\
 && playwright install-deps

# 安装whl包
COPY --from=maimaidx-stage /tmp/maimaiDX/dist/* /tmp

COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt && pip install /tmp/*.whl

COPY ./ /app/

