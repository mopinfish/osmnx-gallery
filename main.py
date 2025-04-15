import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()
app_name = os.getenv("APP_NAME", "Default App")

st.set_page_config(page_title=app_name)
st.title(app_name)
st.write("これは DevContainer 上の uv + Streamlit 開発環境です。")
