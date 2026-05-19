"""Sunspot — entry point da aplicação Streamlit."""

import logging

import streamlit as st

logger = logging.getLogger(__name__)


def main() -> None:
    """Renderiza o layout inicial da aplicação."""
    st.title("☀️ Sunspot")
    st.subheader("Descubra o sol do seu próximo lar")


if __name__ == "__main__":
    main()
