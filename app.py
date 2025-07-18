import streamlit as st
import pandas as pd
from datetime import datetime

# File CSV
BAHAN_FILE = "data/stok_bahan.csv"
ALAT_FILE = "data/stok_alat.csv"
RIWAYAT_FILE = "data/riwayat_penggunaan.csv"

# Load data
def load_data(file, columns):
    try:
        df = pd.read_csv(file)
        for col in columns:
            if col not in df.columns:
                df[col] = ""
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=columns)

# Load datasets
bahan_df = load_data(BAHAN_FILE, ["Nama Bahan", "Jumlah", "Satuan", "Tempat Penyimpanan", "Tanggal Expired"])
alat_df = load_data(ALAT_FILE, ["Nama Alat", "Jumlah", "Lokasi"])
riwayat_df = load_data(RIWAYAT_FILE, ["Nama", "Kategori", "Jumlah", "Tanggal", "Pengguna", "Keterangan"])

# Setup page
st.set_page_config(page_title="Inventarisasi Lab Kimia", layout="wide")
st.title("🔬 Inventarisasi Laboratorium Kimia")

# Pilih peran pengguna
role = st.sidebar.selectbox("Masuk sebagai", ["Mahasiswa", "Dosen", "Laboran"])

# Daftar menu berdasarkan role
if role == "Laboran":
    menu_options = [
        "Stok Bahan Kimia", "Stok Alat Laboratorium", "Tambah Data",
        "Riwayat Penggunaan", "Stok per Lemari", "Transaksi Lab"
    ]
elif role == "Dosen":
    menu_options = [
        "Stok Bahan Kimia", "Stok Alat Laboratorium", "Riwayat Penggunaan", "Stok per Lemari"
    ]
else:  # Mahasiswa
    menu_options = [
        "Stok Bahan Kimia", "Stok Alat Laboratorium", "Riwayat Penggunaan"
    ]

menu = st.sidebar.selectbox("Pilih Menu", menu_options)

# ------------------------------
# 1. STOK BAHAN KIMIA
# ------------------------------
if menu == "Stok Bahan Kimia":
    st.subheader("📦 Stok Bahan Kimia")
    bahan_display = bahan_df.copy()
    bahan_display["Jumlah"] = pd.to_numeric(bahan_display["Jumlah"], errors="coerce")

    if not riwayat_df.empty:
        penggunaan = riwayat_df[riwayat_df["Kategori"] == "Bahan"]
        penggunaan["Jumlah"] = pd.to_numeric(penggunaan["Jumlah"].str.extract(r'(\d+)')[0], errors="coerce")
        terpakai = penggunaan.groupby("Nama")["Jumlah"].sum().reset_index(name="Terpakai")
        bahan_display = pd.merge(bahan_display, terpakai, left_on="Nama Bahan", right_on="Nama", how="left").fillna(0)
        bahan_display["Sisa"] = bahan_display["Jumlah"] - bahan_display["Terpakai"]
        bahan_display.drop(columns=["Nama"], inplace=True)

    st.dataframe(bahan_display)

# ------------------------------
# 2. STOK ALAT
# ------------------------------
elif menu == "Stok Alat Laboratorium":
    st.subheader("🔧 Stok Alat Laboratorium")
    st.dataframe(alat_df)

# ------------------------------
# 3. TAMBAH DATA (KHUSUS LABORAN)
# ------------------------------
elif menu == "Tambah Data" and role == "Laboran":
    st.subheader("➕ Tambah Data")
    tab1, tab2, tab3 = st.tabs(["Bahan Kimia", "Alat Laboratorium", "Riwayat Penggunaan"])

    with tab1:
        nama = st.text_input("Nama Bahan")
        jumlah = st.number_input("Jumlah", min_value=0.00)
        satuan = st.selectbox("Satuan", ["g", "mg", "kg", "mL", "L"])
        tempat = st.text_input("Tempat Penyimpanan")
        expired = st.date_input("Tanggal Expired")
        if st.button("Simpan Bahan"):
            new = pd.DataFrame([[nama, jumlah, satuan, tempat, expired]], columns=bahan_df.columns)
            bahan_df = pd.concat([bahan_df, new], ignore_index=True)
            bahan_df.to_csv(BAHAN_FILE, index=False)
            st.success("✅ Data bahan disimpan")

    with tab2:
        nama = st.text_input("Nama Alat")
        jumlah = st.number_input("Jumlah", min_value=0)
        lokasi = st.text_input("Lokasi Penyimpanan")
        if st.button("Simpan Alat"):
            new = pd.DataFrame([[nama, jumlah, lokasi]], columns=alat_df.columns)
            alat_df = pd.concat([alat_df, new], ignore_index=True)
            alat_df.to_csv(ALAT_FILE, index=False)
            st.success("✅ Data alat disimpan")

    with tab3:
        nama = st.selectbox("Nama", list(bahan_df["Nama Bahan"].unique()) + list(alat_df["Nama Alat"].unique()))
        kategori = st.selectbox("Kategori", ["Bahan", "Alat"])
        jumlah = st.text_input("Jumlah (contoh: 50 ml)")
        tanggal = st.date_input("Tanggal", value=datetime.today())
        pengguna = st.text_input("Pengguna")
        keterangan = st.text_area("Keterangan")
        if st.button("Simpan Riwayat"):
            new = pd.DataFrame([[nama, kategori, jumlah, tanggal, pengguna, keterangan]], columns=riwayat_df.columns)
            riwayat_df = pd.concat([riwayat_df, new], ignore_index=True)
            riwayat_df.to_csv(RIWAYAT_FILE, index=False)
            st.success("✅ Riwayat penggunaan disimpan")

