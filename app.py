import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Path file CSV
DATA_FOLDER = "data"
STOK_BAHAN = os.path.join(DATA_FOLDER, "stok_bahan.csv")
STOK_ALAT = os.path.join(DATA_FOLDER, "stok_alat.csv")
RIWAYAT_FILE = os.path.join(DATA_FOLDER, "riwayat_penggunaan.csv")

os.makedirs(DATA_FOLDER, exist_ok=True)

def initialize_file(filepath, columns):
    if not os.path.exists(filepath):
        pd.DataFrame(columns=columns).to_csv(filepath, index=False)

initialize_file(STOK_BAHAN, ["Nama", "Jumlah", "Satuan", "Tempat Penyimpanan", "Tanggal Expired"])
initialize_file(STOK_ALAT, ["Nama", "Jumlah", "Lokasi"])
initialize_file(RIWAYAT_FILE, ["Nama", "Kategori", "Jumlah", "Tanggal", "Pengguna", "Keterangan"])

def load_data():
    try:
        bahan_df = pd.read_csv(STOK_BAHAN)
    except:
        bahan_df = pd.DataFrame(columns=["Nama", "Jumlah", "Satuan", "Tempat Penyimpanan", "Tanggal Expired"])
    
    try:
        alat_df = pd.read_csv(STOK_ALAT)
    except:
        alat_df = pd.DataFrame(columns=["Nama", "Jumlah", "Lokasi"])
    
    try:
        riwayat_df = pd.read_csv(RIWAYAT_FILE)
    except:
        riwayat_df = pd.DataFrame(columns=["Nama", "Kategori", "Jumlah", "Tanggal", "Pengguna", "Keterangan"])
    
    return bahan_df, alat_df, riwayat_df

def save_data(bahan_df, alat_df, riwayat_df):
    bahan_df.to_csv(STOK_BAHAN, index=False)
    alat_df.to_csv(STOK_ALAT, index=False)
    riwayat_df.to_csv(RIWAYAT_FILE, index=False)

# Sidebar
st.sidebar.title("Login Pengguna")
role = st.sidebar.selectbox("Pilih peran", ["Mahasiswa", "Dosen", "Laboran"])
pengguna = st.sidebar.text_input("Nama Pengguna", key="pengguna")

bahan_df, alat_df, riwayat_df = load_data()

