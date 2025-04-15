# パッケージインストール
install:
	uv pip install --system -r requirements.txt -r requirements-dev.txt
# Streamlit 実行
run:
	streamlit run main.py
# フォーマット
format:
	black .

# Lint
lint:
	ruff check .

# 型チェック
check:
	mypy .

# テスト実行
test:
	pytest tests/