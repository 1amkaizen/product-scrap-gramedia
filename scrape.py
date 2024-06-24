import os
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys

# Fungsi untuk mengumpulkan URL produk dari halaman produk dengan pencarian
def get_product_urls(driver, pages, query=None):
    product_urls = []
    try:
        driver.get('https://affiliate.gramedia.com/content/products')

        if query:
            # Lakukan pencarian jika ada query
            search_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="input-search"]'))
            )
            search_input.clear()
            search_input.send_keys(query)
            search_input.send_keys(Keys.RETURN)

            # Tunggu hingga hasil pencarian dimuat
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="products-list"]/a'))
            )
        else:
            # Tunggu hingga produk-list dimuat
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="products-list"]/a'))
            )

        current_page = 1
        while True:
            product_elements = driver.find_elements(By.XPATH, '//*[@id="products-list"]/a')
            print(f"Menelusuri halaman {current_page}...")
            
            for product_element in product_elements:
                url = product_element.get_attribute('href')
                product_urls.append(url)

            if pages != 0 and current_page >= pages:
                break

            try:
                next_button = driver.find_element(By.XPATH, '//button[@aria-label="Go to next page"]')
                next_button.click()
                current_page += 1
                WebDriverWait(driver, 10).until(
                    EC.staleness_of(product_elements[0])
                )
            except (NoSuchElementException, TimeoutException):
                break

        return product_urls

    except Exception as e:
        print('Terjadi kesalahan saat mengumpulkan URL produk:', str(e))
        return []
    

# Fungsi untuk mengambil data dari setiap halaman produk
def scrape_product_data(driver, product_url):
    try:
        driver.get(product_url)
        
        # Tunggu hingga judul produk dimuat
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="fuse-main"]/div/div/div[2]/div[2]/div[1]/h1'))
        )
        
        # Mengambil judul produk
        title = driver.find_element(By.XPATH, '//*[@id="fuse-main"]/div/div/div[2]/div[2]/div[1]/h1').text
        if title.endswith(':'):
            title = title[:-1]
        
        # Mengambil author produk
        try:
            author = driver.find_element(By.XPATH, '//*[@id="fuse-main"]/div/div/div[2]/div[2]/div[1]/p').text
        except NoSuchElementException:
            author = 'Unknown'
        
        # Mengambil harga jual produk
        try:
            final_price = driver.find_element(By.XPATH, '//*[@id="fuse-main"]/div/div/div[2]/div[2]/div[1]/h6').text
        except NoSuchElementException:
            final_price = 'Not available'
        
        # Mengambil URL gambar produk
        try:
            image_url = driver.find_element(By.XPATH, '//*[@id="fuse-main"]/div/div/div[2]/div[1]/div[1]/div[1]/img').get_attribute('src')
        except NoSuchElementException:
            image_url = 'Not available'
        
        # Mengambil deskripsi produk
        try:
            read_more_button = driver.find_element(By.XPATH, '//button[contains(text(), "Read more")]')
            read_more_button.click()
            WebDriverWait(driver, 10).until(
                EC.text_to_be_present_in_element((By.XPATH, '//button[contains(text(), "Show less")]'), "Show less")
            )
        except NoSuchElementException:
            pass

        try:
            description_element = driver.find_element(By.XPATH, '//*[@class="relative pb-[24px] mt-[14px] w-full h-full overflow-hidden"]/p')
            description = description_element.text.replace('Show less', '').strip()
        except NoSuchElementException:
            description = 'No description available'
        
        # Ambil URL afiliasi
        try:
            generate_link_button = driver.find_element(By.XPATH, '//*[@id="fuse-main"]/div/div/div[2]/div[3]/div/div[1]/button')
            if generate_link_button.is_enabled():
                generate_link_button.click()
                # Tunggu hingga URL afiliasi muncul
                affiliate_url_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//input[@id=":r2:"]'))
                )
                affiliate_url = affiliate_url_element.get_attribute('value')
            else:
                # Jika tombol sudah diklik sebelumnya, langsung ambil URL afiliasi
                affiliate_url_element = driver.find_element(By.XPATH, '//input[@id=":r2:"]')
                affiliate_url = affiliate_url_element.get_attribute('value')
        except NoSuchElementException:
            affiliate_url = 'Not generated'  # Atau nilai lain yang sesuai dengan konteks
        
        # Mengambil detail lainnya
        details = {
            'jumlah halaman': '',
            'penerbit': '',
            'tanggal terbit': '',
            'berat': '',
            'isbn': '',
            'lebar': '',
            'bahasa': '',
            'panjang': ''
        }
        
        detail_elements = driver.find_elements(By.XPATH, '//*[@class="mt-[32px] grid grid-cols-2 gap-y-[22px]"]/div')
        
        for element in detail_elements:
            label = element.find_element(By.XPATH, './p[1]').text.strip().lower()
            value = element.find_element(By.XPATH, './p[2]').text.strip()
            
            if label == 'pages':
                details['jumlah halaman'] = value
            elif label == 'publisher':
                details['penerbit'] = value
            elif label == 'publish date':
                details['tanggal terbit'] = value
            elif label == 'weight':
                details['berat'] = value
            elif label == 'isbn':
                details['isbn'] = value
            elif label == 'width':
                details['lebar'] = value
            elif label == 'language':
                details['bahasa'] = value
            elif label == 'height':
                details['panjang'] = value
        
        data = {
            'title': title,
            'author': author,
            'final_price': final_price,
            'jumlah halaman': details['jumlah halaman'],
            'penerbit': details['penerbit'],
            'tanggal terbit': details['tanggal terbit'],
            'berat': details['berat'],
            'isbn': details['isbn'],
            'lebar': details['lebar'],
            'bahasa': details['bahasa'],
            'panjang': details['panjang'],
            'image_url': image_url,
            'description': description,
            'affiliate_url': affiliate_url  # Menambahkan URL afiliasi ke dalam data produk
        }
        
        return data

    except Exception as e:
        print(f'Terjadi kesalahan saat mengambil data produk dari {product_url}: {str(e)}')
        return None

