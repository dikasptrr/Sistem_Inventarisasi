import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- Path File ---
DATA_DIR = "data"
ALAT_FILE = os.path.join(DATA_DIR, "stok_alat.csv")
BAHAN_FILE = os.path.join(DATA_DIR, "stok_bahan.csv")
RIWAYAT_FILE = os.path.join(DATA_DIR, "riwayat_penggunaan.csv")

# --- Load atau buat file ---
def load_data():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(ALAT_FILE):
        pd.DataFrame(columns=["Nama Alat", "Jumlah", "Tempat Penyimpanan"]).to_csv(ALAT_FILE, index=False)
    if not os.path.exists(BAHAN_FILE):
        pd.DataFrame(columns=["Nama Bahan", "Jumlah", "Tanggal Expired", "Tempat Penyimpanan"]).to_csv(BAHAN_FILE, index=False)
    if not os.path.exists(RIWAYAT_FILE):
        pd.DataFrame(columns=["Nama", "Kategori", "Jumlah Digunakan", "Tanggal", "Digunakan Oleh", "Keperluan", "Status"]).to_csv(RIWAYAT_FILE, index=False)
    return pd.read_csv(ALAT_FILE), pd.read_csv(BAHAN_FILE), pd.read_csv(RIWAYAT_FILE)

# --- Load data awal ---
alat_df, bahan_df, riwayat_df = load_data()

# --- Sidebar ---
st.title("📒 Inventarisasi Laboratorium Kimia Politeknik AKA Bogor")
menu = st.sidebar.selectbox("Menu", ["Stok Alat", "Stok Bahan", "Riwayat Penggunaan", "Tambah Data"])

# --- Stok Alat ---
if menu == "Stok Alat":
    st.header("📌 Stok Alat Laboratorium")
    st.dataframe(alat_df)
    with st.expander("🔍 Cari Alat"):
        search = st.text_input("Nama alat:")
        filtered = alat_df[alat_df["Nama Alat"].str.contains(search, case=False)]
        st.dataframe(filtered)

# --- Stok Bahan ---
elif menu == "Stok Bahan":
    st.header("🧪 Stok Bahan Kimia")
    bahan_df_copy = bahan_df.copy()
    bahan_df_copy["Jumlah Awal"] = bahan_df_copy["Jumlah"].str.extract(r'(\d+\.?\d*)').astype(float)
    bahan_df_copy["Satuan"] = bahan_df_copy["Jumlah"].str.extract(r'([a-zA-Z]+)')

    penggunaan = riwayat_df[riwayat_df["Kategori"] == "Bahan"]
    penggunaan = penggunaan.groupby("Nama")["Jumlah Digunakan"].apply(lambda x: pd.to_numeric(x, errors='coerce').sum()).reset_index(name="Jumlah Terpakai")

    merged = pd.merge(bahan_df_copy, penggunaan, how="left", left_on="Nama Bahan", right_on="Nama")
    merged["Jumlah Terpakai"].fillna(0, inplace=True)
    merged["Sisa"] = merged["Jumlah Awal"] - merged["Jumlah Terpakai"]

    def status_stok(sisa, satuan):
        satuan = str(satuan).lower()
        if pd.isna(sisa): return "Tidak Diketahui"
        if satuan == "ml": return "❗ Menipis" if sisa < 50 else "Cukup"
        if satuan == "g": return "❗ Menipis" if sisa < 25 else "Cukup"
        return "❗ Menipis" if sisa < 10 else "Cukup"

    merged["Status"] = merged.apply(lambda row: status_stok(row["Sisa"], row["Satuan"]), axis=1)

    st.dataframe(merged[["Nama Bahan", "Jumlah", "Jumlah Terpakai", "Sisa", "Satuan", "Status", "Tanggal Expired", "Tempat Penyimpanan"]])
    
    with st.expander("🔍 Cari Bahan"):
        search = st.text_input("Nama bahan:")
        filtered = merged[merged["Nama Bahan"].str.contains(search, case=False)]
        st.dataframe(filtered)

# --- Riwayat Penggunaan ---
elif menu == "Riwayat Penggunaan":
    st.header("📝 Riwayat Penggunaan")
    st.dataframe(riwayat_df)

# --- Tambah Data ---
elif menu == "Tambah Data":
    st.header("➕ Tambah Data")
    kategori = st.selectbox("Kategori", ["Alat", "Bahan", "Riwayat Penggunaan"])

    if kategori == "Alat":
        nama = st.text_input("Nama Alat")
        jumlah = st.number_input("Jumlah", min_value=1)
        lokasi = st.text_input("Tempat Penyimpanan")
        if st.button("Simpan Alat"):
            new_row = {"Nama Alat": nama, "Jumlah": jumlah, "Tempat Penyimpanan": lokasi}
            alat_df = pd.concat([alat_df, pd.DataFrame([new_row])], ignore_index=True)
            alat_df.to_csv(ALAT_FILE, index=False)
            st.success("✅ Alat ditambahkan")

    elif kategori == "Bahan":
        nama = st.text_input("Nama Bahan")
        jumlah = st.text_input("Jumlah (mis. 500 ml / 1 kg)")
        expired = st.date_input("Tanggal Expired")
        lokasi = st.text_input("Tempat Penyimpanan")
        if st.button("Simpan Bahan"):
            new_row = {"Nama Bahan": nama, "Jumlah": jumlah, "Tanggal Expired": expired, "Tempat Penyimpanan": lokasi}
            bahan_df = pd.concat([bahan_df, pd.DataFrame([new_row])], ignore_index=True)
            bahan_df.to_csv(BAHAN_FILE, index=False)
            st.success("✅ Bahan ditambahkan")

        st.subheader("🗑️ Hapus Bahan")
        if not bahan_df.empty:
            bahan_terpilih = st.selectbox("Pilih bahan", bahan_df["Nama Bahan"].unique())
            if st.button("Hapus Bahan"):
                bahan_df = bahan_df[bahan_df["Nama Bahan"] != bahan_terpilih]
                bahan_df.to_csv(BAHAN_FILE, index=False)
                st.success(f"✅ '{bahan_terpilih}' dihapus")

    elif kategori == "Riwayat Penggunaan":
        nama = st.text_input("Nama Barang")
        kategori_penggunaan = st.selectbox("Kategori", ["Alat", "Bahan"])
        jumlah = st.text_input("Jumlah Digunakan")
        tanggal = st.date_input("Tanggal", value=datetime.today())
        oleh = st.text_input("Digunakan Oleh")
        keperluan = st.text_area("Keperluan")
        status = st.selectbox("Status", ["Digunakan", "Dikembalikan"] if kategori_penggunaan == "Alat" else ["Digunakan"])
        if st.button("Simpan Riwayat"):
            new_row = {
                "Nama": nama,
                "Kategori": kategori_penggunaan,
                "Jumlah Digunakan": jumlah,
                "Tanggal": tanggal,
                "Digunakan Oleh": oleh,
                "Keperluan": keperluan,
                "Status": status
            }
            riwayat_df = pd.concat([riwayat_df, pd.DataFrame([new_row])], ignore_index=True)
            riwayat_df.to_csv(RIWAYAT_FILE, index=False)
            st.success("✅ Riwayat penggunaan disimpan")
