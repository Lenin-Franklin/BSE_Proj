import os
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


class CompanySearch:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def search_company(self, company_name: str):
        """Searches for a company and loads its annual report page"""
        try:
            search_box = self.wait.until(
                EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_SmartSearch_smartSearch"))
            )
            search_box.clear()
            search_box.send_keys(company_name)
            time.sleep(2)  # let dropdown load
            search_box.send_keys(Keys.ENTER)

            submit_btn = self.wait.until(
                EC.element_to_be_clickable((By.ID, "ContentPlaceHolder1_btnSubmit"))
            )
            submit_btn.click()

            self.wait.until(
                EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_gvData"))
            )
            print(f"✔️ Search completed for {company_name}")

        except Exception as e:
            print(f"⚠️ Error while searching company {company_name}: {e}")


class AnnualReportDownloader:
    def __init__(self, driver, wait, base_dir):
        self.driver = driver
        self.wait = wait
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)

    def download_reports(self, company_code: str, company_name: str, limit: int = 7):
        """Extracts annual report table and downloads only the latest N PDFs"""
        try:
            report_table = self.wait.until(
                EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_grdAnnualReport"))
            )
            rows = report_table.find_elements(By.TAG_NAME, "tr")

            print(f"✔️ Found {len(rows)-1} reports for {company_name}")

            # Company-specific folder
            company_dir = os.path.join(self.base_dir, company_code.upper())
            os.makedirs(company_dir, exist_ok=True)

            # ✅ Pick only the latest N reports (skip header row)
            latest_rows = rows[1:limit+1]

            for row in latest_rows:
                cols = row.find_elements(By.TAG_NAME, "td")
                if not cols:
                    continue

                year = cols[0].text.strip()
                pdf_link = cols[-1].find_element(By.TAG_NAME, "a").get_attribute("href")

                if pdf_link and pdf_link.endswith(".pdf"):
                    filepath = os.path.join(company_dir, f"{year}_{company_code}.pdf")

                    if not os.path.exists(filepath):
                        response = requests.get(pdf_link, stream=True)
                        with open(filepath, "wb") as f:
                            for chunk in response.iter_content(1024):
                                f.write(chunk)
                        print(f"✅ Downloaded {filepath}")
                    else:
                        print(f"⏩ Skipped {year} (already exists)")
                else:
                    print(f"⚠️ No valid PDF link for {year}")

        except Exception as e:
            print(f"⚠️ Error extracting reports for {company_name}: {e}")


# --- Usage Example ---
if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 15)

    driver.get("https://www.bseindia.com/corporates/HistoricalAnnualreport.aspx")

    try:
        base_dir = r"C:\Users\lenin\OneDrive\Desktop\NSE Scraper"

        searcher = CompanySearch(driver, wait)
        searcher.search_company("INFOSYS")

        downloader = AnnualReportDownloader(driver, wait, base_dir)
        downloader.download_reports("INFY", "INFOSYS", limit=7)  # ✅ now latest 7 reports

    finally:
        time.sleep(5)
        driver.quit()
