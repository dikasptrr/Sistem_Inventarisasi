import streamlit as st
import pandas as pd
import os
from datetime import datetime

# File penyimpanan
FILE_BAHAN = "bahan_kimia.csv"
FILE_RIWAYAT = "riwayat_pemakaian.csv"

# Fungsi load data
def load_data(file, columns):
    if os.path.exists(file):
        return pd.read_csv(file)
    else:
        return pd.DataFrame(columns=columns)

# Fungsi save data
def save_data(df, file):
    df.to_csv(file, index=False)

# Fungsi cek kelayakan bahan
def cek_kelayakan(sisa, expired):
    try:
        expired_date = datetime.strptime(expired, "%Y-%m-%d").date()
        if sisa > 0 and datetime.today().date
