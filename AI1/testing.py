#untuk menguji dan merekam kinerja sistem tanya-jawab yang telah dibangun sebelumnya.

# Import modul dan library yang dibutuhkan
from iteung import reply #Mengimpor sebuah modul atau fungsi bernama reply dari sebuah paket atau modul yang disebut iteung. Ini berarti kode di dalam file iteung memiliki sebuah fungsi atau modul yang bernama reply, yang ingin digunakan di sini.
import pandas as pd #untuk bekerja dengan data dalam bentuk DataFrame, yang mirip dengan tabel dalam basis data.
import os #untuk berinteraksi dengan sistem operasi di mana program berjalan.

# Inisialisasi path untuk file Excel dan variabel pengecekan keberadaan file
file_path = "akurasi50.xlsx"
adaFile = False

# Inisialisasi list untuk menyimpan jawaban, akurasi, dan pertanyaan
listJawaban = []
listPertanyaan = []

# Pengecekan keberadaan file Excel
if os.path.exists(file_path):
    print("File Excel ada.")
    try:
        # Membaca data dari file Excel jika file tersebut ada
        data = pd.read_excel(file_path)
        # Mengambil data dari kolom yang ditentukan
        listJawaban = data["Jawaban"].tolist()
        listPertanyaan = data["Pertanyaan"].tolist()
        adaFile = True
    except pd.errors.EmptyDataError:
        print("File Excel Kosong.")
else:
    print("File Excel tidak ada.")

# Loop utama untuk interaksi dengan pengguna
while True:
    # Menerima input dari pengguna
    message = input("Kamu: ")
    
    # Keluar dari loop jika pengguna memasukkan "exit"
    if message == "exit":
        break

    # Memanggil fungsi botReply dari modul reply untuk mendapatkan jawaban
    return_message, akurasi = reply.botReply(message)

    # Menambahkan jawaban, akurasi, dan pertanyaan ke dalam list
    listJawaban.append(return_message)
    listPertanyaan.append(message)

    # Menampilkan jawaban dari ITeung
    print(f"ITeung: {return_message}")

    # Membuat DataFrame baru dari list yang telah diupdate
    df = pd.DataFrame({
        'Pertanyaan': listPertanyaan,
        'Jawaban': listJawaban,
    })

    # Jika file Excel sudah ada sebelumnya
    if adaFile:
        try:
            # Menyimpan DataFrame ke dalam file Excel tanpa menyertakan indeks
            df.to_excel(file_path, index=False)
        except PermissionError:
            print("File Excel sedang dibuka. Tutup file tersebut dan coba lagi.")
    # Jika file Excel belum ada
    else:
        # Menyimpan DataFrame ke dalam file Excel tanpa menyertakan indeks
        df.to_excel(file_path, index=False)