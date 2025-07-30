import streamlit as st
import pandas as pd
import os
from datetime import datetime, date
import base64

# === SETUP ===
st.set_page_config(page_title="LogNStock", page_icon="📦", layout="wide")
DATA_FOLDER = "data"
os.makedirs(DATA_FOLDER, exist_ok=True)

AKUN_PATH = os.path.join(DATA_FOLDER, "akun_pengguna.csv")
STOK_BAHAN = os.path.join(DATA_FOLDER, "stok_bahan.csv")
STOK_ALAT = os.path.join(DATA_FOLDER, "stok_alat.csv")
RIWAYAT = os.path.join(DATA_FOLDER, "riwayat_penggunaan.csv")

# Inisialisasi File
def initialize_file(path, columns):
    if not os.path.exists(path):
        pd.DataFrame(columns=columns).to_csv(path, index=False)

initialize_file(AKUN_PATH, ["username", "password", "role"])
initialize_file(STOK_BAHAN, ["Nama", "Jumlah", "Satuan", "Tempat Penyimpanan", "Tanggal Expired"])
initialize_file(STOK_ALAT, ["Nama", "Jumlah", "Lokasi"])
initialize_file(RIWAYAT, ["Nama", "Kategori", "Jumlah", "Tanggal & Waktu", "Pengguna", "Keterangan"])

# CREDENTIALS khusus Laboran
CREDENTIALS_LABORAN = {
    "Laboran": "lab1234",
    "Adminlab": "lab1234"
}

# Styling Background
def add_bg_from_local(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data).decode()
    st.markdown(
        f"""
         <style>
         .stApp {{
             background-image: url("data:image/jpg;base64,{encoded}");
             background-size: cover;
             background-attachment: fixed;
         }}
         </style>
         """,
        unsafe_allow_html=True
    )

if os.path.exists("images/background_lab.jpg"):
    add_bg_from_local("images/background_lab.jpg")

# SIDEBAR: Login & Register
st.sidebar.title("🔐 Login Sistem")
tab = st.sidebar.radio("Menu", ["Login", "Register"])

login_status = False
login_user = None
login_role = None

if tab == "Login":
    role = st.sidebar.selectbox("Masuk Sebagai", ["Mahasiswa", "Dosen", "Laboran"])
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        if role == "Laboran":
            if username in CREDENTIALS_LABORAN and password == CREDENTIALS_LABORAN[username]:
                login_status = True
                login_user = username
                login_role = role
            else:
                st.sidebar.error("Username atau password salah.")
        else:
            df = pd.read_csv(AKUN_PATH)
            user = df[(df["username"] == username) & (df["role"] == role)]
            if not user.empty and password == user.iloc[0]["password"]:
                login_status = True
                login_user = username
                login_role = role
            else:
                st.sidebar.error("Akun tidak ditemukan atau password salah.")

elif tab == "Register":
    new_user = st.sidebar.text_input("Username Baru")
    new_pass = st.sidebar.text_input("Password Baru", type="password")
    new_role = st.sidebar.selectbox("Daftar Sebagai", ["Mahasiswa", "Dosen"])
    if st.sidebar.button("Daftar"):
        if new_user and new_pass:
            df = pd.read_csv(AKUN_PATH)
            if new_user in df["username"].values:
                st.sidebar.warning("Username sudah terdaftar.")
            else:
                new_data = pd.DataFrame([[new_user, new_pass, new_role]], columns=["username", "password", "role"])
                df = pd.concat([df, new_data], ignore_index=True)
                df.to_csv(AKUN_PATH, index=False)
                st.sidebar.success("Akun berhasil dibuat.")
        else:
            st.sidebar.warning("Isi semua kolom.")

