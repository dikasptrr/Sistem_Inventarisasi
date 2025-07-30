import streamlit as st
import pandas as pd
import os
from datetime import datetime, date
import base64

# === Setup folder data ===
DATA_FOLDER = "data"
os.makedirs(DATA_FOLDER, exist_ok=True)
AKUN_PATH = os.path.join(DATA_FOLDER, "akun_pengguna.csv")

# === Inisialisasi file akun pengguna jika belum ada ===
if not os.path.exists(AKUN_PATH):
    akun_df = pd.DataFrame(columns=["username", "password", "role"])
    akun_df.to_csv(AKUN_PATH, index=False)

# === Akun Laboran (admin manual) ===
CREDENTIALS = {
    "laboran": "lab123",
    "admin": "admin123"
}

# === Variabel login ===
login_status = False
login_user = None
login_role = None

# === SIDEBAR: Login & Register ===
st.sidebar.header("🔐 Login Pengguna")

# --- LOGIN ---
role = st.sidebar.selectbox("Pilih Peran", ["Mahasiswa", "Dosen", "Laboran"])
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")
login_button = st.sidebar.button("Login")

# --- REGISTER ---
st.sidebar.markdown("---")
st.sidebar.markdown("📝 **Belum punya akun? Daftar di sini**")
new_user = st.sidebar.text_input("Buat Username Baru")
new_pass = st.sidebar.text_input("Buat Password Baru", type="password")
new_role = st.sidebar.selectbox("Daftar Sebagai", ["Mahasiswa", "Dosen"])
register_button = st.sidebar.button("Daftar Akun")

# === Proses LOGIN ===
if login_button:
    if role == "Laboran":
        if username in CREDENTIALS:
            if password == CREDENTIALS[username]:
                login_status = True
                login_user = username
                login_role = role
            else:
                st.sidebar.error("❌ Password salah.")
        else:
            st.sidebar.error("❌ Username tidak ditemukan.")
    else:
        akun_df = pd.read_csv(AKUN_PATH)
        user_data = akun_df[(akun_df["username"] == username) & (akun_df["role"] == role)]
        if not user_data.empty:
            if password == user_data.iloc[0]["password"]:
                login_status = True
                login_user = username
                login_role = role
            else:
                st.sidebar.error("❌ Password salah.")
        else:
            st.sidebar.error("❌ Akun tidak ditemukan.")

# === Proses REGISTER ===
if register_button:
    if new_user == "" or new_pass == "":
        st.sidebar.warning("⚠️ Username dan password tidak boleh kosong.")
    else:
        akun_df = pd.read_csv(AKUN_PATH)
        if new_user in akun_df["username"].values:
            st.sidebar.warning("⚠️ Username sudah terdaftar, silakan pilih yang lain.")
        else:
            new_entry = pd.DataFrame([[new_user, new_pass, new_role]], columns=["username", "password", "role"])
            akun_df = pd.concat([akun_df, new_entry], ignore_index=True)
            akun_df.to_csv(AKUN_PATH, index=False)
            st.sidebar.success(f"✅ Akun '{new_user}' berhasil dibuat sebagai {new_role}!")

# === Setelah login berhasil, tampilkan halaman utama ===
if login_status:
    st.success(f"Selamat datang, {login_user} ({login_role})!")
    # ... tampilkan menu utama sesuai peran ...
    # Tambahkan kode lanjutan Anda di sini berdasarkan peran
