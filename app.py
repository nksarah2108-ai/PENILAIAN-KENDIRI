import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# ==============================
# GOOGLE SHEET CONNECTION
# ==============================

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
    "service_account.json",
    scopes=scope
)

client = gspread.authorize(creds)

spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1bnVFcZk0A8QikZGUI_Q2sknRSkHWCKxf_IZXWgwOu2Y/edit")
sheet = spreadsheet.worksheet("RESPON_GURU")

# ==============================
# AMBIL NAMA YANG DAH ISI
# ==============================

data = sheet.get_all_records()
nama_dah_isi = [row["Nama"] for row in data]

# ==============================
# SENARAI 37 GURU (GANTI DENGAN NAMA SEBENAR)
# ==============================

senarai_guru = [
    "Guru 1","Guru 2","Guru 3","Guru 4","Guru 5",
    "Guru 6","Guru 7","Guru 8","Guru 9","Guru 10",
    "Guru 11","Guru 12","Guru 13","Guru 14","Guru 15",
    "Guru 16","Guru 17","Guru 18","Guru 19","Guru 20",
    "Guru 21","Guru 22","Guru 23","Guru 24","Guru 25",
    "Guru 26","Guru 27","Guru 28","Guru 29","Guru 30",
    "Guru 31","Guru 32","Guru 33","Guru 34","Guru 35",
    "Guru 36","Guru 37"
]

guru_available = [g for g in senarai_guru if g not in nama_dah_isi]

# ==============================
# UI
# ==============================

st.title("BORANG PENILAIAN KENDIRI STANDARD 4")

if len(guru_available) == 0:
    st.success("Semua guru telah mengisi borang.")
    st.stop()

nama = st.selectbox("Nama Guru", guru_available)
tarikh = st.date_input("Tarikh", datetime.today())
mpel = st.text_input("Mata Pelajaran")
kelas = st.text_input("Kelas")

st.subheader("Skor (1 - 4)")

def skor(label):
    return st.selectbox(label, [1,2,3,4], key=label)

item_list = [
"4.1.1a","4.1.1b","4.1.1c",
"4.2.1a","4.2.1b","4.2.1c",
"4.2.2a","4.2.2b","4.2.2c","4.2.2d",
"4.3.1a","4.3.1b","4.3.1c","4.3.1d","4.3.1e",
"4.4.1a","4.4.1b","4.4.1c","4.4.1d","4.4.1e","4.4.1f","4.4.1g",
"4.4.2a","4.4.2b","4.4.2c","4.4.2d",
"4.5.1a","4.5.1b","4.5.1c","4.5.1d","4.5.1e",
"4.6.1a","4.6.1b","4.6.1c","4.6.1d","4.6.1e","4.6.1f","4.6.1g"
]

skor_data = []

for item in item_list:
    skor_data.append(skor(item))

# ==============================
# SUBMIT BUTTON
# ==============================

if st.button("HANTAR"):
    new_row = [
        nama,
        tarikh.strftime("%d-%m-%Y"),
        mpel,
        kelas
    ] + skor_data + ["","",""]

    sheet.append_row(new_row)

    st.success("Data berjaya dihantar!")
    st.rerun()
