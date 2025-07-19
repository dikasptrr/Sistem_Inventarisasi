import streamlit as st
import pandas as pd
import os
from datetime import date

# ==== Konstanta path CSV ====
BAHAN_CSV = "stok_bahan.csv"
ALAT_CSV = "stok_alat.csv"
RIWAYAT_CSV = "riwayat_penggunaan.csv"

# ==== Inisialisasi data jika belum ada ====
def init_csv():
    if not os.path.exists(BAHAN_CSV):
        pd.DataFrame(columns=["Nama", "Jumlah", "Satuan", "Tempat Penyimpanan", "Tanggal Expired"]).to_csv(BAHAN_CSV, index=False)
    if not os.path.exists(ALAT_CSV):
        pd.DataFrame(columns=["Nama", "Jumlah", "Satuan"]).to_csv(ALAT_CSV, index=False)
    if not os.path.exists(RIWAYAT_CSV):
        pd.DataFrame(columns=["Nama Barang", "Kategori", "Jumlah", "Tanggal", "Pengguna", "Keterangan"]).to_csv(RIWAYAT_CSV, index=False)

# ==== Load Data ====
def load_data():
    df_bahan = pd.read_csv(BAHAN_CSV)
    df_alat = pd.read_csv(ALAT_CSV)
    df_riwayat = pd.read_csv(RIWAYAT_CSV)
    return df_bahan, df_alat, df_riwayat

# ==== Save Data ====
def save_data(df_bahan, df_alat, df_riwayat):
    df_bahan.to_csv(BAHAN_CSV, index=False)
    df_alat.to_csv(ALAT_CSV, index=False)
    df_riwayat.to_csv(RIWAYAT_CSV, index=False)

# ==== Reset Semua Data ====
def clear_all_data():
    for file in [BAHAN_CSV, ALAT_CSV, RIWAYAT_CSV]:
        if os.path.exists(file):
            os.remove(file)
    init_csv()

# ==== UI Styling ====
def apply_style():
    st.markdown("""
        <style>
        .stApp {
            background-image: url('https://images.unsplash.com/photo-1581090700227-1e8e908976d2');
            background-size: cover;
        }
        .css-1v0mbdj, .stButton button {
            background-color: #4CAF50;
            color: white;
            border: none;
        }
        .stButton button:hover {
            background-color: #45a049;
        }
        </style>
    """, unsafe_allow_html=True)

