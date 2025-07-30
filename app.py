import streamlit as st
from login import login_page
from dashboard import dashboard_page
from logbook import logbook_page

# -------------------- Inisialisasi Session --------------------
if 'login' not in st.session_state:
    st.session_state.login = False
if 'user' not in st.session_state:
    st.session_state.user = ''

# -------------------- Routing Aplikasi --------------------
def main():
    if not st.session_state.login:
        login_page()
    else:
        st.sidebar.title("📋 Menu Utama")
        menu = st.sidebar.selectbox("Pilih Menu", ["Dashboard", "Isi Logbook", "Logout"])

        if menu == "Dashboard":
            dashboard_page()
        elif menu == "Isi Logbook":
            logbook_page()
        elif menu == "Logout":
            st.session_state.login = False
            st.experimental_rerun()

if __name__ == "__main__":
    main()
