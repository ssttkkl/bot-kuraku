FROM python:3.10-slim as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM antonapetrov/uvicorn-gunicorn-fastapi:python3.10-slim

ENV APP_MODULE=bot:app
ENV MAX_WORKERS=1

ENV TZ=Asia/Shanghai

ENV LANG zh_CN.UTF-8
ENV LANGUAGE zh_CN.UTF-8
ENV LC_ALL zh_CN.UTF-8

RUN ln -fs /usr/share/zoneinfo/${TZ} /etc/localtime

RUN apt update && apt install git -y && pip install playwright && playwright install chromium && playwright install-deps

COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./ /app/

WORKDIR /app
