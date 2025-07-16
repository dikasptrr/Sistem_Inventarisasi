import streamlit as st
import pandas as pd
import os

# File penyimpanan
FILE_ALAT = "alat_lab.csv"
FILE_BAHAN = "bahan_kimia.csv"

# Fungsi load data
def load_data(file, columns):
    if os.path.exists(file):
        return pd.read_csv(file)
    else:
        return pd.DataFrame(columns=columns)

# Fungsi save data
def save_data(df, file):
    df.to_csv(file, index=False)

# Judul Aplikasi
st.title("🧪 Sistem Inventaris Laboratorium")

# Menu Navigasi
menu = st.sidebar.selectbox("Menu", [
    "Lihat Inventaris",
    "Tambah Alat Lab",
    "Tambah Bahan Kimia",
    "Update Pemakaian Bahan Kimia",
    "Cari Barang"
])

# Load data
alat_data = load_data(FILE_ALAT, ["Nama Alat", "Jumlah", "Lokasi", "Kondisi"])
bahan_data = load_data(FILE_BAHAN, ["Nama Bahan", "Jumlah Awal", "
