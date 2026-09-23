import streamlit as st
from src.config import load_config
from src.pipeline import run_app_pipeline

def main():
    config = load_config()
    st.set_page_config(page_title=config["app"]["title"], layout="wide")
    st.title(config["app"]["title"])
    st.caption("Scientific single-line image profiler for rainbow analysis.")
    run_app_pipeline(config)

if __name__ == "__main__":
    main()