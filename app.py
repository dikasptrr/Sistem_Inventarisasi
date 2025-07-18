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
    bahan_df_copy["Satuan"] = bahan_df_copy["Jumlah"].str.extract(r'([a-zA-Z]+)')

    # Hitung total penggunaan bahan
    penggunaan_bahan = riwayat_df[riwayat_df["Kategori"] == "Bahan"]
    penggunaan_agg = (
        penggunaan_bahan.groupby("Nama")["Jumlah Digunakan"]
        .apply(lambda x: pd.to_numeric(x, errors='coerce').sum())
        .reset_index()
        .rename(columns={"Jumlah Digunakan": "Jumlah Terpakai"})
    )

    # Gabungkan dan hitung sisa
    merged = pd.merge(bahan_df_copy, penggunaan_agg, how="left", left_on="Nama Bahan", right_on="Nama")
    merged["Jumlah Terpakai"] = merged["Jumlah Terpakai"].fillna(0)
    merged["Sisa"] = merged["Jumlah Awal"] - merged["Jumlah Terpakai"]

    # --- Logika ambang batas berdasarkan satuan ---
    def status_stok(sisa, satuan):
        if pd.isna(sisa):
            return "Tidak Diketahui"
        satuan = str(satuan).lower()
        if satuan == "ml":
            return "❗ Stok Menipis" if sisa < 50 else "Cukup"
        elif satuan == "g":
            return "❗ Stok Menipis" if sisa < 25 else "Cukup"
        else:
            return "❗ Stok Menipis" if sisa < 10 else "Cukup"

    merged["Status"] = merged.apply(lambda row: status_stok(row["Sisa"], row["Satuan"]), axis=1)

    # Tampilkan peringatan umum
    if "❗ Stok Menipis" in merged["Status"].values:
        st.warning("⚠️ Beberapa bahan memiliki stok menipis!")

    # Tampilkan hasil
    st.dataframe(
        merged[["Nama Bahan", "Jumlah", "Jumlah Terpakai", "Sisa", "Satuan", "Status", "Tanggal Expired", "Tempat Penyimpanan"]]
    )

    # Fitur pencarian
    with st.expander("🔍 Cari Bahan"):
        search = st.text_input("Nama bahan:")
        filtered = merged[merged["Nama Bahan"].str.contains(search, case=False)]
        st.dataframe(
            filtered[["Nama Bahan", "Jumlah", "Jumlah Terpakai", "Sisa", "Satuan", "Status", "Tanggal Expired", "Tempat Penyimpanan"]]
        )

# --- Riwayat Penggunaan ---
elif menu == "Riwayat Penggunaan":
    st.header("📝 Riwayat Penggunaan Alat dan Bahan")
    st.dataframe(riwayat_df)

# --- Tambah Data ---
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
            alat_df.to_csv(ALAT_FILE, index=False)
            st.success("Alat berhasil ditambahkan!")

    elif kategori == "Bahan":
        st.subheader("🧾 Tambah Bahan")
        nama = st.text_input("Nama Bahan")
        jumlah = st.text_input("Jumlah (mis. 500 ml / 1 kg)")
        expired = st.date_input("Tanggal Kedaluwarsa")
        lokasi = st.text_input("Tempat Penyimpanan")
        if st.button("Simpan"):
            new_row = {"Nama Bahan": nama, "Jumlah": jumlah, "Tanggal Expired": expired, "Tempat Penyimpanan": lokasi}
            bahan_df = pd.concat([bahan_df, pd.DataFrame([new_row])], ignore_index=True)
            bahan_df.to_csv(BAHAN_FILE, index=False)
            st.success("Bahan berhasil ditambahkan!")

        st.markdown("---")
        st.subheader("🗑️ Hapus Data Bahan")
        if not bahan_df.empty:
            bahan_terpilih = st.selectbox("Pilih bahan yang ingin dihapus", bahan_df["Nama Bahan"].unique())
            if st.button("Hapus Bahan"):
                bahan_df = bahan_df[bahan_df["Nama Bahan"] != bahan_terpilih]
                bahan_df.to_csv(BAHAN_FILE, index=False)
                st.success(f"Bahan '{bahan_terpilih}' berhasil dihapus!")
        else:
            st.info("Belum ada data bahan yang bisa dihapus.")


    elif kategori == "Riwayat Penggunaan":
        nama = st.text_input("Nama Alat/Bahan")
        kategori_penggunaan = st.selectbox("Kategori", ["Alat", "Bahan"])
        jumlah = st.text_input("Jumlah Digunakan (angka saja)")
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
            riwayat_df.to_csv(RIWAYAT_FILE, index=False)
            st.success("Riwayat penggunaan berhasil ditambahkan!")

    
