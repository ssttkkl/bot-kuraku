FROM python:3.11-slim

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

# install PDM
ENV PDM_CHECK_UPDATE=false
RUN pip install -U pdm

# set command/entrypoint, adapt to fit your needs
WORKDIR /project

COPY ./ /project/
RUN chmod +x start.sh
RUN pdm install --check
ENV PATH="/project/.venv/bin:$PATH"

CMD ["start.sh"]

