#file ini untuk Normalisasi Teks: Membersihkan teks dari tanda baca.
#Analisis Statistik Panjang Pertanyaan dan Jawaban: Menghitung panjang pertanyaan dan jawaban.

# -*- coding: utf-8 -*-
"""ITeung
# Preprocessing
"""

# Import library dan modul yang dibutuhkan
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory # melakukan stemming pada kata-kata dalam Bahasa Indonesia. Sastrawi adalah library pemrosesan bahasa alami untuk Bahasa Indonesia.
import io # manipulasi operasi file dalam memori.
import os # berinteraksi dengan sistem operasi, misalnya untuk manipulasi path file atau menjalankan perintah sistem.
import re # operasi pencarian dan manipulasi string dengan pola tertentu.
import requests # melakukan HTTP requests. Dalam konteks ini, mungkin digunakan untuk mengambil data dari internet.
import csv # membaca dan menulis file CSV.
import datetime # bekerja dengan tanggal dan waktu.
import numpy as np # untuk operasi array dan matriks.
import pandas as pd # membaca, mengolah, dan menganalisis data dalam bentuk DataFrame.
import random # operasi yang melibatkan unsur acak.
import pickle # menyimpan dan membaca objek Python dalam format yang dapat diserialisasi.

# Inisialisasi Stemmer untuk Bahasa Indonesia
factory = StemmerFactory()
stemmer = factory.create_stemmer()

# Regex untuk menghapus tanda baca
punct_re_escape = re.compile('[%s]' % re.escape('!"#$%&()*+,./:;<=>?@[\\]^_`{|}~'))

# Kata-kata tidak dikenal yang akan digunakan dalam proses normalisasi
unknowns = ["gak paham","kurang ngerti","I don't know"]

# Membaca daftar slang bahasa Indonesia dari file CSV
list_indonesia_slang = pd.read_csv('./dataset/daftar-slang-bahasa-indonesia.csv', header=None).to_numpy()

data_slang = {}
# Membuat kamus (dictionary) dari daftar slang
for key, value in list_indonesia_slang:
    data_slang[key] = value

# Fungsi untuk melakukan switch berdasarkan kamus
def dynamic_switcher(dict_data, key):
    return dict_data.get(key, None)

# Fungsi untuk memeriksa apakah suatu kata merupakan kata normal atau slang
def check_normal_word(word_input):
    slang_result = dynamic_switcher(data_slang, word_input)
    if slang_result:
        return slang_result
    return word_input

# Fungsi untuk normalisasi kalimat
def normalize_sentence(sentence):
    # Menghapus tanda baca, mengubah huruf menjadi lowercase
    sentence = punct_re_escape.sub('', sentence.lower())
    # Menghapus kata-kata tertentu dari kalimat
    sentence = sentence.replace('iteung', '').replace('\n', '').replace(' wah','').replace('wow','').replace(' dong','').replace(' sih','').replace(' deh','')
    sentence = sentence.replace('teung', '')
    sentence = re.sub(r'((wk)+(w?)+(k?)+)+', '', sentence)
    sentence = re.sub(r'((xi)+(x?)+(i?)+)+', '', sentence)
    sentence = re.sub(r'((h(a|i|e)h)((a|i|e)?)+(h?)+((a|i|e)?)+)+', '', sentence)
    sentence = ' '.join(sentence.split())
    
    if sentence:
        # Memisahkan kalimat menjadi kata-kata
        sentence = sentence.strip().split(" ")
        normal_sentence = " "
        
        # Melakukan normalisasi pada setiap kata dalam kalimat
        for word in sentence:
            normalize_word = check_normal_word(word)
            root_sentence = stemmer.stem(normalize_word)
            normal_sentence += root_sentence+" "
        
        return punct_re_escape.sub('', normal_sentence)
    
    return sentence

# Membaca data pertanyaan dan jawaban dari file CSV
df = pd.read_csv('./dataset/qa.csv', sep='|', usecols=['question', 'answer'])
df.head()

# Statistik panjang pertanyaan
question_length = {}
# Statistik panjang jawaban
answer_length = {}

# Iterasi melalui setiap baris data
for index, row in df.iterrows():
    # Normalisasi kalimat pertanyaan
    question = normalize_sentence(row['question'])
    question = normalize_sentence(question)
    question = stemmer.stem(question)

    # Menghitung panjang pertanyaan dan jawaban
    if question_length.get(len(question.split())):
        question_length[len(question.split())] += 1
    else:
        question_length[len(question.split())] = 1

    if answer_length.get(len(str(row['answer']).split())):
        answer_length[len(str(row['answer']).split())] += 1
    else:
        answer_length[len(str(row['answer']).split())] = 1

# Menampilkan statistik panjang pertanyaan
question_length

# Menampilkan statistik panjang jawaban
answer_length

# Konversi statistik panjang pertanyaan ke dalam DataFrame
val_question_length = list(question_length.values())
key_question_length = list(question_length.keys())
key_val_question_length = list(zip(key_question_length, val_question_length))
df_question_length = pd.DataFrame(key_val_question_length, columns=['length_data', 'total_sentences'])
df_question_length.sort_values(by=['length_data'], inplace=True)
df_question_length.describe()

# Konversi statistik panjang jawaban ke dalam DataFrame
val_answer_length = list(answer_length.values())
key_answer_length = list(answer_length.keys())
key_val_answer_length = list(zip(key_answer_length, val_answer_length))
df_answer_length = pd.DataFrame(key_val_answer_length, columns=['length_data', 'total_sentences'])
df_answer_length.sort_values(by=['length_data'], inplace=True)
df_answer_length.describe()

data_length = 0

# Menulis data hasil preprocessing ke dalam file txt
filename= './dataset/clean_qa.txt'
with open(filename, 'w', encoding='utf-8') as f:
    for index, row in df.iterrows():
        # Normalisasi kalimat pertanyaan
        question = normalize_sentence(str(row['question']))
        question = normalize_sentence(question)
        question = stemmer.stem(question)

        # Normalisasi dan preprocessing kalimat jawaban
        answer = str(row['answer']).lower().replace('iteung', 'aku').replace('\n', ' ')

        # Menulis data ke dalam file
        if len(question.split()) > 0 and len(question.split()) < 13 and len(answer.split()) < 29:
            body = "{"+question+"}|<START> {"+answer+"} <END>"
            print(body, file=f)
