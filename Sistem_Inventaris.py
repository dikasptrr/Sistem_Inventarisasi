import streamlit as st
import pandas as pd
import os

# File CSV
DATA_FILE = "inventaris_lab.csv"

# Load data
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=[
            "Nama Barang", "Jumlah", "Kategori", "Lokasi", "Kondisi",
            "Satuan", "Jumlah Awal", "Jumlah Terpakai", "Sisa"
        ])

# Simpan data
def save_data(data):
    data.to_csv(DATA_FILE, index=False)

# Hitung sisa
def hitung_sisa(row):
    try:
        return row["Jumlah Awal"] - row["Jumlah Terpakai"]
    except:
        return None

# Judul
st.title("🔬 Sistem Inventaris Laboratorium")

# Sidebar menu
menu = st.sidebar.selectbox("Menu", ["Lihat Inventaris", "Tambah Barang", "Cari Barang", "Cek Sisa Bahan Kimia"])

# Load data
data = load_data()

# Lihat Inventaris
if menu == "Lihat Inventaris":
    st.subheader("📋 Daftar Inventaris")
    st.dataframe(data)

# Tambah Barang
elif menu == "Tambah Barang":
    st.subheader("➕ Tambah Barang Baru")
    nama = st.text_input("Nama Barang")
    kategori = st.selectbox("Kategori", ["Elektronik", "Kimia", "Biologi", "Alat Tulis", "Lainnya"])
    lokasi = st.text_input("Lokasi Penyimpanan")
    kondisi = st.selectbox("Kondisi", ["Baik", "Rusak", "Perlu Perbaikan"])

    if kategori == "Kimia":
        satuan = st.text_input("Satuan (misal: mL, gram)")
        jumlah_awal = st.number_input("Jumlah Awal", min_value=0.0, step=1.0)
        jumlah_terpakai = st.number_input("Jumlah Terpakai", min_value=0.0, step=1.0)
        sisa = jumlah_awal - jumlah_terpakai
        jumlah = None  # Untuk kimia, tidak pakai jumlah biasa
    else:
        jumlah = st.number_input("Jumlah Barang", min_value=1, step=1)
        satuan = jumlah_awal = jumlah_terpakai = sisa = None

    if st.button("Simpan"):
        new_data = pd.DataFrame({
            "Nama Barang": [nama],
            "Jumlah": [jumlah],
            "Kategori": [kategori],
            "Lokasi": [lokasi],
            "Kondisi": [kondisi],
            "Satuan": [satuan],
            "Jumlah Awal": [jumlah_awal],
            "Jumlah Terpakai": [jumlah_terpakai],
            "Sisa": [sisa]
        })
        data = pd.concat([data, new_data], ignore_index=True)
        save_data(data)
        st.success(f"Barang '{nama}' berhasil ditambahkan!")

# Cari Barang
elif menu == "Cari Barang":
    st.subheader("🔍 Cari Barang")
    keyword = st.text_input("Masukkan kata kunci")

    if keyword:
        filtered = data[data.apply(lambda row: keyword.lower() in str(row).lower(), axis=1)]
        st.write(f"Hasil pencarian untuk: **{keyword}**")
        st.dataframe(filtered)
    else:
        st.info("Masukkan kata kunci untuk mencari.")

# Cek Sisa Bahan Kimia
elif menu == "Cek S
