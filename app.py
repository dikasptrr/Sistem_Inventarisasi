import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Folder data
DATA_DIR = "data"
ALAT_FILE = os.path.join(DATA_DIR, "stok_alat.csv")
BAHAN_FILE = os.path.join(DATA_DIR, "stok_bahan.csv")
RIWAYAT_FILE = os.path.join(DATA_DIR, "riwayat_penggunaan.csv")

# Load data
def load_data():
    alat_df = pd.read_csv(ALAT_FILE)
    bahan_df = pd.read_csv(BAHAN_FILE)
    riwayat_df = pd.read_csv(RIWAYAT_FILE)
    return alat_df, bahan_df, riwayat_df

# Simpan data
def save_data(df, file_path):
    df.to_csv(file_path, index=False)

st.title("📒 Logbook Inventarisasi Laboratorium Kimia")

# Menu sidebar
menu = st.sidebar.selectbox("Menu", ["Stok Alat", "Stok Bahan", "Riwayat Penggunaan", "Tambah Data"])

alat_df, bahan_df, riwayat_df = load_data()

if menu == "Stok Alat":
    st.header("📌 Stok Alat Laboratorium")
    st.dataframe(alat_df)
    with st.expander("🔍 Cari Alat"):
        search = st.text_input("Nama alat:")
        filtered = alat_df[alat_df["Nama Alat"].str.contains(search, case=False)]
        st.dataframe(filtered)

elif menu == "Stok Bahan":
    st.header("🧪 Stok Bahan Kimia")
    st.dataframe(bahan_df)
    with st.expander("🔍 Cari Bahan"):
        search = st.text_input("Nama bahan:")
        filtered = bahan_df[bahan_df["Nama Bahan"].str.contains(search, case=False)]
        st.dataframe(filtered)

elif menu == "Riwayat Penggunaan":
    st.header("📝 Riwayat Penggunaan Alat dan Bahan")
    st.dataframe(riwayat_df)

elif menu == "Tambah Data":
    st.header("➕ Tambah Data Inventaris")

    kategori = st.selectbox("Kategori", ["Alat", "Bahan", "Riwayat Penggunaan"])

    if kategori == "Alat":
        nama = st.text_input("Nama Alat")
        jumlah = st.number_input("Jumlah", min_value=1)
        lokasi = st.text_input("Tempat Penyimpanan")
        if st.button("Simpan"):
            new_row = {"Nama Alat": nama, "Jumlah": jumlah, "Tempat Penyimpanan": lokasi}
            alat_df = pd.concat([alat_df, pd.DataFrame([new_row])], ignore_index=True)
            save_data(alat_df, ALAT_FILE)
            st.success("Alat berhasil ditambahkan!")

    elif kategori == "Bahan":
        nama = st.text_input("Nama Bahan")
        jumlah = st.text_input("Jumlah (mis. 500 ml / 1 kg)")
        expired = st.date_input("Tanggal Kedaluwarsa")
        lokasi = st.text_input("Tempat Penyimpanan")
        if st.button("Simpan"):
            new_row = {"Nama Bahan": nama, "Jumlah": jumlah, "Tanggal Expired": expired, "Tempat Penyimpanan": lokasi}
            bahan_df = pd.concat([bahan_df, pd.DataFrame([new_row])], ignore_index=True)
            save_data(bahan_df, BAHAN_FILE)
            st.success("Bahan berhasil ditambahkan!")

    elif kategori == "Riwayat Penggunaan":
        nama = st.text_input("Nama Alat/Bahan")
        kategori_penggunaan = st.selectbox("Kategori", ["Alat", "Bahan"])
        jumlah = st.text_input("Jumlah Digunakan")
        tanggal = st.date_input("Tanggal Penggunaan", value=datetime.today())
        digunakan_oleh = st.text_input("Digunakan Oleh")
        keperluan = st.text_area("Keperluan")
        if st.button("Simpan"):
            new_row = {
                "Nama": nama,
                "Kategori": kategori_penggunaan,
                "Jumlah Digunakan": jumlah,
                "Tanggal": tanggal,
                "Digunakan Oleh": digunakan_oleh,
                "Keperluan": keperluan
            }
            riwayat_df = pd.concat([riwayat_df, pd.DataFrame([new_row])], ignore_index=True)
            save_data(riwayat_df, RIWAYAT_FILE)
            st.success("Riwayat penggunaan berhasil ditambahkan!")
