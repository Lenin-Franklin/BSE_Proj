import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Configuration
COMPANY_NAME = "Reliance Industries Ltd"
COMPANY_CODE = "500325"
YEAR = "2025"
DOWNLOAD_DIR = "reports"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Setup Chrome
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def download_pdf(url, filename):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"✅ Downloaded: {filename}")
        else:
            print(f"❌ Failed to download: {url} (Status: {response.status_code})")
    except Exception as e:
        print(f"⚠️ Error downloading {filename}: {e}")

def scrape_reliance_2025():
    print(f"\n🔍 Searching for {COMPANY_NAME} Annual Report ({YEAR})...")
    driver.get("https://www.bseindia.com/corporates/HistoricalAnnualReport.aspx")
    time.sleep(5)  # Let the page settle

    try:
        # Wait for dropdown and form fields directly in main page
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "ddlYear")))
        print("✅ Found ddlYear in main page")

        # Select year
        Select(driver.find_element(By.ID, "ddlYear")).select_by_visible_text(YEAR)

        # Enter company code
        scrip_input = driver.find_element(By.ID, "txtScrip")
        scrip_input.clear()
        scrip_input.send_keys(COMPANY_CODE)

        # Click search
        driver.find_element(By.ID, "btnSearch").click()

        # Wait for results table
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "grdAnnualReport")))

        # Find and download the correct Annual Report
        rows = driver.find_elements(By.XPATH, "//table[@id='grdAnnualReport']//tr")
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) >= 2:
                report_name = cells[1].text.strip()
                if COMPANY_NAME in report_name and "Annual Report" in report_name:
                    link = row.find_element(By.TAG_NAME, "a").get_attribute("href")
                    filename = os.path.join(DOWNLOAD_DIR, f"Annual_Report_{COMPANY_NAME.replace(' ', '_')}_{YEAR}.pdf")
                    download_pdf(link, filename)
                    break
        else:
            print(f"⚠️ No Annual Report found for {COMPANY_NAME} in {YEAR}.")

    except Exception as e:
        print(f"❌ Error during scraping: {type(e).__name__}: {e}")
        with open("page_dump.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("📝 Dumped page source to page_dump.html for inspection.")

scrape_reliance_2025()
driver.quit()
print("\n✅ Script completed.")
