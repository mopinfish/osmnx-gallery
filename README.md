# osmnx-tools

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
