
import streamlit as st

def dashboard_page():
    st.title("📊 Dashboard LogNStock")
    st.write(f"Selamat datang, {st.session_state.user} 👋")
