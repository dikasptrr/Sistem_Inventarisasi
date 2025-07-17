import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- Path File ---
DATA_DIR = "data"
ALAT_FILE = os.path.join(DATA_DIR, "stok_alat.csv")
BAHAN_FILE = os.path.join(DATA_DIR, "stok_bahan.csv")
RIWAYAT_FILE = os.path.join(DATA_DIR, "riwayat_penggunaan.csv")

# --- Buat folder dan file jika belum ada ---
def load_data():
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(ALAT_FILE):
        pd.DataFrame(columns=["Nama Alat", "Jumlah", "Tempat Penyimpanan"]).to_csv(ALAT_FILE, index=False)

    if not os.path.exists(BAHAN_FILE):
        pd.DataFrame(columns=["Nama Bahan", "Jumlah", "Tanggal Expired", "Tempat Penyimpanan"]).to_csv(BAHAN_FILE, index=False)

    if not os.path.exists(RIWAYAT_FILE):
        pd.DataFrame(columns=["Nama", "Kategori", "Jumlah Digunakan", "Tanggal", "Digunakan Oleh", "Keperluan"]).to_csv(RIWAYAT_FILE, index=False)

    alat_df = pd.read_csv(ALAT_FILE)
    bahan_df = pd.read_csv(BAHAN_FILE)
    riwayat_df = pd.read_csv(RIWAYAT_FILE)
    return alat_df, bahan_df, riwayat_df

# --- Load data awal ---
alat_df, bahan_df, riwayat_df = load_data()

# --- Sidebar Menu ---
st.title("📒 Logbook Inventarisasi Laboratorium Kimia Politeknik AKA Bogor")
menu = st.sidebar.selectbox("Menu", ["Stok Alat", "Stok Bahan", "Riwayat Penggunaan", "Tambah Data"])

# --- Tampilan Stok Alat ---
if menu == "Stok Alat":
    st.header("📌 Stok Alat Laboratorium")
    st.dataframe(alat_df)
    with st.expander("🔍 Cari Alat"):
        search = st.text_input("Nama alat:")
        filtered = alat_df[alat_df["Nama Alat"].str.contains(search, case=False)]
        st.dataframe(filtered)

# --- Tampilan Stok Bahan (plus Sisa & Stok Menipis) ---
elif menu == "Stok Bahan":
    st.header("🧪 Stok Bahan Kimia")

    # Proses jumlah awal & satuan
    bahan_df_copy = bahan_df.copy()
    bahan_df_copy["Jumlah Awal"] = bahan_df_copy["Jumlah"].str.extract(r'(\d+\.?\d*)').astype(float)
    bahan_df_copy["Satuan"] = bahan_df_copy["Ju]()
