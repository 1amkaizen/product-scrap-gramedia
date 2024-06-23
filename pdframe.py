import pandas as pd

# Load dataset
df = pd.read_csv('products.csv')

# Tampilkan dataframe untuk memastikan data terbaca dengan benar
print(df)
#print(df.info())
#print(df.describe())  # Menampilkan statistik deskriptif untuk kolom-kolom numerik
#print(df.shape)  # Menampilkan jumlah baris dan kolom dalam DataFrame
#print(df['Harga'].dtype)  # Menampilkan tipe data kolom 'harga'
#print(df['Kategori'].unique())  # Menampilkan nilai unik dalam kolom 'kategori'
#print(df['Penulis'].value_counts())  # Menghitung jumlah buku yang ditulis oleh setiap penulis
#print(df.isnull().sum())  # Menghitung jumlah nilai null dalam setiap kolom
#print(df.groupby('final_price').mean())  # Menghitung rata-rata harga untuk setiap kategori

