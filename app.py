import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ---------- Path dan File ----------
DATA_DIR = "data"
ALAT_FILE = os.path.join(DATA_DIR, "stok_alat.csv")
BAHAN_FILE = os.path.join(DATA_DIR, "stok_bahan.csv")
RIWAYAT_FILE = os.path.join(DATA_DIR, "riwayat_penggunaan.csv")

# ---------- Load dan Buat File ----------
def load_data():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(ALAT_FILE):
        pd.DataFrame(columns=["Nama Alat", "Jumlah", "Tempat"]).to_csv(ALAT_FILE, index=False)
    if not os.path.exists(BAHAN_FILE):
        pd.DataFrame(columns=["Nama Bahan", "Jumlah", "Tanggal Expired", "Tempat Penyimpanan"]).to_csv(BAHAN_FILE, index=False)
    if not os.path.exists(RIWAYAT_FILE):
        pd.DataFrame(columns=["Nama", "Kategori", "Jumlah", "Tanggal", "Pengguna", "Keperluan"]).to_csv(RIWAYAT_FILE, index=False)

    return pd.read_csv(ALAT_FILE), pd.read_csv(BAHAN_FILE), pd.read_csv(RIWAYAT_FILE)

alat_df, bahan_df, riwayat_df = load_data()

# ---------- Konfigurasi Halaman ----------
st.set_page_config(page_title="Inventarisasi Lab Kimia", layout="wide")
st.markdown("<h1 style='text-align:center; color:navy;'>📘 Inventarisasi Lab Kimia - Politeknik AKA Bogor</h1>", unsafe_allow_html=True)
menu = st.sidebar.radio("Menu", ["Stok Alat", "Stok Bahan", "Riwayat", "Tambah Data", "Stok per Lemari"])

# ---------- Tampilan Stok Alat ----------
if menu == "Stok Alat":
    st.subheader("📌 Daftar Stok Alat")
    st.dataframe(alat_df)
    search = st.text_input("🔍 Cari alat:")
    if search:
        st.dataframe(alat_df[alat_df["Nama Alat"].str.contains(search, case=False)])

# ---------- Tampilan Stok Bahan ----------
elif menu == "Stok Bahan":
    st.subheader("🧪 Daftar Stok Bahan Kimia")
    df = bahan_df.copy()

    required_columns = ["Nama Bahan", "Jumlah", "Tanggal Expired", "Tempat Penyimpanan"]
    for col in required_columns:
        if col not in df.columns:
            st.error(f"❌ Kolom '{col}' tidak ditemukan di stok_bahan.csv")
            st.stop()

    df["Jumlah Awal"] = df["Jumlah"].str.extract(r"(\d+\.?\d*)").astype(float)
    df["Satuan"] = df["Jumlah"].str.extract(r"([a-zA-Z]+)")

    penggunaan = riwayat_df[riwayat_df["Kategori"] == "Bahan"]
    penggunaan["Jumlah"] = pd.to_numeric(penggunaan["Jumlah"], errors="coerce")
    terpakai = penggunaan.groupby("Nama")["Jumlah"].sum().reset_index(name="Terpakai")

    df = df.merge(terpakai, how="left", left_on="Nama Bahan", right_on="Nama")
    df["Terpakai"] = df["Terpakai"].fillna(0)
    df.drop(columns=["Nama"], inplace=True, errors="ignore")
    df["Sisa"] = df["Jumlah Awal"] - df["Terpakai"]

    def status(sisa, satuan):
        satuan = str(satuan).lower()
        if satuan == "ml" and sisa < 50:
            return "❗ Menipis"
        elif satuan == "g" and sisa < 25:
            return "❗ Menipis"
        elif sisa < 10:
            return "❗ Menipis"
        return "✅ Cukup"

    df["Status"] = df.apply(lambda row: status(row["Sisa"], row["Satuan"]), axis=1)

    st.dataframe(df[["Nama Bahan", "Jumlah", "Terpakai", "Sisa", "Satuan", "Status", "Tanggal Expired", "Tempat Penyimpanan"]])

    search = st.text_input("🔍 Cari bahan:")
    if search:
        hasil = df[df["Nama Bahan"].str.contains(search, case=False)]
        st.dataframe(hasil)

# ---------- Riwayat ----------
elif menu == "Riwayat":
    st.subheader("📄 Riwayat Penggunaan Alat & Bahan")
    st.dataframe(riwayat_df)

