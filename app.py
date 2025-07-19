import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Konfigurasi halaman
st.set_page_config(page_title="Inventarisasi Lab Kimia", page_icon="🧪", layout="wide")

# Inisialisasi session state
if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False
    st.session_state.role = ""
    st.session_state.pengguna = ""

# Path file CSV
DATA_FOLDER = "data"
STOK_BAHAN = os.path.join(DATA_FOLDER, "stok_bahan.csv")
STOK_ALAT = os.path.join(DATA_FOLDER, "stok_alat.csv")
RIWAYAT_FILE = os.path.join(DATA_FOLDER, "riwayat_penggunaan.csv")

# Pastikan folder data ada
os.makedirs(DATA_FOLDER, exist_ok=True)

# Inisialisasi file jika belum ada
def initialize_file(filepath, columns):
    if not os.path.exists(filepath):
        pd.DataFrame(columns=columns).to_csv(filepath, index=False)

initialize_file(STOK_BAHAN, ["Nama", "Jumlah", "Satuan", "Tempat Penyimpanan", "Tanggal Expired"])
initialize_file(STOK_ALAT, ["Nama", "Jumlah", "Lokasi"])
initialize_file(RIWAYAT_FILE, ["Nama", "Kategori", "Jumlah", "Tanggal", "Pengguna", "Keterangan"])

# Load data
def load_data():
    bahan_df = pd.read_csv(STOK_BAHAN)
    alat_df = pd.read_csv(STOK_ALAT)
    riwayat_df = pd.read_csv(RIWAYAT_FILE)
    return bahan_df, alat_df, riwayat_df

# Simpan data
def save_data(bahan_df, alat_df, riwayat_df):
    bahan_df.to_csv(STOK_BAHAN, index=False)
    alat_df.to_csv(STOK_ALAT, index=False)
    riwayat_df.to_csv(RIWAYAT_FILE, index=False)

# Login pengguna
if not st.session_state.is_logged_in:
    st.title("🔐 Login Pengguna")
    st.session_state.pengguna = st.text_input("Nama Pengguna")
    st.session_state.role = st.selectbox("Pilih Peran", ["Mahasiswa", "Dosen", "Laboran"])
    if st.button("Login"):
        if st.session_state.pengguna:
            st.session_state.is_logged_in = True
            st.experimental_rerun()
        else:
            st.warning("Nama pengguna harus diisi terlebih dahulu.")
    st.stop()

# Load data setelah login
pengguna = st.session_state.pengguna
role = st.session_state.role
bahan_df, alat_df, riwayat_df = load_data()

# Menu berdasarkan peran
if role == "Laboran":
    menu = st.sidebar.selectbox("Menu", ["Stok Bahan Kimia", "Stok Alat Laboratorium", "Peminjaman & Pengembalian", "Riwayat Aktivitas", "Logbook Pemakaian"])

    if menu == "Stok Bahan Kimia":
        st.title("📦 Stok Bahan Kimia")
        st.dataframe(bahan_df)
        st.subheader("Tambah / Hapus Bahan")
        nama = st.text_input("Nama Bahan")
        jumlah = st.number_input("Jumlah", min_value=0.0)
        satuan = st.selectbox("Satuan", ["g", "ml"])
        tempat = st.text_input("Tempat Penyimpanan")
        expired = st.date_input("Tanggal Expired")
        if st.button("Tambah Bahan"):
            new = pd.DataFrame([[nama, jumlah, satuan, tempat, expired]], columns=bahan_df.columns)
            bahan_df = pd.concat([bahan_df, new], ignore_index=True)
            save_data(bahan_df, alat_df, riwayat_df)
            st.success("Data bahan ditambahkan!")
        if st.button("Hapus Bahan"):
            bahan_df = bahan_df[bahan_df["Nama"] != nama]
            save_data(bahan_df, alat_df, riwayat_df)
            st.success("Data bahan dihapus!")

    elif menu == "Stok Alat Laboratorium":
        st.title("🛠️ Stok Alat Laboratorium")
        st.dataframe(alat_df)
        st.subheader("Tambah / Hapus Alat")
        nama = st.text_input("Nama Alat")
        jumlah = st.number_input("Jumlah", min_value=0, step=1)
        lokasi = st.text_input("Lokasi")
        if st.button("Tambah Alat"):
            new = pd.DataFrame([[nama, jumlah, lokasi]], columns=alat_df.columns)
            alat_df = pd.concat([alat_df, new], ignore_index=True)
            save_data(bahan_df, alat_df, riwayat_df)
            st.success("Data alat ditambahkan!")
        if st.button("Hapus Alat"):
            alat_df = alat_df[alat_df["Nama"] != nama]
            save_data(bahan_df, alat_df, riwayat_df)
            st.success("Data alat dihapus!")

    elif menu == "Peminjaman & Pengembalian":
        st.title("🔄 Peminjaman & Pengembalian Alat")
        alat_dipilih = st.selectbox("Nama Alat", alat_df["Nama"].unique())
        jumlah = st.number_input("Jumlah", min_value=1, step=1)
        aksi = st.radio("Aksi", ["Pinjam", "Kembalikan"])
        keterangan = st.text_input("Keterangan")
        if st.button("Simpan Aksi"):
            index = alat_df[alat_df["Nama"] == alat_dipilih].index[0]
            if aksi == "Pinjam":
                alat_df.at[index, "Jumlah"] -= jumlah
            else:
                alat_df.at[index, "Jumlah"] += jumlah
            log = pd.DataFrame([[alat_dipilih, "Alat", jumlah, datetime.now().date(), pengguna, f"{aksi}: {keterangan}"]], columns=riwayat_df.columns)
            riwayat_df = pd.concat([riwayat_df, log], ignore_index=True)
            save_data(bahan_df, alat_df, riwayat_df)
            st.success(f"Alat berhasil {aksi.lower()}!")

    elif menu == "Riwayat Aktivitas":
        st.title("📚 Riwayat Aktivitas")
        st.dataframe(riwayat_df)

    elif menu == "Logbook Pemakaian":
        st.title("📝 Logbook Pemakaian")
        st.dataframe(riwayat_df)

elif role in ["Mahasiswa", "Dosen"]:
    menu = st.sidebar.selectbox("Menu", ["Stok Bahan Kimia", "Stok Alat Laboratorium", "Logbook Pemakaian"])

    if menu == "Stok Bahan Kimia":
        st.title("📦 Stok Bahan Kimia")
        st.dataframe(bahan_df)

    elif menu == "Stok Alat Laboratorium":
        st.title("🛠️ Stok Alat Laboratorium")
        st.dataframe(alat_df)

    elif menu == "Logbook Pemakaian":
        st.title("📝 Logbook Pemakaian")
        nama = st.text_input("Nama Barang")
        kategori = st.selectbox("Kategori", ["Bahan", "Alat"])

        if kategori == "Alat":
            jumlah = st.number_input("Jumlah (buah)", min_value=1, step=1, format="%d")
        else:
            satuan = st.selectbox("Satuan", ["g", "ml"])
            jumlah = st.number_input(f"Jumlah ({satuan})", min_value=0.01, format="%f")

        tanggal = st.date_input("Tanggal")
        keterangan = st.text_area("Keterangan")
        if st.button("Catat Penggunaan"):
            log = pd.DataFrame([[nama, kategori, jumlah, tanggal, pengguna, keterangan]], columns=riwayat_df.columns)
            riwayat_df = pd.concat([riwayat_df, log], ignore_index=True)
            save_data(bahan_df, alat_df, riwayat_df)
            st.success("Penggunaan dicatat dalam logbook!")