# ==== App Utama ====
def main():
    st.set_page_config(page_title="Inventarisasi Lab Kimia", layout="wide")
    apply_style()
    init_csv()
    df_bahan, df_alat, df_riwayat = load_data()

    # Sidebar: Login & Navigasi
    st.sidebar.title("🔐 Login Pengguna")
    role = st.sidebar.selectbox("Pilih Peran", ["Mahasiswa", "Dosen", "Laboran"])
    nama_pengguna = st.sidebar.text_input("Nama Pengguna")

    st.sidebar.markdown("📝 **Menu**")
    menu = []
    if role == "Laboran":
        menu = ["Kelola Stok Bahan", "Kelola Stok Alat", "Lihat Logbook", "Clear Semua Data"]
    else:
        menu = ["Isi Logbook Pemakaian"]

    sub_menu = st.sidebar.selectbox("Pilih Menu", menu)

    # ========== Tampilan Menu ==========
    if sub_menu == "Kelola Stok Bahan":
        st.title("🧪 Kelola Stok Bahan Kimia")
        st.dataframe(df_bahan, use_container_width=True)

        with st.expander("➕ Tambah Bahan Kimia"):
            nama = st.text_input("Nama Bahan")
            jumlah = st.number_input("Jumlah", min_value=0.0, format="%.2f")
            satuan = st.selectbox("Satuan", ["g", "mL"])
            tempat = st.text_input("Tempat Penyimpanan")
            expired = st.date_input("Tanggal Expired")

            if st.button("Tambah Bahan"):
                if nama and tempat:
                    new_data = pd.DataFrame([[nama, jumlah, satuan, tempat, expired]],
                                            columns=df_bahan.columns)
                    df_bahan = pd.concat([df_bahan, new_data], ignore_index=True)
                    save_data(df_bahan, df_alat, df_riwayat)
                    st.success("✅ Bahan kimia berhasil ditambahkan.")
                else:
                    st.warning("Harap lengkapi semua kolom.")

    elif sub_menu == "Kelola Stok Alat":
        st.title("🔧 Kelola Stok Alat Laboratorium")
        st.dataframe(df_alat, use_container_width=True)

        with st.expander("➕ Tambah Alat"):
            nama = st.text_input("Nama Alat")
            jumlah = st.number_input("Jumlah", min_value=1, step=1)
            satuan = "buah"

            if st.button("Tambah Alat"):
                if nama:
                    if nama in df_alat["Nama"].values:
                        idx = df_alat[df_alat["Nama"] == nama].index[0]
                        df_alat.at[idx, "Jumlah"] += jumlah
                    else:
                        new_data = pd.DataFrame([[nama, jumlah, satuan]], columns=df_alat.columns)
                        df_alat = pd.concat([df_alat, new_data], ignore_index=True)
                    save_data(df_bahan, df_alat, df_riwayat)
                    st.success("✅ Alat berhasil ditambahkan atau diperbarui.")
                else:
                    st.warning("Harap isi nama alat.")

    elif sub_menu == "Lihat Logbook":
        st.title("📚 Riwayat Logbook Penggunaan")
        st.dataframe(df_riwayat, use_container_width=True)

    elif sub_menu == "Clear Semua Data":
        if st.button("🗑️ Hapus Semua Data"):
            clear_all_data()
            st.success("✅ Semua data berhasil dihapus.")
    
    elif sub_menu == "Isi Logbook Pemakaian":
        jenis_log = st.radio("Pilih Jenis Logbook", ["Penggunaan Bahan Kimia", "Peminjaman & Pengembalian Alat"])

        if jenis_log == "Penggunaan Bahan Kimia":
            st.title("🧪 Penggunaan Bahan Kimia")
            if not df_bahan.empty:
                nama = st.text_input("Masukkan Nama Anda", value=nama_pengguna)
                bahan = st.selectbox("Pilih Bahan", df_bahan["Nama"].unique())
                jumlah = st.number_input("Jumlah (g/mL)", min_value=0.0, format="%.2f")
                tanggal = st.date_input("Tanggal", value=date.today())
                keterangan = st.text_area("Keterangan")

                if st.button("Simpan Penggunaan"):
                    idx = df_bahan[df_bahan["Nama"] == bahan].index[0]
                    if df_bahan.at[idx, "Jumlah"] >= jumlah:
                        df_bahan.at[idx, "Jumlah"] -= jumlah
                        log = pd.DataFrame([[bahan, "Bahan", jumlah, tanggal, nama, keterangan]],
                                           columns=df_riwayat.columns)
                        df_riwayat = pd.concat([df_riwayat, log], ignore_index=True)
                        save_data(df_bahan, df_alat, df_riwayat)
                        st.success(f"✅ Penggunaan {bahan} tercatat oleh {nama}.")
                    else:
                        st.warning("Jumlah tidak mencukupi di stok.")
            else:
                st.warning("Belum ada data bahan kimia.")

        elif jenis_log == "Peminjaman & Pengembalian Alat":
            st.title("🔄 Peminjaman & Pengembalian Alat")
            if not df_alat.empty:
                nama = st.text_input("Masukkan Nama Anda", value=nama_pengguna)
                selected_items = st.multiselect("Pilih Alat", df_alat["Nama"].unique())

                jumlah_dict = {}
                for alat in selected_items:
                    jumlah_dict[alat] = st.number_input(f"Jumlah untuk {alat}", min_value=1, step=1, key=f"{alat}_jumlah")

                aksi = st.radio("Aksi", ["Pinjam", "Kembalikan"])
                tanggal = st.date_input("Tanggal", value=date.today())
                keterangan = st.text_area("Keterangan")

                if st.button("Simpan Log"):
                    success = []
                    for alat in selected_items:
                        jumlah = jumlah_dict[alat]
                        idx = df_alat[df_alat["Nama"] == alat].index[0]

                        if aksi == "Pinjam":
                            if df_alat.at[idx, "Jumlah"] >= jumlah:
                                df_alat.at[idx, "Jumlah"] -= jumlah
                            else:
                                st.warning(f"Jumlah {alat} tidak mencukupi.")
                                continue
                        else:
                            df_alat.at[idx, "Jumlah"] += jumlah

                        log = pd.DataFrame([[alat, "Alat", jumlah, tanggal, nama, f"{aksi}: {keterangan}"]],
                                           columns=df_riwayat.columns)
                        df_riwayat = pd.concat([df_riwayat, log], ignore_index=True)
                        success.append(alat)

                    if success:
                        save_data(df_bahan, df_alat, df_riwayat)
                        st.success(f"✅ Berhasil mencatat {aksi.lower()} alat: {', '.join(success)} oleh {nama}.")
            else:
                st.warning("Belum ada data alat.")
