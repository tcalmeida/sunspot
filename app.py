"""Sunspot — entry point da aplicação Streamlit."""

import streamlit as st

from app.ui.main_page import render_main_page

st.set_page_config(
    page_title="Sunspot",
    page_icon="☀️",
    layout="centered",
)

render_main_page()