# Fungsi untuk memuat URL yang sudah diproses dari file
def load_processed_urls(processed_urls_file):
    if os.path.exists(processed_urls_file):
        with open(processed_urls_file, 'r') as file:
            return set(file.read().splitlines())
    return set()

# Fungsi untuk menyimpan URL yang sudah diproses ke file
def save_processed_urls(processed_urls, processed_urls_file):
    with open(processed_urls_file, 'a') as file:
        for url in processed_urls:
            file.write(f"{url}\n")

# Fungsi untuk mengumpulkan URL produk dan menyimpan data produk ke CSV
def scrape_and_save_product_data(driver, pages, query=None, output_file='products.csv', processed_urls_file='processed_urls.txt'):
    if query:
        print(f'Mencari produk dengan kata kunci: {query}')
    
    processed_urls = load_processed_urls(processed_urls_file)
    
    if query:
        product_urls = get_product_urls(driver, 1, query)
    else:
        product_urls = get_product_urls(driver, pages)
    
    data_list = []
    new_processed_urls = set()
    
    for product_url in product_urls:
        if product_url in processed_urls:
            continue
        
        data = scrape_product_data(driver, product_url)
        if data:
            data_list.append(data)
            new_processed_urls.add(product_url)
    
    if data_list:
        if os.path.exists(output_file):
            df = pd.DataFrame(data_list)
            df.to_csv(output_file, mode='a', header=False, index=False)
        else:
            df = pd.DataFrame(data_list)
            df.to_csv(output_file, index=False)
        print(f'Data produk telah disimpan ke {output_file}')
    else:
        print('Tidak ada data produk yang berhasil diambil')
    
    save_processed_urls(new_processed_urls, processed_urls_file)
    print(f'URL produk yang diproses telah disimpan ke {processed_urls_file}')

