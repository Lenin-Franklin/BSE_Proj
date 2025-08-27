from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def fetch_reports(company_name):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.bseindia.com/corporates/HistoricalAnnualreport.aspx")

    # 1. Enter company name
    search_box = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "txtSecurityName"))
    )
    search_box.clear()
    search_box.send_keys(company_name)

    # 2. Click Submit
    submit_btn = driver.find_element(By.ID, "btnSubmit")
    submit_btn.click()

    # 3. Wait for results table
    results_table = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_grdAnnualReport"))
    )

    # 4. Extract report links
    rows = results_table.find_elements(By.TAG_NAME, "tr")
    for row in rows[1:]:  # skip header
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) >= 3:
            year = cols[1].text.strip()
            link = cols[2].find_element(By.TAG_NAME, "a").get_attribute("href")
            print(year, "->", link)

    time.sleep(3)
    driver.quit()

# Example usage
fetch_reports("INFOSYS LTD")