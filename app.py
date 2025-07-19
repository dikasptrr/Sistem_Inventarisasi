import streamlit as st
import pandas as pd
import os
from datetime import date

# === Setup awal dan path file ===
DATA_FOLDER = "data"
STOK_BAHAN_PATH = os.path.join(DATA_FOLDER, "stok_bahan.csv")
STOK_ALAT_PATH = os.path.join(DATA_FOLDER, "stok_alat.csv")
RIWAYAT_PENGGUNAAN_PATH = os.path.join(DATA_FOLDER, "riwayat_penggunaan.csv")

os.makedirs(DATA_FOLDER, exist_ok=True)

# === Inisialisasi file jika belum ada ===
if not os.path.exists(STOK_BAHAN_PATH):
    pd.DataFrame(columns=["Nama", "Jumlah", "Satuan", "Tempat Penyimpanan", "Tanggal Expired"]).to_csv(STOK_BAHAN_PATH, index=False)
if not os.path.exists(STOK_ALAT_PATH):
    pd.DataFrame(columns=["Nama", "Jumlah", "Satuan", "Tempat Penyimpanan"]).to_csv(STOK_ALAT_PATH, index=False)
if not os.path.exists(RIWAYAT_PENGGUNAAN_PATH):
    pd.DataFrame(columns=["Nama Pengguna", "Peran", "Jenis", "Nama Barang", "Jumlah", "Tanggal", "Status"]).to_csv(RIWAYAT_PENGGUNAAN_PATH, index=False)

# === Fungsi utilitas ===
def load_data(path):
    return pd.read_csv(path)

def save_data(df, path):
    df.to_csv(path, index=False)

def update_stok_bahan(nama, jumlah_pakai):
    df = load_data(STOK_BAHAN_PATH)
    df.loc[df["Nama"] == nama, "Jumlah"] -= jumlah_pakai
    save_data(df, STOK_BAHAN_PATH)

def update_stok_alat(nama, jumlah, status):
    df = load_data(STOK_ALAT_PATH)
    if status == "Peminjaman":
        df.loc[df["Nama"] == nama, "Jumlah"] -= jumlah
    elif status == "Pengembalian":
        df.loc[df["Nama"] == nama, "Jumlah"] += jumlah
    save_data(df, STOK_ALAT_PATH)

# === Sidebar Login ===
st.sidebar.markdown("### 🔐 Login Pengguna")
peran = st.sidebar.selectbox("Pilih Peran", ["Laboran", "Mahasiswa", "Dosen"])
nama_pengguna = st.sidebar.text_input("Nama Pengguna")

st.sidebar.markdown("### 📋 Menu")

# === Laboran ===
if peran == "Laboran":
    menu = st.sidebar.selectbox("Pilih Menu", ["Stok Bahan Kimia", "Stok Alat Laboratorium", "Logbook Pemakaian"])
    
    if menu == "Stok Bahan Kimia":
        st.title("📦 Stok Bahan Kimia")
        df_bahan = load_data(STOK_BAHAN_PATH)
        st.dataframe(df_bahan.reset_index(drop=True).rename(lambda x: x+1), use_container_width=True)

        st.markdown("### Tambah / Hapus Bahan")
        nama_bahan = st.text_input("Nama Bahan")
        jumlah = st.number_input("Jumlah", value=0.0, step=0.1, format="%.2f")
        satuan = st.selectbox("Satuan", ["g", "ml"])
        tempat = st.selectbox("Tempat Penyimpanan", ["Lemari 1", "Lemari 2", "Lemari 3"])
        expired = st.date_input("Tanggal Expired", value=date.today())

        if st.button("Tambah Bahan"):
            df_bahan = load_data(STOK_BAHAN_PATH)
            if nama_bahan in df_bahan["Nama"].values:
                df_bahan.loc[df_bahan["Nama"] == nama_bahan, "Jumlah"] += jumlah
            else:
                df_baru = pd.DataFrame([[nama_bahan, jumlah, satuan, tempat, expired]], columns=df_bahan.columns)
                df_bahan = pd.concat([df_bahan, df_baru], ignore_index=True)
            save_data(df_bahan, STOK_BAHAN_PATH)
            st.success("Bahan berhasil ditambahkan atau diperbarui.")

    elif menu == "Stok Alat Laboratorium":
        st.title("🔧 Stok Alat Laboratorium")
        df_alat = load_data(STOK_ALAT_PATH)
        st.dataframe(df_alat.reset_index(drop=True).rename(lambda x: x+1), use_container_width=True)

        st.markdown("### Tambah / Hapus Alat")
        nama_alat = st.text_input("Nama Alat")
        jumlah = st.number_input("Jumlah", value=0, step=1, format="%d")
        satuan = "buah"
        tempat = st.selectbox("Tempat Penyimpanan", ["Lemari 1", "Lemari 2", "Lemari 3"])

        if st.button("Tambah Alat"):
            df_alat = load_data(STOK_ALAT_PATH)
            if nama_alat in df_alat["Nama"].values:
                df_alat.loc[df_alat["Nama"] == nama_alat, "Jumlah"] += jumlah
            else:
                df_baru = pd.DataFrame([[nama_alat, jumlah, satuan, tempat]], columns=df_alat.columns)
                df_alat = pd.concat([df_alat, df_baru], ignore_index=True)
            save_data(df_alat, STOK_ALAT_PATH)
            st.success("Alat berhasil ditambahkan atau diperbarui.")

        st.markdown("### Hapus Alat dari Data")
        alat_untuk_dihapus = st.selectbox("Pilih Alat untuk Dihapus", df_alat["Nama"].unique().tolist())
        if st.button("Hapus Alat Ini"):
            df_alat = df_alat[df_alat["Nama"] != alat_untuk_dihapus]
            save_data(df_alat, STOK_ALAT_PATH)
            st.success(f"Alat '{alat_untuk_dihapus}' berhasil dihapus.")


    elif menu == "Logbook Pemakaian":
        st.title("📖 Logbook Pemakaian")
        df_log = load_data(RIWAYAT_PENGGUNAAN_PATH)
        st.dataframe(df_log.reset_index(drop=True).rename(lambda x: x+1), use_container_width=True)