# ------------------------------
# 4. RIWAYAT
# ------------------------------
elif menu == "Riwayat Penggunaan":
    st.subheader("📄 Riwayat Penggunaan Alat & Bahan")
    st.dataframe(riwayat_df)

# ------------------------------
# 5. STOK PER LEMARI
# ------------------------------
elif menu == "Stok per Lemari":
    st.subheader("📁 Stok Bahan per Lemari")
    if "Tempat Penyimpanan" in bahan_df.columns:
        lemari = st.selectbox("Pilih Lemari", bahan_df["Tempat Penyimpanan"].unique())
        filtered = bahan_df[bahan_df["Tempat Penyimpanan"] == lemari]
        st.dataframe(filtered)
    else:
        st.warning("Kolom 'Tempat Penyimpanan' tidak ditemukan.")

# ------------------------------
# 6. TRANSAKSI KHUSUS LABORAN
# ------------------------------
elif menu == "Transaksi Lab" and role == "Laboran":
    st.subheader("🛠️ Transaksi Alat & Bahan (Laboran)")

    jenis_transaksi = st.selectbox("Jenis Transaksi", ["Peminjaman Alat", "Pengembalian Alat", "Pengambilan Bahan Kimia"])

    if jenis_transaksi == "Peminjaman Alat":
        if alat_df.empty:
            st.warning("Stok alat kosong.")
        else:
            nama = st.selectbox("Alat Dipinjam", alat_df["Nama Alat"].unique())
            jumlah = st.number_input("Jumlah Dipinjam", min_value=1)
            tanggal = st.date_input("Tanggal", value=datetime.today())
            pengguna = st.text_input("Dipinjam Oleh")
            keperluan = st.text_area("Keperluan")
            if st.button("Simpan Peminjaman"):
                alat_df.loc[alat_df["Nama Alat"] == nama, "Jumlah"] -= jumlah
                alat_df.to_csv(ALAT_FILE, index=False)
                new = pd.DataFrame([[nama, "Alat", jumlah, tanggal, pengguna, f"Peminjaman. {keperluan}"]], columns=riwayat_df.columns)
                riwayat_df = pd.concat([riwayat_df, new], ignore_index=True)
                riwayat_df.to_csv(RIWAYAT_FILE, index=False)
                st.success("✅ Peminjaman disimpan")

    elif jenis_transaksi == "Pengembalian Alat":
        nama = st.selectbox("Alat Dikembalikan", alat_df["Nama Alat"].unique())
        jumlah = st.number_input("Jumlah Dikembalikan", min_value=1)
        tanggal = st.date_input("Tanggal", value=datetime.today())
        pengguna = st.text_input("Dikembalikan Oleh")
        catatan = st.text_area("Catatan")
        if st.button("Simpan Pengembalian"):
            alat_df.loc[alat_df["Nama Alat"] == nama, "Jumlah"] += jumlah
            alat_df.to_csv(ALAT_FILE, index=False)
            new = pd.DataFrame([[nama, "Pengembalian Alat", -jumlah, tanggal, pengguna, f"Pengembalian. {catatan}"]], columns=riwayat_df.columns)
            riwayat_df = pd.concat([riwayat_df, new], ignore_index=True)
            riwayat_df.to_csv(RIWAYAT_FILE, index=False)
            st.success("✅ Pengembalian disimpan")

    elif jenis_transaksi == "Pengambilan Bahan Kimia":
        nama = st.selectbox("Bahan Diambil", bahan_df["Nama Bahan"].unique())
        jumlah = st.text_input("Jumlah Diambil (misal 50 ml)")
        tanggal = st.date_input("Tanggal", value=datetime.today())
        pengguna = st.text_input("Diambil Oleh")
        keperluan = st.text_area("Keperluan")
        if st.button("Simpan Pengambilan"):
            new = pd.DataFrame([[nama, "Bahan", jumlah, tanggal, pengguna, f"Pengambilan. {keperluan}"]], columns=riwayat_df.columns)
            riwayat_df = pd.concat([riwayat_df, new], ignore_index=True)
            riwayat_df.to_csv(RIWAYAT_FILE, index=False)
            st.success("✅ Pengambilan bahan disimpan")
