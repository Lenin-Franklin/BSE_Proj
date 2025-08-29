from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

# --- Setup WebDriver ---
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

url = "https://www.bseindia.com/corporates/HistoricalAnnualreport.aspx"
driver.get(url)

wait = WebDriverWait(driver, 15)

try:
    # --- Step 1: Locate search box ---
    search_box = wait.until(
        EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_SmartSearch_smartSearch"))
    )
    print("✔️ Search box found")

    # --- Step 2: Type company name and wait for dropdown ---
    search_box.clear()
    search_box.send_keys("INFOSYS")
    time.sleep(2)  # wait for dropdown to appear

    # Press ENTER directly (first suggestion is auto-selected)
    search_box.send_keys(Keys.ENTER)
    print("✔️ First dropdown suggestion selected via ENTER")

    # --- Step 3: Click Submit button ---
    submit_btn = wait.until(
        EC.element_to_be_clickable((By.ID, "ContentPlaceHolder1_btnSubmit"))
    )
    submit_btn.click()
    print("✔️ Submit button clicked")

    # --- Step 4: Wait for results ---
    wait.until(
        EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_gvData"))
    )
    print("✔️ Results table loaded successfully")

except Exception as e:
    print(f"⚠️ Error: {e}")

finally:
    time.sleep(5)
    driver.quit()
