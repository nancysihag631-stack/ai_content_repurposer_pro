#!/bin/zsh
ollama pull llama3.2 || true
streamlit run app.py
