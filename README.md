# product-scrap-gramedia

Proyek ini menggunakan Selenium untuk melakukan scraping data produk dari situs web Gramedia Affiliates. Anda dapat menggunakannya untuk mengumpulkan informasi produk seperti judul, harga, deskripsi, dan lain-lain.


Pastikan juga Anda memiliki Chrome WebDriver yang sesuai dengan versi Chrome Anda. Anda dapat mengunduhnya [di sini](https://sites.google.com/a/chromium.org/chromedriver/downloads) dan pastikan menyesuaikan path-nya di file `main.py`.

### Penggunaan

1. **Login ke Gramedia Affiliates:**
   Sebelum memulai scraping, pastikan untuk login ke Gramedia Affiliates dengan mengatur variabel lingkungan `EMAIL` dan `PASSWORD`.

   ```bash
   export EMAIL="youremail@gmail.com"
   export PASSWORD="yourpassword"
   ```

   
2. **Scraping dengan Parameter -p (Pages):**
   Untuk menelusuri jumlah halaman produk tertentu, gunakan parameter `-p` diikuti dengan jumlah halaman yang diinginkan:
   ```
   python main.py -p 2
   ```
   Ini akan menelusuri dua halaman produk dari Gramedia.

3. **Scraping dengan Parameter -q (Query):**
   Untuk melakukan pencarian produk berdasarkan kata kunci, gunakan parameter `-q` diikuti dengan query pencarian:
   ```
   python main.py -q "buku panduan belajar"
   ```
   Ini akan mencari produk dengan kata kunci "buku panduan belajar".

4. **Bantuan dan Opsi Lainnya:**
   Untuk melihat opsi lengkap yang tersedia, termasuk bantuan dan panduan, gunakan flag `-h`:
   ```
   python main.py -h
   ```



