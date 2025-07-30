import streamlit as st
import pandas as pd
import os
from datetime import datetime, date
import base64

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
USER_FILE = os.path.join(DATA_FOLDER, "akun_pengguna.csv")

TEMPAT_PENYIMPANAN_BAHAN = ["Lemari 1", "Lemari 2", "Rak A", "Rak B"]
TEMPAT_PENYIMPANAN_ALAT = ["Gudang Alat 1", "Gudang Alat 2", "Rak Alat A", "Rak Alat B"]

# ========== INISIALISASI ==========
def initialize_file(path, columns):
    if not os.path.exists(path):
        pd.DataFrame(columns=columns).to_csv(path, index=False)

initialize_file(STOK_BAHAN, ["Nama", "Jumlah", "Satuan", "Tempat Penyimpanan", "Batch", "Tanggal Masuk", "Tanggal Expired"])
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

def load_users():
    return pd.read_csv(USER_FILE)

def save_user(username, password, role):
    df = load_users()
    if username in df['username'].values:
        return False  # Username sudah ada
    new_user = pd.DataFrame([[username, password, role]], columns=["username", "password", "role"])
    df = pd.concat([df, new_user], ignore_index=True)
    df.to_csv(USER_FILE, index=False)
    return True

# === Penambahan Akun Hardcode === 
if not os.path.exists(USER_FILE):
    df_default = pd.DataFrame([
        {"username": "laboran", "password": "lab1234", "role": "Laboran"},
        {"username": "Admin", "password": "12345", "role": "Laboran"},
        {"username": "mahasiswa", "password": "123", "role": "Mahasiswa"},
        {"username": "dosen", "password": "123", "role": "Dosen"},
    ])
    df_default.to_csv(USER_FILE, index=False)

# === Tampilan Halaman Login + Register ===
if not st.session_state.get("logged_in"):
    st.title("📦 Sistem Inventarisasi Laboratorium Kimia")
    st.markdown("---")

    menu = st.radio("Pilih Menu:", ["🔐 Login Pengguna", "👤 Register Akun Baru"])
    
    if menu == "🔐 Login Pengguna":
        st.subheader("🔐 Login Pengguna")
        username = st.text_input("Username", key="login_username").strip()
        password = st.text_input("Password", type="password", key="login_password").strip()
        role = st.selectbox("Peran", ["Mahasiswa", "Dosen", "Laboran"], key="login_role")

        if st.button("Login"):
            if not username or not password:
                st.warning("Username dan password harus diisi.")
            else:
                users = load_users()

                user_match = users[
                    (users['username'] == username) &
                    (users['password'] == password) &
                    (users['role'] == role)
                ]

                if not user_match.empty:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.role = role
                    st.success(f"Login berhasil sebagai {role}!")
                    st.rerun()
                else:
                    st.error("Username, password, atau peran salah!")

    elif menu == "👤 Register Akun Baru":
        st.subheader("👤 Register Akun Baru")
        new_username = st.text_input("Username", key="register_username")
        new_password = st.text_input("Password", type="password", key="register_password")
        new_role = st.selectbox("Peran", ["Mahasiswa", "Dosen", "Laboran"], key="register_role")

        if st.button("Register"):
            if new_username.strip() == "" or new_password.strip() == "":
                st.warning("Username dan password tidak boleh kosong.")
            else:
                if save_user(new_username, new_password, new_role):
                    st.success("Registrasi berhasil! Silakan login.")
                else:
                    st.error("Username sudah digunakan. Gunakan yang lain.")


# Setelah login berhasil, lanjutkan ke halaman utama
if st.session_state.get("logged_in"):
    role = st.session_state.get("role")
    username = st.session_state.get("username")
    st.markdown("---")
    st.success(f"Selamat datang, {username} ({role})")
    df_bahan, df_alat, df_riwayat = load_data()

# ========== MENU ==========
    if role == "Laboran":
        menu = st.sidebar.selectbox("📋 Menu", ["Stok Bahan Kimia", "Stok Alat Laboratorium", "Logbook Pemakaian", "Reset Semua Data"])

        if menu == "Stok Bahan Kimia":
            st.title(":package: Stok Bahan Kimia")
            df_display = df_bahan.copy().reset_index(drop=True)
            df_display.index += 1
            df_display.index.name = "No"
            df_display = df_display.sort_values(by=["Batch", "Tanggal Masuk"], ascending=[False, False])
            st.dataframe(df_display)

            st.subheader("Tambah / Hapus Bahan")
            nama = st.text_input("Nama Bahan")
            jumlah = st.number_input("Jumlah", min_value=0.0)
            satuan = st.selectbox("Satuan", ["g", "mL"])
            tempat = st.selectbox("Tempat Penyimpanan", TEMPAT_PENYIMPANAN_BAHAN)
            expired = st.date_input("Tanggal Expired", value=date.today())

            if st.button("Tambah Bahan"):
                if not nama or jumlah == 0 or not tempat:
                    st.warning("❗ Harap lengkapi semua kolom terlebih dahulu.")
                else:
                    # Cari batch terakhir
                    if not df_bahan.empty:
                        last_batch = df_bahan["Batch"].max() if "Batch" in df_bahan.columns else 0
                    else:
                        last_batch = 0
                    batch_number = last_batch + 1

                    tanggal_masuk = date.today()
                    new = pd.DataFrame([[nama, jumlah, satuan, tempat, expired, batch_number, tanggal_masuk]],
                                       columns=["Nama", "Jumlah", "Satuan", "Tempat Penyimpanan", "Batch", "Tanggal Masuk", "Tanggal Expired"])
                    df_bahan = pd.concat([df_bahan, new], ignore_index=True)
                    save_data(df_bahan, df_alat, df_riwayat)
                    st.success(f"✅ Bahan batch ke-{batch_number} berhasil ditambahkan.")


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
            tempat = st.selectbox("Tempat Penyimpanan", TEMPAT_PENYIMPANAN_ALAT)

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
    
