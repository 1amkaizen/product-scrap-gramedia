import argparse
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from scrape import scrape_and_save_product_data
from login import login

def main():
    driver = None  # Inisialisasi driver di luar try-except-finally untuk mengatasi UnboundLocalError
    
    try:
        parser = argparse.ArgumentParser(description='Scrape product data from Gramedia.')
        parser.add_argument('-p', '--pages', type=int, default=1, help='Number of pages to scrape. Use 0 to scrape all pages.')
        parser.add_argument('-q', '--query', type=str, default=None, help='Search query for product')
        args = parser.parse_args()

        if not args.pages and not args.query:
            print("Silakan gunakan flag -p untuk menentukan jumlah halaman atau -q untuk pencarian produk.")
            return
        
        if args.pages != 1 and args.query:
            raise ValueError('Cannot use both -p and -q options simultaneously. Choose either -p or -q.')

        chromedriver_path = '/usr/bin/chromedriver'
        email = os.getenv('EMAIL')
        password = os.getenv('PASSWORD')

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        service = Service(chromedriver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)

        if args.pages or args.query:
            login(driver, email, password)

        if args.query:
            scrape_and_save_product_data(driver, args.pages, args.query)
        elif args.pages == 1 and not args.query:
            print("Silakan gunakan flag -p untuk menentukan jumlah halaman atau -q untuk pencarian produk.")
        else:
            scrape_and_save_product_data(driver, args.pages)

    except Exception as e:
        print(f'Terjadi kesalahan: {str(e)}')

    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()

