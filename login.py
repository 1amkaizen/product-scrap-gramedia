from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, TimeoutException
import time
def login(driver, email, password):
    driver.get('https://affiliate.gramedia.com/sign-in')
    print("Opened login page.")

    email_input = driver.find_element(By.NAME, 'email')
    password_input = driver.find_element(By.NAME, 'password')
    email_input.send_keys(email)
    password_input.send_keys(password)
    print("Entered email and password.")

    login_button = driver.find_element(By.XPATH, "//button[@type='submit' and contains(@class, 'MuiButton-root')]")
    login_button.click()
    print("Clicked login button.")

    # Optionally, wait for the login to complete
    time.sleep(5)  # Tunggu beberapa detik untuk memastikan halaman sudah termuat

    # Verify login by checking the current URL or an element specific to logged-in users
    current_url = driver.current_url
    if "sign-in" in current_url:
        raise Exception("Login failed. Still on the sign-in page.")
    print("Login successful, current URL:", current_url)

