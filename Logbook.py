import streamlit as st
from datetime import datetime
import pandas as pd
import os

def logbook_page():
    st.title("📝 Form Logbook Peminjaman")

    alat = st.text_input("Nama Alat")
    tanggal = st.date_input("Tanggal Peminjaman")
    waktu = st.time_input("Waktu Peminjaman")
    keperluan = st.text_area("Keperluan")

    if st.button("Simpan Log"):
        waktu_peminjaman = datetime.combine(tanggal, waktu)
        log_data = {
            "Pengguna": st.session_state.user,
            "Alat": alat,
            "Tanggal": waktu_peminjaman.strftime("%Y-%m-%d"),
            "Waktu": waktu_peminjaman.strftime("%H:%M"),
            "Keperluan": keperluan
        }

        log_df = pd.DataFrame([log_data])
        log_file = "data/logbook.csv"

        if os.path.exists(log_file):
            existing_df = pd.read_csv(log_file)
            log_df = pd.concat([existing_df, log_df], ignore_index=True)

        log_df.to_csv(log_file, index=False)
        st.success("Logbook berhasil disimpan!")
