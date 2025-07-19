import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Konfigurasi halaman
st.set_page_config(page_title="Inventarisasi Lab Kimia", page_icon="🧪", layout="wide")

# Styling
st.markdown("""
    <style>
        [data-testid="stAppViewContainer"] {
            background-image: url("https://images.unsplash.com/photo-1581092580502-3d5c3c9e1cfa");
            background-size: cover;
        }
        [data-testid="stSidebar"] {
            background-color: rgba(255, 255, 255, 0.85);
        }
        h1, h2, h3 {
            color: #003366;
        }
        .stButton>button {
            background-color: #006699;
            color: white;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Path file
DATA_FOLDER = "data"
os.makedirs(DATA_FOLDER, exist_ok=True)
STOK_BAHAN = os.path.join(DATA_FOLDER, "stok_bahan.csv")
STOK_ALAT = os.path.join(DATA_FOLDER, "stok_alat.csv")
RIWAYAT = os.path.join(DATA_FOLDER, "riwayat_penggunaan.csv")

# Inisialisasi file
def initialize_file(path, columns):
    if not os.path.exists(path):
        pd.DataFrame(columns=columns).to_csv(path, index=False)

initialize_file(STOK_BAHAN, ["Nama", "Jumlah", "Satuan", "Tempat Penyimpanan", "Tanggal Expired"])
initialize_file(STOK_ALAT, ["Nama", "Jumlah", "Lokasi"])
initialize_file(RIWAYAT, ["Nama", "Kategori", "Jumlah", "Tanggal", "Pengguna", "Keterangan"])

# Load data
def load_data():
    return pd.read_csv(STOK_BAHAN), pd.read_csv(STOK_ALAT), pd.read_csv(RIWAYAT)

def save_data(df_bahan, df_alat, df_riwayat):
    df_bahan.to_csv(STOK_BAHAN, index=False)
    df_alat.to_csv(STOK_ALAT, index=False)
    df_riwayat.to_csv(RIWAYAT, index=False)

# Login di sidebar
st.sidebar.title("🔑 Login Pengguna")
role = st.sidebar.selectbox("Pilih Peran", ["Mahasiswa", "Dosen", "Laboran"])
pengguna = st.sidebar.text_input("Nama Pengguna")

# Load data
df_bahan, df_alat, df_riwayat = load_data()

# LABORAN
if role == "Laboran":
    menu = st.sidebar.selectbox("📋 Menu", ["Stok Bahan Kimia", "Stok Alat Laboratorium", "Logbook Pemakaian"])

    if menu == "Stok Bahan Kimia":
        st.title("📦 Stok Bahan Kimia")
        df_display = df_bahan.copy().reset_index(drop=True)
        df_display.index += 1
        df_display.index.name = "No"
        st.dataframe(df_display)

        st.subheader("Tambah / Hapus Bahan")
        nama = st.text_input("Nama Bahan")
        jumlah = st.number_input("Jumlah", min_value=0.0)
        satuan = st.selectbox("Satuan", ["g", "ml"])
        tempat = st.text_input("Tempat Penyimpanan")
        expired = st.date_input("Tanggal Expired")

        if st.button("Tambah Bahan"):
            if nama:
                new = pd.DataFrame([[nama, jumlah, satuan, tempat, expired]], columns=df_bahan.columns)
                df_bahan = pd.concat([df_bahan, new], ignore_index=True)
                save_data(df_bahan, df_alat, df_riwayat)
                st.success("✅ Bahan berhasil ditambahkan.")

        if st.button("Hapus Bahan"):
            df_bahan = df_bahan[df_bahan["Nama"] != nama]
            save_data(df_bahan, df_alat, df_riwayat)
            st.success("🗑️ Bahan berhasil dihapus.")

    elif menu == "Stok Alat Laboratorium":
        st.title("🔧 Stok Alat Laboratorium")
        df_display = df_alat.copy().reset_index(drop=True)
        df_display.index += 1
        df_display.index.name = "No"
        st.dataframe(df_display)

        st.subheader("Tambah / Hapus Alat")
        nama = st.text_input("Nama Alat")
        jumlah = st.number_input("Jumlah", min_value=0, step=1)
        lokasi = st.text_input("Lokasi")

        if st.button("Tambah Alat"):
            if nama:
                if nama in df_alat["Nama"].values:
                    idx = df_alat[df_alat["Nama"] == nama].index[0]
                    df_alat.at[idx, "Jumlah"] += jumlah
                else:
                    new = pd.DataFrame([[nama, jumlah, lokasi]], columns=df_alat.columns)
                    df_alat = pd.concat([df_alat, new], ignore_index=True)
                save_data(df_bahan, df_alat, df_riwayat)
                st.success("✅ Alat berhasil ditambahkan atau diperbarui.")

        if st.button("Hapus Alat"):
            df_alat = df_alat[df_alat["Nama"] != nama]
            save_data(df_bahan, df_alat, df_riwayat)
            st.success("🗑️ Alat berhasil dihapus.")

    elif menu == "Logbook Pemakaian":
        st.title("📘 Logbook Pemakaian")
        if df_riwayat.empty:
            st.info("Belum ada catatan.")
        else:
            df_display = df_riwayat.copy()
            df_display = df_display.rename(columns={"Pengguna": "Nama Pengguna"})
            df_display = df_riwayat.copy().reset_index(drop=True)
            df_display.index += 1
            df_display.index.name = "No"
            st.dataframe(df_display)

# MAHASISWA & DOSEN
elif role in ["Mahasiswa", "Dosen"]:
    menu = st.sidebar.selectbox("📋 Menu", ["Stok Bahan Kimia", "Stok Alat Laboratorium", "Isi Logbook Pemakaian"])

    if menu == "Stok Bahan Kimia":
        st.title("📦 Stok Bahan Kimia")
        df_display = df_bahan.copy().reset_index(drop=True)
        df_display.index += 1
        df_display.index.name = "No"
        st.dataframe(df_display)

    elif menu == "Stok Alat Laboratorium":
        st.title("🔧 Stok Alat Laboratorium")
        df_display = df_alat.copy().reset_index(drop=True)
        df_display.index += 1
        df_display.index.name = "No"
        st.dataframe(df_display)

    elif menu == "Isi Logbook Pemakaian":
        sub_menu = st.radio("Pilih Jenis Logbook", ["Penggunaan Bahan Kimia", "Peminjaman & Pengembalian Alat"])

        if sub_menu == "Penggunaan Bahan Kimia":
            st.title("🧪 Logbook Penggunaan Bahan Kimia")
            if not df_bahan.empty:
                pengguna = st.text_input("Masukkan Nama Anda")
                nama = st.selectbox("Pilih Bahan", df_bahan["Nama"].unique())
                jumlah = st.number_input("Jumlah", min_value=0.01, step=0.01)
                satuan = st.selectbox("Satuan", ["g", "ml"])
                tanggal = st.date_input("Tanggal")
                keterangan = st.text_area("Keterangan")

                if st.button("Catat Penggunaan"):
                    if nama and pengguna:
                        new = pd.DataFrame([[nama, "Bahan", f"{jumlah} {satuan}", tanggal, pengguna, keterangan]],
                                   columns=df_riwayat.columns)
                        df_riwayat = pd.concat([df_riwayat, new], ignore_index=True)
                        save_data(df_bahan, df_alat, df_riwayat)
                        st.success(f"✅ Penggunaan dicatat oleh **{pengguna}**.")
                    else:
                        st.error("⚠️ Lengkapi semua data.")
                        
                elif sub_menu == "Peminjaman & Pengembalian Alat":
                    st.title("🔄 Peminjaman & Pengembalian Alat")
                    if not df_alat.empty:
                        pengguna = st.text_input("Masukkan Nama Anda")
                        selected_items = st.multiselect("Pilih Alat", df_alat["Nama"].unique())

                        jumlah_dict = {}
                        for item in selected_items:
                            jumlah = st.number_input(f"Jumlah untuk {item}", min_value=1, step=1, key=item)
                            jumlah_dict[item] = jumlah
                            aksi = st.radio("Aksi", ["Pinjam", "Kembalikan"])
                            tanggal = st.date_input("Tanggal")
                            keterangan = st.text_area("Keterangan")

                        if st.button("Simpan Log"):
                            success_log = []
                            for alat in selected_items:
                                jumlah = jumlah_dict[alat]
                                idx = df_alat[df_alat["Nama"] == alat].index[0]

                                if aksi == "Pinjam":
                                    if df_alat.at[idx, "Jumlah"] >= jumlah:
                                        df_alat.at[idx, "Jumlah"] -= jumlah
                                    else:
                                        st.error(f"Jumlah alat '{alat}' tidak mencukupi.")
                                        continue
                                elif aksi == "Kembalikan":
                                    df_alat.at[idx, "Jumlah"] += jumlah

                                # Catat log
                                log = pd.DataFrame([[alat, "Alat", jumlah, tanggal, pengguna, f"{aksi}: {keterangan}"]],
                                           columns=df_riwayat.columns)
                                df_riwayat = pd.concat([df_riwayat, log], ignore_index=True)
                                success_log.append(alat)

                             if success_log:
                                save_data(df_bahan, df_alat, df_riwayat)
                                st.success(f"✅ Berhasil {aksi.lower()} alat: {', '.join(success_log)} oleh **{pengguna}**.")
                    else:
                        st.warning("Belum ada data alat.")
