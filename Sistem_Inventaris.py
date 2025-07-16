import streamlit as st
import pandas as pd
import os

# File CSV untuk menyimpan data inventaris
DATA_FILE = "inventaris_lab.csv"

# Fungsi untuk memuat data
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["Nama Barang", "Jumlah", "Kategori", "Lokasi", "Kondisi"])

# Fungsi untuk menyimpan data
def save_data(data):
    data.to_csv(DATA_FILE, index=False)

# Judul aplikasi
st.title("🔬 Sistem Inventaris Laboratorium")

# Menu navigasi
menu = st.sidebar.selectbox("Menu", ["Lihat Inventaris", "Tambah Barang", "Cari Barang"])

# Load data
data = load_data()

# 1. Tampilkan semua data
if menu == "Lihat Inventaris":
    st.subheader("📋 Daftar Inventaris")
    st.dataframe(data)

# 2. Tambah data baru
elif menu == "Tambah Barang":
    st.subheader("➕ Tambah Barang Baru")
    nama = st.text_input("Nama Barang")
    jumlah = st.number_input("Jumlah", min_value=1, step=1)
    kategori = st.selectbox("Kategori", ["Elektronik", "Kimia", "Biologi", "Alat Tulis", "Lainnya"])
    lokasi = st.text_input("Lokasi Penyimpanan")
    kondisi = st.selectbox("Kondisi", ["Baik", "Rusak", "Perlu Perbaikan"])

    if st.button("Simpan"):
        new_data = pd.DataFrame({
            "Nama Barang": [nama],
            "Jumlah": [jumlah],
            "Kategori": [kategori],
            "Lokasi": [lokasi],
            "Kondisi": [kondisi]
        })
        data = pd.concat([data, new_data], ignore_index=True)
        save_data(data)
        st.success(f"Barang '{nama}' berhasil ditambahkan!")

# 3. Cari barang
elif menu == "Cari Barang":
    st.subheader("🔍 Cari Barang")
    keyword = st.text_input("Masukkan nama barang atau kategori")

    if keyword:
        filtered = data[data.apply(lambda row: keyword.lower() in str(row).lower(), axis=1)]
        st.write(f"Hasil pencarian untuk: **{keyword}**")
        st.dataframe(filtered)
    else:
        st.info("Silakan masukkan kata kunci untuk mencari.")
