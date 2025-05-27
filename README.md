# osmnx-gallery

This is a Streamlit-based web application built upon the [OSMnx Examples](https://github.com/gboeing/osmnx-examples) repository, which demonstrates features of the OSMnx Python library.

## 📌 Features

- Download and analyze street networks from OpenStreetMap
- Visualize routing, elevation, POIs, building footprints, and more
- Interactive UI powered by Streamlit

## 📂 Structure

- `pages/`: Streamlit multipage modules converted from Jupyter notebooks
- `LICENSE`: MIT License referencing original OSMnx Examples authorship

## 📄 License and Attribution

This application uses code and examples adapted from the OSMnx Examples repository developed by Geoff Boeing.

> Copyright (c) 2016–2025 Geoff Boeing  
> [https://geoffboeing.com](https://geoffboeing.com)

Licensed under the [MIT License](./LICENSE).

OpenStreetMap data © [OpenStreetMap contributors](https://www.openstreetmap.org/copyright).

本アプリは Geoff Boeing 氏が開発した OSMnx およびその公式チュートリアルリポジトリ [OSMnx Examples](https://github.com/gboeing/osmnx-examples) をもとに作成されています。

このアプリの一部コードおよび資料は MITライセンス に基づいて使用・改変されています。以下の著作権表示およびライセンス条項をすべての複製物に含めています。

Copyright (c) 2016–2025 Geoff Boeing  
https://geoffboeing.com/

本ソフトウェアは「現状のまま」提供されており、商品性や特定目的への適合性を含む明示または黙示のいかなる保証もありません。

## setup

```bash
# setup project
mkdir osmnx-tools
cd sosmnx-tools
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install uv

# install dependencies
uv pip install -r requirements.txt -r requirements-dev.txt
```

## commands

```bash
# 仮想環境を有効化
source .venv/bin/activate

# Streamlit 実行
streamlit run main.py

# フォーマット
black main.py

# Lint
ruff .

# 型チェック
mypy main.py

# テスト実行
pytest tests/

# dockerコンテナ内で実行
docker compose up -d
```
