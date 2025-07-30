import streamlit as st
import pandas as pd
import os
from datetime import date
import base64

# ========== KONFIGURASI ==========
st.set_page_config(page_title="Log N Stock", page_icon="📦", layout="wide")

# ========== FOLDER & FILE SETUP ==========
DATA_FOLDER = "data"
os.makedirs(DATA_FOLDER, exist_ok=True)

AKUN_PATH = os.path.join(DATA_FOLDER, "akun_pengguna.csv")
STOK_BAHAN = os.path.join(DATA_FOLDER, "stok_bahan.csv")
STOK_ALAT = os.path.join(DATA_FOLDER, "stok_alat.csv")
RIWAYAT = os.path.join(DATA_FOLDER, "riwayat_penggunaan.csv")

# Inisialisasi file akun jika belum ada
if not os.path.exists(AKUN_PATH):
    pd.DataFrame(columns=["username", "password", "role"]).to_csv(AKUN_PATH, index=False)

# Inisialisasi file stok
def initialize_file(path, columns):
    if not os.path.exists(path):
        pd.DataFrame(columns=columns).to_csv(path, index=False)

initialize_file(STOK_BAHAN, ["Nama", "Jumlah", "Satuan", "Tempat Penyimpanan", "Tanggal Expired"])
initialize_file(STOK_ALAT, ["Nama", "Jumlah", "Lokasi"])
initialize_file(RIWAYAT, ["Nama", "Kategori", "Jumlah", "Tanggal", "Pengguna", "Keterangan"])

# ========== STYLING ==========
def add_bg_from_local(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
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

add_bg_from_local("images/background_lab.jpg")

# ========== CREDENTIALS LABORAN (KHUSUS ADMIN) ==========
CREDENTIALS_LABORAN = {
    "Laboran": "lab1234",
    "Adminlab": "lab1234"
}

# ========== SIDEBAR LOGIN / REGISTER ==========
st.sidebar.title("🔐 Login Sistem")

tab = st.sidebar.radio("Pilih Menu", ["Login", "Register"])

login_status = False
login_user = None
login_role = None

if tab == "Login":
    role = st.sidebar.selectbox("Masuk Sebagai", ["Mahasiswa", "Dosen", "Laboran"])
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    login_button = st.sidebar.button("Login")

    if login_button:
        if role == "Laboran":
            if username in CREDENTIALS_LABORAN and password == CREDENTIALS_LABORAN[username]:
                login_status = True
                login_user = username
                login_role = role
            else:
                st.sidebar.error("Username atau password salah.")
        else:
            akun_df = pd.read_csv(AKUN_PATH)
            user_data = akun_df[(akun_df["username"] == username) & (akun_df["role"] == role)]
            if not user_data.empty and password == user_data.iloc[0]["password"]:
                login_status = True
                login_user = username
                login_role = role
            else:
                st.sidebar.error("Akun tidak ditemukan atau password salah.")

elif tab == "Register":
    st.sidebar.markdown("📝 Daftarkan Akun Baru")
    new_user = st.sidebar.text_input("Buat Username")
    new_pass = st.sidebar.text_input("Buat Password", type="password")
    new_role = st.sidebar.selectbox("Daftar Sebagai", ["Mahasiswa", "Dosen"])
    register_button = st.sidebar.button("Daftar")

    if register_button:
        if new_user == "" or new_pass == "":
            st.sidebar.warning("Username dan Password wajib diisi.")
        else:
            akun_df = pd.read_csv(AKUN_PATH)
            if new_user in akun_df["username"].values:
                st.sidebar.warning("Username sudah terdaftar.")
            else:
                new_data = pd.DataFrame([[new_user, new_pass, new_role]], columns=["username", "password", "role"])
                akun_df = pd.concat([akun_df, new_data], ignore_index=True)
                akun_df.to_csv(AKUN_PATH, index=False)
                st.sidebar.success(f"Akun '{new_user}' berhasil dibuat!")

# ========== JIKA LOGIN BERHASIL ==========
if login_status:
    st.success(f"Selamat datang, **{login_user}** ({login_role})")
    # 👉 Di sini kamu bisa lanjutkan ke menu utama kamu berdasarkan `login_role`
else:
    st.warning("Silakan login terlebih dahulu untuk mengakses fitur sistem.")
