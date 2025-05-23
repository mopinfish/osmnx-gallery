# ベースイメージは devcontainer feature に委ねるので不要
# ここでは uv をインストールするだけ

FROM mcr.microsoft.com/devcontainers/python:1-3.11

ENV GDAL_VERSION=3.6.0

RUN \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    gdal-bin \
    libgdal-dev \
    python3-gdal && \
    rm -rf /var/lib/apt/lists/*

# uv をインストールし、正しい場所から /usr/local/bin に移動
RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
    && mv /root/.local/bin/uv /usr/local/bin/uv \
    && mv /root/.local/bin/uvx /usr/local/bin/uvx \
    && rm -rf /root/.local