# === Mahasiswa & Dosen ===
else:
    menu = st.sidebar.selectbox("Pilih Menu", ["Isi Logbook Pemakaian"])

    if menu == "Isi Logbook Pemakaian":
        tab1, tab2 = st.tabs(["Peminjaman & Pengembalian Alat", "Penggunaan Bahan Kimia"])

        # === Tab 1: Alat ===
        with tab1:
            st.header("🔧 Peminjaman & Pengembalian Alat")
            df_alat = load_data(STOK_ALAT_PATH)
            alat_list = df_alat["Nama"].tolist()
            pilihan = st.multiselect("Pilih Alat", alat_list)
            status = st.radio("Status", ["Peminjaman", "Pengembalian"])
            jumlah_dict = {}

            for alat in pilihan:
                jumlah_dict[alat] = st.number_input(f"Jumlah untuk {alat}", min_value=1, step=1, key=f"alat_{alat}")

            if st.button("Simpan Peminjaman/Pengembalian"):
                today = date.today()
                for alat in pilihan:
                    jumlah = jumlah_dict[alat]
                    update_stok_alat(alat, jumlah, status)
                    log_entry = {
                        "Nama Pengguna": nama_pengguna,
                        "Peran": peran,
                        "Jenis": "Alat",
                        "Nama Barang": alat,
                        "Jumlah": jumlah,
                        "Tanggal": today,
                        "Status": status
                    }
                    df_log = load_data(RIWAYAT_PENGGUNAAN_PATH)
                    df_log = pd.concat([df_log, pd.DataFrame([log_entry])], ignore_index=True)
                    save_data(df_log, RIWAYAT_PENGGUNAAN_PATH)
                st.success("Data peminjaman/pengembalian alat berhasil disimpan.")

        # === Tab 2: Bahan Kimia ===
        with tab2:
            st.header("⚗️ Penggunaan Bahan Kimia")
            df_bahan = load_data(STOK_BAHAN_PATH)
            bahan_list = df_bahan["Nama"].tolist()
            pilihan_bahan = st.multiselect("Pilih Bahan Kimia", bahan_list)
            jumlah_dict_bahan = {}

            for bahan in pilihan_bahan:
                jumlah_dict_bahan[bahan] = st.number_input(f"Jumlah yang digunakan untuk {bahan}", min_value=0.01, step=0.01, format="%.2f", key=f"bahan_{bahan}")

            if st.button("Simpan Penggunaan Bahan"):
                today = date.today()
                for bahan in pilihan_bahan:
                    jumlah = jumlah_dict_bahan[bahan]
                    update_stok_bahan(bahan, jumlah)
                    log_entry = {
                        "Nama Pengguna": nama_pengguna,
                        "Peran": peran,
                        "Jenis": "Bahan Kimia",
                        "Nama Barang": bahan,
                        "Jumlah": jumlah,
                        "Tanggal": today,
                        "Status": "Penggunaan"
                    }
                    df_log = load_data(RIWAYAT_PENGGUNAAN_PATH)
                    df_log = pd.concat([df_log, pd.DataFrame([log_entry])], ignore_index=True)
                    save_data(df_log, RIWAYAT_PENGGUNAAN_PATH)
                st.success("Data penggunaan bahan kimia berhasil disimpan.")

# === Styling ===
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1581090700227-1e8e90817684");
        background-size: cover;
        background-position: center;
    }
    .css-18ni7ap, .css-1d391kg {
        background-color: rgba(255, 255, 255, 0.85) !important;
        border-radius: 10px;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
