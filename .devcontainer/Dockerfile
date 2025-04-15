# ベースイメージは devcontainer feature に委ねるので不要
# ここでは uv をインストールするだけ

FROM mcr.microsoft.com/devcontainers/python:1-3.11

# uv をインストールし、正しい場所から /usr/local/bin に移動
RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
    && mv /root/.local/bin/uv /usr/local/bin/uv \
    && mv /root/.local/bin/uvx /usr/local/bin/uvx \
    && rm -rf /root/.local