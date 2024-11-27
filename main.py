
from streamlit_app import streamlit_app
from chains import Chain
from portfolio import Portfolio
from utils import clean_text
from streamlit_app import streamlit_app
import streamlit as st
import os 

port = int(os.environ.get("PORT", 8501))

if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    streamlit_app.create_streamlit_app(chain, portfolio, clean_text)

