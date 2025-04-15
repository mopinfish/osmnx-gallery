# Streamlit 実行
run:
	streamlit run main.py
# フォーマット
format:
	black main.py

# Lint
lint:
	ruff check

# 型チェック
check:
	mypy main.py

# テスト実行
test:
	pytest tests/