# ---------- Tambah Data ----------
elif menu == "Tambah Data":
    st.subheader("➕ Tambah Inventaris / Penggunaan / Pengembalian")
    opsi = st.selectbox("Kategori", ["Alat", "Bahan", "Riwayat Penggunaan", "Pengembalian Alat"])

    if opsi == "Alat":
        nama = st.text_input("Nama Alat")
        jumlah = st.number_input("Jumlah", min_value=1)
        tempat = st.text_input("Tempat Penyimpanan")
        if st.button("Simpan"):
            new = pd.DataFrame([[nama, jumlah, tempat]], columns=alat_df.columns)
            alat_df = pd.concat([alat_df, new], ignore_index=True)
            alat_df.to_csv(ALAT_FILE, index=False)
            st.success("✅ Alat ditambahkan")

    elif opsi == "Bahan":
        nama = st.text_input("Nama Bahan")
        jumlah = st.text_input("Jumlah (misal 500 ml)")
        expired = st.date_input("Tanggal Expired")
        tempat = st.text_input("Tempat Penyimpanan")
        if st.button("Simpan"):
            new = pd.DataFrame([[nama, jumlah, expired, tempat]], columns=bahan_df.columns)
            bahan_df = pd.concat([bahan_df, new], ignore_index=True)
            bahan_df.to_csv(BAHAN_FILE, index=False)
            st.success("✅ Bahan ditambahkan")

        st.markdown("---")
        st.subheader("🗑️ Hapus Bahan")
        if not bahan_df.empty:
            target = st.selectbox("Pilih bahan", bahan_df["Nama Bahan"].unique())
            if st.button("Hapus Bahan"):
                bahan_df = bahan_df[bahan_df["Nama Bahan"] != target]
                bahan_df.to_csv(BAHAN_FILE, index=False)
                st.success(f"✅ Bahan '{target}' dihapus")

    elif opsi == "Riwayat Penggunaan":
        nama = st.text_input("Nama")
        kategori = st.selectbox("Kategori", ["Alat", "Bahan"])
        jumlah = st.text_input("Jumlah Digunakan")
        tanggal = st.date_input("Tanggal", value=datetime.today())
        pengguna = st.text_input("Pengguna")
        keperluan = st.text_area("Keperluan")
        if st.button("Simpan"):
            new = pd.DataFrame([[nama, kategori, jumlah, tanggal, pengguna, keperluan]], columns=riwayat_df.columns)
            riwayat_df = pd.concat([riwayat_df, new], ignore_index=True)
            riwayat_df.to_csv(RIWAYAT_FILE, index=False)
            st.success("✅ Riwayat disimpan")

    elif opsi == "Pengembalian Alat":
        if alat_df.empty:
            st.warning("Stok alat kosong.")
        else:
            nama = st.selectbox("Alat Dikembalikan", alat_df["Nama Alat"].unique())
            jumlah = st.number_input("Jumlah", min_value=1)
            tanggal = st.date_input("Tanggal", value=datetime.today())
            pengguna = st.text_input("Dikembalikan Oleh")
            catatan = st.text_area("Catatan", "")
            if st.button("Simpan Pengembalian"):
                alat_df.loc[alat_df["Nama Alat"] == nama, "Jumlah"] += jumlah
                alat_df.to_csv(ALAT_FILE, index=False)
                new = pd.DataFrame([[nama, "Pengembalian Alat", -jumlah, tanggal, pengguna, f"Pengembalian. {catatan}"]], columns=riwayat_df.columns)
                riwayat_df = pd.concat([riwayat_df, new], ignore_index=True)
                riwayat_df.to_csv(RIWAYAT_FILE, index=False)
                st.success("✅ Pengembalian disimpan")

# ---------- Stok per Lemari ----------
elif menu == "Stok per Lemari":
    st.subheader("📦 Total Stok per Lemari")
    df = bahan_df.copy()
    df["Jumlah Angka"] = df["Jumlah"].str.extract(r'(\d+\.?\d*)')
    df["Jumlah Angka"] = pd.to_numeric(df["Jumlah Angka"], errors="coerce").fillna(0)
    df["Tempat Penyimpanan"] = df["Tempat Penyimpanan"].fillna("Tidak Diketahui")

    hasil = df.groupby("Tempat Penyimpanan")["Jumlah Angka"].sum().reset_index()
    hasil.columns = ["Tempat Penyimpanan", "Total Jumlah"]
    st.dataframe(hasil)