# Laboran View
if role == "Laboran":
    menu = st.sidebar.selectbox("Menu", ["Stok Bahan Kimia", "Stok Alat Laboratorium", "Peminjaman & Pengembalian", "Riwayat Penggunaan", "Logbook Pemakaian"])

    if menu == "Stok Bahan Kimia":
        st.title("Stok Bahan Kimia")
        st.dataframe(bahan_df)

        st.subheader("Tambah / Hapus Bahan")
        nama_bahan = st.text_input("Nama Bahan")
        jumlah = st.number_input("Jumlah", min_value=0.0)
        satuan = st.selectbox("Satuan", ["g", "ml"])
        tempat = st.text_input("Tempat Penyimpanan")
        expired = st.date_input("Tanggal Expired")
        
        if st.button("Tambah Bahan"):
            if nama_bahan:
                new = pd.DataFrame([[nama_bahan, jumlah, satuan, tempat, expired]], columns=bahan_df.columns)
                bahan_df = pd.concat([bahan_df, new], ignore_index=True)
                save_data(bahan_df, alat_df, riwayat_df)
                st.success("Bahan ditambahkan.")
            else:
                st.error("Nama bahan harus diisi.")

        if st.button("Hapus Bahan"):
            bahan_df = bahan_df[bahan_df["Nama"] != nama_bahan]
            save_data(bahan_df, alat_df, riwayat_df)
            st.success("Bahan dihapus.")

    elif menu == "Stok Alat Laboratorium":
        st.title("Stok Alat Laboratorium")
        st.dataframe(alat_df)

        st.subheader("Tambah / Hapus Alat")
        nama_alat = st.text_input("Nama Alat")
        jumlah_alat = st.number_input("Jumlah", min_value=0, step=1)
        lokasi = st.text_input("Lokasi")

        if st.button("Tambah Alat"):
            if nama_alat:
                new = pd.DataFrame([[nama_alat, jumlah_alat, lokasi]], columns=alat_df.columns)
                alat_df = pd.concat([alat_df, new], ignore_index=True)
                save_data(bahan_df, alat_df, riwayat_df)
                st.success("Alat ditambahkan.")
            else:
                st.error("Nama alat harus diisi.")

        if st.button("Hapus Alat"):
            alat_df = alat_df[alat_df["Nama"] != nama_alat]
            save_data(bahan_df, alat_df, riwayat_df)
            st.success("Alat dihapus.")

    elif menu == "Peminjaman & Pengembalian":
        st.title("Peminjaman & Pengembalian Alat")
        if not alat_df.empty:
            alat_dipilih = st.selectbox("Nama Alat", alat_df["Nama"].unique())
            jumlah = st.number_input("Jumlah", min_value=1, step=1)
            aksi = st.radio("Aksi", ["Pinjam", "Kembalikan"])
            keterangan = st.text_input("Keterangan")

            if st.button("Simpan Aksi"):
                idx = alat_df[alat_df["Nama"] == alat_dipilih].index[0]
                if aksi == "Pinjam" and alat_df.at[idx, "Jumlah"] >= jumlah:
                    alat_df.at[idx, "Jumlah"] -= jumlah
                elif aksi == "Kembalikan":
                    alat_df.at[idx, "Jumlah"] += jumlah
                else:
                    st.error("Jumlah tidak mencukupi.")
                    st.stop()
                
                log = pd.DataFrame([[alat_dipilih, "Alat", jumlah, datetime.now().date(), pengguna, f"{aksi}: {keterangan}"]],
                                   columns=riwayat_df.columns)
                riwayat_df = pd.concat([riwayat_df, log], ignore_index=True)
                save_data(bahan_df, alat_df, riwayat_df)
                st.success(f"Alat berhasil {aksi.lower()}.")
        else:
            st.warning("Belum ada data alat.")

    elif menu == "Riwayat Penggunaan":
        st.title("Riwayat Penggunaan")
        st.dataframe(riwayat_df)

    elif menu == "Logbook Pemakaian":
        st.title("Logbook Pemakaian (Monitoring)")
        st.dataframe(riwayat_df)

# Mahasiswa & Dosen View
elif role in ["Mahasiswa", "Dosen"]:
    menu = st.sidebar.selectbox("Menu", ["Stok Bahan Kimia", "Stok Alat Laboratorium", "Logbook Pemakaian"])

    if menu == "Stok Bahan Kimia":
        st.title("Stok Bahan Kimia")
        st.dataframe(bahan_df)

    elif menu == "Stok Alat Laboratorium":
        st.title("Stok Alat Laboratorium")
        st.dataframe(alat_df)

    elif menu == "Logbook Pemakaian":
        st.title("Isi Logbook Pemakaian")
        nama = st.text_input("Nama Barang")
        kategori = st.selectbox("Kategori", ["Bahan", "Alat"])

        if kategori == "Alat":
            jumlah = st.number_input("Jumlah", min_value=1, step=1, format="%d")
            satuan = "buah"
        else:
            jumlah = st.number_input("Jumlah", min_value=0.1, step=0.1, format="%.2f")
            satuan = st.selectbox("Satuan", ["g", "ml"])

        tanggal = st.date_input("Tanggal")
        keterangan = st.text_area("Keterangan")

        if st.button("Catat Pemakaian"):
            if nama:
                jumlah_akhir = f"{jumlah} {satuan}"
                log = pd.DataFrame([[nama, kategori, jumlah_akhir, tanggal, pengguna, keterangan]], columns=riwayat_df.columns)
                riwayat_df = pd.concat([riwayat_df, log], ignore_index=True)
                save_data(bahan_df, alat_df, riwayat_df)
                st.success("Penggunaan berhasil dicatat.")
            else:
                st.error("Nama barang harus diisi.")
