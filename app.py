import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- Styling background ---
def set_background():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://images.unsplash.com/photo-1581090700227-1e8e8f2340e5");
            background-size: cover;
            background-attachment: fixed;
            background-repeat: no-repeat;
            color: white;
        }}
        .block-container {{
            background-color: rgba(0, 0, 0, 0.6);
            padding: 2rem;
            border-radius: 1rem;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_background()

# --- Judul ---
st.title("📘 Sistem Inventarisasi Lab Kimia")
st.markdown("Logbook digital untuk alat & bahan kimia")

# --- Folder data ---
DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# --- Load data ---
@st.cache_data
def load_data(file_name):
    path = os.path.join(DATA_DIR, file_name)
    if os.path.exists(path):
        return pd.read_csv(path)
    else:
        return pd.DataFrame()

# --- Simpan data ---
def save_data(df, file_name):
    path = os.path.join(DATA_DIR, file_name)
    df.to_csv(path, index=False)

# --- Tab navigasi ---
tab = st.sidebar.radio("Menu", ["Stok", "Input Data", "Riwayat"])

if tab == "Stok":
    st.subheader("📦 Stok Alat dan Bahan")
    bahan_df = load_data("bahan.csv")
    alat_df = load_data("alat.csv")
    
    st.write("### Bahan Kimia")
    st.dataframe(bahan_df if not bahan_df.empty else "Belum ada data.")

    st.write("### Alat Laboratorium")
    st.dataframe(alat_df if not alat_df.empty else "Belum ada data.")

elif tab == "Input Data":
    st.subheader("✍️ Input Data Baru")

    kategori = st.selectbox("Pilih Kategori", ["Bahan", "Alat"])
    nama = st.text_input("Nama Item")
    jumlah = st.number_input("Jumlah", min_value=0)
    satuan = st.text_input("Satuan")
    expired = st.date_input("Tanggal Expired (bila bahan kimia)", disabled=(kategori == "Alat"))

    if st.button("Simpan"):
        new_data = {
            "Nama": nama,
            "Jumlah": jumlah,
            "Satuan": satuan,
            "Tanggal Expired": expired if kategori == "Bahan" else "-"
        }
        file_name = "bahan.csv" if kategori == "Bahan" else "alat.csv"
        df = load_data(file_name)
        df = df.append(new_data, ignore_index=True)
        save_data(df, file_name)
        st.success(f"{kategori} berhasil ditambahkan!")

elif tab == "Riwayat":
    st.subheader("📖 Riwayat Penggunaan")

    file_name = st.selectbox("Pilih File", ["bahan.csv", "alat.csv"])
    df = load_data(file_name)
    if df.empty:
        st.info("Belum ada data.")
    else:
        st.dataframe(df)
