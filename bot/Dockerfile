ARG PYTHON_BASE=3.11-slim

# ========== build-stage ==========
FROM python:$PYTHON_BASE AS builder

# install PDM
RUN pip install -U pdm
# disable update check
ENV PDM_CHECK_UPDATE=false
# copy files
COPY pyproject.toml pdm.lock README.md /project/

# install dependencies and project into the local packages directory
WORKDIR /project
RUN pdm install --check --prod --no-editable

# ========== main ==========
FROM python:$PYTHON_BASE

ENV TZ=Asia/Shanghai

ENV LANG zh_CN.UTF-8
ENV LANGUAGE zh_CN.UTF-8
ENV LC_ALL zh_CN.UTF-8

RUN ln -fs /usr/share/zoneinfo/${TZ} /etc/localtime

# 安装必要依赖（git、gcc、bzip2、playwright、unzip、curl）
RUN apt update\
 && apt install git gcc bzip2 curl unzip p7zip-full nano -y\
 && pip install playwright\
 && playwright install chromium\
 && playwright install-deps

#  # 下载maimaidx静态数据
# RUN curl -o /tmp/static.7z "https://share.yuzuchan.moe/p/Resource.7z?sign=EvCwaGwJrneyD1Olq00NG3HXNK7fQKpx_sa3Ck9Uzjs=:0"\
#  && 7z x /tmp/static.7z -mcp=65001 -o/app/data/maimaidx\
#  && rm /tmp/static.zip

# retrieve packages from build stage
COPY --from=builder /project/.venv/ /project/.venv
ENV PATH="/project/.venv/bin:$PATH"
# set command/entrypoint, adapt to fit your needs
COPY ./ /project/

WORKDIR /project
RUN chmod +x start.sh
CMD ["start.sh"]

