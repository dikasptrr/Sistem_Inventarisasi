import streamlit as st

# Dummy user database
users = {
    "admin": "admin123",
    "user": "user123"
}

def login_page():
    st.sidebar.title("🔐 Login Sistem")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    
    if st.sidebar.button("Login"):
        if username in users and users[username] == password:
            st.session_state.login = True
            st.session_state.user = username
            st.success("Login berhasil! 🎉")
            st.experimental_rerun()
        else:
            st.error("Username atau password salah!")