# MENU UTAMA SESUDAH LOGIN
if login_status:
    st.success(f"Selamat datang, **{login_user}** ({login_role})!")

    df_bahan = pd.read_csv(STOK_BAHAN)
    df_alat = pd.read_csv(STOK_ALAT)
    df_riwayat = pd.read_csv(RIWAYAT)

    # ==== MENU LABORAN ====
    if login_role == "Laboran":
        menu = st.sidebar.selectbox("📋 Menu", ["Stok Bahan Kimia", "Stok Alat", "Logbook", "Reset Data"])

        if menu == "Stok Bahan Kimia":
            st.title("📦 Stok Bahan Kimia")
            st.dataframe(df_bahan)

            nama = st.text_input("Nama Bahan")
            jumlah = st.number_input("Jumlah", 0.0)
            satuan = st.selectbox("Satuan", ["g", "mL"])
            tempat = st.text_input("Tempat Penyimpanan")
            expired = st.date_input("Tanggal Expired")

            if st.button("Tambah Bahan"):
                if nama and tempat:
                    if nama in df_bahan["Nama"].values:
                        idx = df_bahan[df_bahan["Nama"] == nama].index[0]
                        df_bahan.at[idx, "Jumlah"] += jumlah
                    else:
                        new = pd.DataFrame([[nama, jumlah, satuan, tempat, expired]], columns=df_bahan.columns)
                        df_bahan = pd.concat([df_bahan, new], ignore_index=True)
                    df_bahan.to_csv(STOK_BAHAN, index=False)
                    st.success("Data bahan disimpan.")

            if st.button("Hapus Bahan"):
                df_bahan = df_bahan[df_bahan["Nama"] != nama]
                df_bahan.to_csv(STOK_BAHAN, index=False)
                st.success("Bahan dihapus.")

        elif menu == "Stok Alat":
            st.title("🔧 Stok Alat")
            st.dataframe(df_alat)

            nama = st.text_input("Nama Alat")
            jumlah = st.number_input("Jumlah", 0, step=1)
            lokasi = st.text_input("Lokasi")

            if st.button("Tambah Alat"):
                if nama:
                    if nama in df_alat["Nama"].values:
                        idx = df_alat[df_alat["Nama"] == nama].index[0]
                        df_alat.at[idx, "Jumlah"] += jumlah
                    else:
                        new = pd.DataFrame([[nama, jumlah, lokasi]], columns=df_alat.columns)
                        df_alat = pd.concat([df_alat, new], ignore_index=True)
                    df_alat.to_csv(STOK_ALAT, index=False)
                    st.success("Alat disimpan.")

            if st.button("Hapus Alat"):
                df_alat = df_alat[df_alat["Nama"] != nama]
                df_alat.to_csv(STOK_ALAT, index=False)
                st.success("Alat dihapus.")

        elif menu == "Logbook":
            st.title("📘 Riwayat Logbook")
            st.dataframe(df_riwayat)

        elif menu == "Reset Data":
            if st.checkbox("Saya yakin ingin menghapus semua data"):
                pd.DataFrame(columns=df_bahan.columns).to_csv(STOK_BAHAN, index=False)
                pd.DataFrame(columns=df_alat.columns).to_csv(STOK_ALAT, index=False)
                pd.DataFrame(columns=df_riwayat.columns).to_csv(RIWAYAT, index=False)
                st.success("Semua data berhasil dihapus.")

    # ==== MENU MAHASISWA / DOSEN ====
    else:
        menu = st.sidebar.selectbox("📋 Menu", ["Lihat Stok", "Isi Logbook"])

        if menu == "Lihat Stok":
            st.subheader("📦 Stok Bahan Kimia")
            st.dataframe(df_bahan)
            st.subheader("🔧 Stok Alat")
            st.dataframe(df_alat)

        elif menu == "Isi Logbook":
            sub_menu = st.radio("Jenis Logbook", ["Penggunaan Bahan", "Peminjaman / Pengembalian Alat"])

            if sub_menu == "Penggunaan Bahan":
                st.title("🧪 Penggunaan Bahan Kimia")
                nama = st.selectbox("Pilih Bahan", df_bahan["Nama"].unique())
                jumlah = st.number_input("Jumlah", 0.01, step=0.01)
                satuan = st.selectbox("Satuan", ["g", "mL"])
                tanggal = st.date_input("Tanggal", value=date.today())
                waktu = st.time_input("Waktu")
                keterangan = st.text_area("Keterangan")

                if st.button("Catat Penggunaan"):
                    idx = df_bahan[df_bahan["Nama"] == nama].index[0]
                    if df_bahan.at[idx, "Jumlah"] >= jumlah:
                        df_bahan.at[idx, "Jumlah"] -= jumlah
                        datetime_str = f"{tanggal} {waktu.strftime('%H:%M')}"
                        log = pd.DataFrame([[nama, "Penggunaan Bahan Kimia", f"{jumlah} {satuan}", datetime_str, login_user, keterangan]],
                                           columns=df_riwayat.columns)
                        df_bahan.to_csv(STOK_BAHAN, index=False)
                        df_riwayat = pd.concat([df_riwayat, log], ignore_index=True)
                        df_riwayat.to_csv(RIWAYAT, index=False)
                        st.success("Penggunaan dicatat.")
                    else:
                        st.error("Stok tidak mencukupi.")

            elif sub_menu == "Peminjaman / Pengembalian Alat":
                st.title("🔄 Peminjaman / Pengembalian Alat")
                alat = st.selectbox("Pilih Alat", df_alat["Nama"].unique())
                jumlah = st.number_input("Jumlah", 1, step=1)
                aksi = st.radio("Aksi", ["Pinjam", "Kembalikan"])
                tanggal = st.date_input("Tanggal")
                waktu = st.time_input("Waktu")
                keterangan = st.text_area("Keterangan")

                if st.button("Catat"):
                    idx = df_alat[df_alat["Nama"] == alat].index[0]
                    if aksi == "Pinjam" and df_alat.at[idx, "Jumlah"] < jumlah:
                        st.error("Jumlah tidak mencukupi untuk dipinjam.")
                    else:
                        if aksi == "Pinjam":
                            df_alat.at[idx, "Jumlah"] -= jumlah
                            kategori = "Peminjaman Alat"
                        else:
                            df_alat.at[idx, "Jumlah"] += jumlah
                            kategori = "Pengembalian Alat"

                        datetime_str = f"{tanggal} {waktu.strftime('%H:%M')}"
                        log = pd.DataFrame([[alat, kategori, jumlah, datetime_str, login_user, keterangan]],
                                           columns=df_riwayat.columns)
                        df_alat.to_csv(STOK_ALAT, index=False)
                        df_riwayat = pd.concat([df_riwayat, log], ignore_index=True)
                        df_riwayat.to_csv(RIWAYAT, index=False)
                        st.success(f"{aksi} alat dicatat.")

else:
    st.warning("🔑 Silakan login terlebih dahulu untuk mengakses sistem.")
