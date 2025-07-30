# ... (semua bagian awal seperti sebelumnya: import, set page config, background, CREDENTIALS, dll)

# ========== LOGIN / REGISTER ==========
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

# ========== MENU UTAMA ==========
if login_status:
    st.success(f"Selamat datang, **{login_user}** ({login_role})")

    # Load Data
    df_bahan = pd.read_csv(STOK_BAHAN)
    df_alat = pd.read_csv(STOK_ALAT)
    df_riwayat = pd.read_csv(RIWAYAT)

    if login_role == "Laboran":
        menu = st.sidebar.selectbox("📋 Menu", [
            "Stok Bahan Kimia", "Stok Alat Laboratorium",
            "Logbook Pemakaian", "Reset Semua Data"
        ])

        if menu == "Stok Bahan Kimia":
            # Tampilkan dan tambah-hapus bahan
            # (copy paste dari logika kamu sebelumnya)
            pass

        elif menu == "Stok Alat Laboratorium":
            # Tampilkan dan tambah-hapus alat
            pass

        elif menu == "Logbook Pemakaian":
            # Tampilkan logbook
            pass

        elif menu == "Reset Semua Data":
            # Reset data
            pass

    elif login_role in ["Mahasiswa", "Dosen"]:
        menu = st.sidebar.selectbox("📋 Menu", [
            "Stok Bahan Kimia", "Stok Alat Laboratorium",
            "Isi Logbook Pemakaian"
        ])

        if menu == "Stok Bahan Kimia":
            # Tampilkan bahan
            pass

        elif menu == "Stok Alat Laboratorium":
            # Tampilkan alat
            pass

        elif menu == "Isi Logbook Pemakaian":
            sub_menu = st.radio("Pilih Jenis Logbook", ["Penggunaan Bahan Kimia", "Peminjaman & Pengembalian Alat"])
            if sub_menu == "Penggunaan Bahan Kimia":
                # Form catat penggunaan bahan
                pass
            elif sub_menu == "Peminjaman & Pengembalian Alat":
                # Form pinjam/kembalikan alat
                pass

else:
    st.warning("Silakan login terlebih dahulu untuk mengakses.")