else:
    st.warning("Silakan login terlebih dahulu untuk mengakses sistem.")


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
             background-position: center;
         }}
         </style>
         """,
        unsafe_allow_html=True
    )

add_bg_from_local("images/background_lab.jpg")

# ========== KONFIGURASI ==========
st.set_page_config(page_title="Log N Stock", page_icon="📦", layout="wide")

# ========== KONFIGURASI USERNAME & PASSWORD LABORAN ==========
CREDENTIALS = {
    # username: password
    "Laboran": "lab1234",
    "Adminlab": "lab1234"
}

# === STYLING BARU ===
# Atur gaya visual
st.markdown(
    """
    <style>
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.85);
        color: black;
    }

    /* Selectbox, textinput, etc. */
    .stSelectbox > div, .stTextInput > div, .stNumberInput > div, .stDateInput > div, .stTextArea > div {
        background-color: white;
        color: black !important;
        border-radius: 10px;
    }
     label, .stSelectbox label, .stTextInput label, .stRadio label {
        color: #000000 !important;
        font-weight: bold;
    }
    /* Button Styling */
    button[kind="primary"] {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
    }
    button[kind="primary"]:hover {
        background-color: #45a049;
    }

    /* Title and headers */
    h1, h2, h3, h4 {
        color: #ffffff;
        text-shadow: 1px 1px 4px rgba(0,0,0,0.7);
    }

    /* Label & Radio */
    label, .stRadio > div {
        color: #ffffff !important;
        font-weight: 500;
    }

    /* Table header */
    thead tr th {
        background-color: #4CAF50 !important;
        color: white !important;
    }
    tbody tr {
        background-color: rgba(255, 255, 255, 0.9) !important;
        color: black !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# === STYLING TAMBAHAN ===
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
        div.stButton > button:hover {
            background-color: #004466;
        }
    </style>
""", unsafe_allow_html=True)

# ========== PATH FILE ==========
DATA_FOLDER = "data"
os.makedirs(DATA_FOLDER, exist_ok=True)
STOK_BAHAN = os.path.join(DATA_FOLDER, "stok_bahan.csv")
STOK_ALAT = os.path.join(DATA_FOLDER, "stok_alat.csv")
RIWAYAT = os.path.join(DATA_FOLDER, "riwayat_penggunaan.csv")

# ========== INISIALISASI ==========
def initialize_file(path, columns):
    if not os.path.exists(path):
        pd.DataFrame(columns=columns).to_csv(path, index=False)

initialize_file(STOK_BAHAN, ["Nama", "Jumlah", "Satuan", "Tempat Penyimpanan", "Tanggal Expired"])
initialize_file(STOK_ALAT, ["Nama", "Jumlah", "Lokasi"])
initialize_file(RIWAYAT, ["Nama", "Kategori", "Jumlah", "Tanggal", "Pengguna", "Keterangan"])

# ========== LOAD & SAVE ==========
def load_data():
    df_bahan = pd.read_csv(STOK_BAHAN)
    df_bahan["Jumlah"] = df_bahan["Jumlah"].astype(float)
    df_alat = pd.read_csv(STOK_ALAT)
    df_alat["Jumlah"] = df_alat["Jumlah"].astype(int)
    df_riwayat = pd.read_csv(RIWAYAT)
    return df_bahan, df_alat, df_riwayat

def save_data(df_bahan, df_alat, df_riwayat):
    df_bahan.to_csv(STOK_BAHAN, index=False)
    df_alat.to_csv(STOK_ALAT, index=False)
    df_riwayat.to_csv(RIWAYAT, index=False)

# ========== LOGIN ==========
st.sidebar.title("🔑 Login Pengguna")
role = st.sidebar.selectbox("Pilih Peran", ["Mahasiswa", "Dosen", "Laboran"])
pengguna = st.sidebar.text_input("Nama Pengguna")

# Jika Laboran, minta password
if role == "Laboran":
    password = st.sidebar.text_input("Password", type="password")
else:
    password = None

# Validasi input login
if not pengguna:
    st.sidebar.warning("⚠️ Masukkan nama pengguna terlebih dahulu.")
    st.stop()

# Validasi password khusus Laboran
if role == "Laboran":
    if pengguna not in CREDENTIALS:
        st.sidebar.error("❌ Username tidak ditemukan.")
        st.stop()
    elif CREDENTIALS[pengguna] != password:
        st.sidebar.error("❌ Password salah.")
        st.stop()


# ========== LOAD DATA ==========
df_bahan, df_alat, df_riwayat = load_data()

# ========== MENU ==========
if role == "Laboran":
    menu = st.sidebar.selectbox("📋 Menu", ["Stok Bahan Kimia", "Stok Alat Laboratorium", "Logbook Pemakaian", "Reset Semua Data"])

    if menu == "Stok Bahan Kimia":
        st.title(":package: Stok Bahan Kimia")
        df_display = df_bahan.copy().reset_index(drop=True)
        df_display.index += 1
        df_display.index.name = "No"
        st.dataframe(df_display)

        st.subheader("Tambah / Hapus Bahan")
        nama = st.text_input("Nama Bahan")
        jumlah = st.number_input("Jumlah", min_value=0.0)
        satuan = st.selectbox("Satuan", ["g", "mL"])
        tempat = st.text_input("Tempat Penyimpanan")
        expired = st.date_input("Tanggal Expired", value=date.today())

        if st.button("Tambah Bahan"):
            if not nama or jumlah == 0 or not tempat:
                st.warning("❗ Harap lengkapi semua kolom terlebih dahulu.")
            else:
                if nama in df_bahan["Nama"].values:
                    idx = df_bahan[df_bahan["Nama"] == nama].index[0]
                    df_bahan.at[idx, "Jumlah"] += jumlah
                else:
                    new = pd.DataFrame([[nama, jumlah, satuan, tempat, expired]], columns=df_bahan.columns)
                    df_bahan = pd.concat([df_bahan, new], ignore_index=True)
                save_data(df_bahan, df_alat, df_riwayat)
                st.success("✅ Bahan berhasil ditambahkan atau diperbarui.")


        if st.button("Hapus Bahan"):
            df_bahan = df_bahan[df_bahan["Nama"] != nama]
            save_data(df_bahan, df_alat, df_riwayat)
            st.success("🗑️ Bahan berhasil dihapus.")

    elif menu == "Stok Alat Laboratorium":
        st.title(":wrench: Stok Alat Laboratorium")
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
        st.title(":blue_book: Logbook Pemakaian")
        
        if df_riwayat.empty:
            st.info("Belum ada catatan.")
        else:
            kategori_terpilih = st.selectbox("Pilih Kategori", ["Semua", "Penggunaan Bahan Kimia", "Peminjaman Alat", "Pengembalian Alat"])
            
            df_display = df_riwayat.copy()
            if kategori_terpilih != "Semua":
                df_display = df_display[df_display["Kategori"] == kategori_terpilih]
        
            df_display = df_display.reset_index(drop=True)
            df_display.index += 1
            df_display.index.name = "No"

            kolom_utama = ["Nama", "Kategori", "Jumlah", "Tanggal", "Pengguna", "Keterangan"]
            df_display = df_display[kolom_utama]
            st.dataframe(df_display)

    elif menu == "Reset Semua Data":
        st.title("🧹 Reset Semua Data")
        st.warning("⚠️ Tindakan ini akan menghapus **seluruh data bahan, alat, dan logbook** secara permanen.")
        konfirmasi = st.checkbox("Saya mengerti dan ingin menghapus semua data.")

        if konfirmasi and st.button("Hapus Sekarang"):
            df_bahan = pd.DataFrame(columns=df_bahan.columns)
            df_alat = pd.DataFrame(columns=df_alat.columns)
            df_riwayat = pd.DataFrame(columns=df_riwayat.columns)
            save_data(df_bahan, df_alat, df_riwayat)
            st.success("✅ Semua data berhasil direset.")


elif role in ["Mahasiswa", "Dosen"]:
    menu = st.sidebar.selectbox("📋 Menu", ["Stok Bahan Kimia", "Stok Alat Laboratorium", "Isi Logbook Pemakaian"])

    if menu == "Stok Bahan Kimia":
        st.title(":package: Stok Bahan Kimia")
        df_display = df_bahan.copy().reset_index(drop=True)
        df_display.index += 1
        df_display.index.name = "No"
        st.dataframe(df_display)

    elif menu == "Stok Alat Laboratorium":
        st.title(":wrench: Stok Alat Laboratorium")
        df_display = df_alat.copy().reset_index(drop=True)
        df_display.index += 1
        df_display.index.name = "No"
        st.dataframe(df_display)

    elif menu == "Isi Logbook Pemakaian":
        sub_menu = st.radio("Pilih Jenis Logbook", ["Penggunaan Bahan Kimia", "Peminjaman & Pengembalian Alat"])

        if sub_menu == "Penggunaan Bahan Kimia":
            st.title(":test_tube: Logbook Penggunaan Bahan Kimia")
            if not df_bahan.empty:
                nama = st.selectbox("Pilih Bahan", df_bahan["Nama"].unique())
                kategori = "Penggunaan Bahan Kimia"
                jumlah = st.number_input("Jumlah", min_value=0.01, step=0.01)
                satuan = st.selectbox("Satuan", ["g", "mL"])
                tanggal = st.date_input("Tanggal", value=date.today())
                keterangan = st.text_area("Keterangan")

                if st.button("Catat Penggunaan"):
                    idx = df_bahan[df_bahan["Nama"] == nama].index[0]
                    stok_saat_ini = df_bahan.at[idx, "Jumlah"]

                    if stok_saat_ini >= jumlah:
                        df_bahan.at[idx, "Jumlah"] -= jumlah
                        new = pd.DataFrame([[nama, kategori, f"{jumlah} {satuan}", tanggal, pengguna, keterangan]],
                                           columns=["Nama", "Kategori", "Jumlah", "Tanggal", "Pengguna", "Keterangan"])
                        df_riwayat = pd.concat([df_riwayat, new], ignore_index=True)
                        save_data(df_bahan, df_alat, df_riwayat)
                        st.success(f"✅ Penggunaan dicatat oleh **{pengguna}**. Stok otomatis berkurang.")
                    else:
                        st.error(f"⚠️ Stok '{nama}' tidak mencukupi. Tersedia hanya {stok_saat_ini} {satuan}.")

        elif sub_menu == "Peminjaman & Pengembalian Alat":
            st.title(":arrows_counterclockwise: Peminjaman & Pengembalian Alat")
            if not df_alat.empty:
                selected_items = st.multiselect("Pilih Alat", df_alat["Nama"].unique())

                jumlah_dict = {}
                for item in selected_items:
                    jumlah = st.number_input(f"Jumlah untuk {item}", min_value=1, step=1, key=item)
                    jumlah_dict[item] = jumlah

                aksi = st.radio("Aksi", ["Pinjam", "Kembalikan"])
                tanggal = st.date_input("Tanggal", value=date.today())
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

                        kategori = "Peminjaman Alat" if aksi == "Pinjam" else "Pengembalian Alat"
                        log = pd.DataFrame([[alat, kategori, jumlah, tanggal, pengguna, keterangan]],
                                           columns=["Nama", "Kategori", "Jumlah", "Tanggal", "Pengguna", "Keterangan"])
                        df_riwayat = pd.concat([df_riwayat, log], ignore_index=True)
                        success_log.append(alat)

                    if success_log:
                        save_data(df_bahan, df_alat, df_riwayat)
                        st.success(f"✅ Berhasil {aksi.lower()} alat: {', '.join(success_log)} oleh **{pengguna}**.")
                    else:
                        st.warning("Belum ada data alat.")
