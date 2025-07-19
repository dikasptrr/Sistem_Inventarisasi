import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Konfigurasi halaman
st.set_page_config(page_title="Inventarisasi Lab Kimia", layout="wide")

# Lokasi file data
DATA_DIR = "data"
STOK_BAHAN = os.path.join(DATA_DIR, "stok_bahan.csv")
STOK_ALAT = os.path.join(DATA_DIR, "stok_alat.csv")
RIWAYAT_FILE = os.path.join(DATA_DIR, "riwayat_penggunaan.csv")

# Inisialisasi folder dan file
os.makedirs(DATA_DIR, exist_ok=True)

def init_csv(filepath, columns):
    if not os.path.exists(filepath):
        pd.DataFrame(columns=columns).to_csv(filepath, index=False)

init_csv(STOK_BAHAN, ["Nama", "Jumlah", "Satuan", "Tempat Penyimpanan", "Tanggal Expired"])
init_csv(STOK_ALAT, ["Nama", "Jumlah", "Lokasi"])
init_csv(RIWAYAT_FILE, ["Nama", "Kategori", "Jumlah", "Tanggal", "Pengguna", "Keterangan"])

# Load data
def load_data():
    return (
        pd.read_csv(STOK_BAHAN),
        pd.read_csv(STOK_ALAT),
        pd.read_csv(RIWAYAT_FILE),
    )

def save_data(bahan, alat, logbook):
    bahan.to_csv(STOK_BAHAN, index=False)
    alat.to_csv(STOK_ALAT, index=False)
    logbook.to_csv(RIWAYAT_FILE, index=False)

# --- LOGIN ---
st.title("🔑 Login Pengguna")
role = st.selectbox("Masuk sebagai:", ["Mahasiswa", "Dosen", "Laboran"])
nama_pengguna = st.text_input("Nama Pengguna")

if nama_pengguna:
    st.sidebar.title(f"Selamat datang, {nama_pengguna} 👋")
    st.sidebar.write(f"Peran: **{role}**")
    bahan_df, alat_df, logbook_df = load_data()

    # === Mahasiswa dan Dosen ===
    if role in ["Mahasiswa", "Dosen"]:
        menu = st.sidebar.radio("📋 Menu", ["Stok Bahan", "Stok Alat", "Logbook - Bahan", "Logbook - Alat"])

        if menu == "Stok Bahan":
            st.header("📦 Stok Bahan Kimia")
            st.dataframe(bahan_df)

        elif menu == "Stok Alat":
            st.header("🔧 Stok Alat Laboratorium")
            st.dataframe(alat_df)

        elif menu == "Logbook - Bahan":
            st.header("🧪 Logbook Pemakaian Bahan Kimia")
            nama = st.text_input("Nama Bahan")
            jumlah = st.number_input("Jumlah", min_value=0.01, step=0.01, format="%.2f")
            satuan = st.selectbox("Satuan", ["g", "ml"])
            tanggal = st.date_input("Tanggal Pemakaian", datetime.today())
            keterangan = st.text_area("Keterangan")

            if st.button("Catat Penggunaan Bahan"):
                new_log = pd.DataFrame([[nama, "Bahan", f"{jumlah} {satuan}", tanggal, nama_pengguna, keterangan]],
                                       columns=logbook_df.columns)
                logbook_df = pd.concat([logbook_df, new_log], ignore_index=True)
                save_data(bahan_df, alat_df, logbook_df)
                st.success("✅ Penggunaan bahan berhasil dicatat.")

        elif menu == "Logbook - Alat":
            st.header("🔄 Logbook Peminjaman / Pengembalian Alat")
            nama = st.selectbox("Nama Alat", alat_df["Nama"].unique() if not alat_df.empty else [])
            aksi = st.radio("Aksi", ["Pinjam", "Kembalikan"])
            jumlah = st.number_input("Jumlah", min_value=1, step=1)
            tanggal = st.date_input("Tanggal", datetime.today())
            keterangan = st.text_area("Keterangan")

            if st.button("Catat Aksi Alat"):
                new_log = pd.DataFrame([[nama, "Alat", jumlah, tanggal, nama_pengguna, f"{aksi}: {keterangan}"]],
                                       columns=logbook_df.columns)
                logbook_df = pd.concat([logbook_df, new_log], ignore_index=True)
                save_data(bahan_df, alat_df, logbook_df)
                st.success(f"✅ Aksi '{aksi}' alat berhasil dicatat.")

    # === Laboran ===
    elif role == "Laboran":
        menu = st.sidebar.radio("📋 Menu", ["Stok Bahan", "Stok Alat", "Logbook Pemakaian"])

        if menu == "Stok Bahan":
            st.header("📦 Kelola Stok Bahan Kimia")
            st.dataframe(bahan_df)

            st.subheader("Tambah / Hapus Bahan")
            nama = st.text_input("Nama Bahan")
            jumlah = st.number_input("Jumlah", min_value=0.0)
            satuan = st.selectbox("Satuan", ["g", "ml"])
            tempat = st.text_input("Tempat Penyimpanan")
            expired = st.date_input("Tanggal Expired")

            col1, col2 = st.columns(2)
            if col1.button("➕ Tambah"):
                new = pd.DataFrame([[nama, jumlah, satuan, tempat, expired]], columns=bahan_df.columns)
                bahan_df = pd.concat([bahan_df, new], ignore_index=True)
                save_data(bahan_df, alat_df, logbook_df)
                st.success("✅ Bahan ditambahkan.")

            if col2.button("🗑️ Hapus"):
                bahan_df = bahan_df[bahan_df["Nama"] != nama]
                save_data(bahan_df, alat_df, logbook_df)
                st.success("✅ Bahan dihapus.")

        elif menu == "Stok Alat":
            st.header("🔧 Kelola Stok Alat Laboratorium")
            st.dataframe(alat_df)

            st.subheader("Tambah / Hapus Alat")
            nama = st.text_input("Nama Alat")
            jumlah = st.number_input("Jumlah", min_value=0, step=1)
            lokasi = st.text_input("Lokasi")

            col1, col2 = st.columns(2)
            if col1.button("➕ Tambah"):
                new = pd.DataFrame([[nama, jumlah, lokasi]], columns=alat_df.columns)
                alat_df = pd.concat([alat_df, new], ignore_index=True)
                save_data(bahan_df, alat_df, logbook_df)
                st.success("✅ Alat ditambahkan.")

            if col2.button("🗑️ Hapus"):
                alat_df = alat_df[alat_df["Nama"] != nama]
                save_data(bahan_df, alat_df, logbook_df)
                st.success("✅ Alat dihapus.")

        elif menu == "Logbook Pemakaian":
            st.header("📘 Riwayat Logbook Pemakaian")
            if logbook_df.empty:
                st.info("Belum ada catatan logbook.")
            else:
                df = logbook_df.copy()
                df.index += 1
                st.dataframe(df)

else:
    st.warning("Masukkan nama pengguna untuk memulai.")
