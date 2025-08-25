import os
import asyncio
from playwright.async_api import async_playwright

# Configuration
COMPANY_NAME = "Reliance Industries Ltd"
COMPANY_CODE = "500325"
YEAR = "2025"
DOWNLOAD_DIR = "reports"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

async def scrape_reliance_2025():
    print(f"\n🔍 Searching for {COMPANY_NAME} Annual Report ({YEAR})...")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(accept_downloads=True)
        page = await context.new_page()

        # Go to BSE Historical Annual Report page
        await page.goto("https://www.bseindia.com/corporates/HistoricalAnnualReport.aspx")
        await page.wait_for_timeout(3000)

        # Find the frame that contains the form
        target_frame = None
        for frame in page.frames:
            try:
                await frame.wait_for_selector("#ddlYear", timeout=3000)
                target_frame = frame
                print("✅ Found form in frame")
                break
            except:
                continue

        if not target_frame:
            print("❌ Could not find form in any frame.")
            await browser.close()
            return

        # Select year
        await target_frame.locator("#ddlYear").select_option(label=YEAR)

        # Enter company code
        await target_frame.locator("#txtScrip").fill(COMPANY_CODE)

        # Click search
        await target_frame.locator("#btnSearch").click()

        # Wait for results table
        await target_frame.locator("#grdAnnualReport").wait_for(timeout=10000)

        # Find the correct row and download
        rows = await target_frame.locator("#grdAnnualReport tr").all()
        for row in rows:
            cells = await row.locator("td").all()
            if len(cells) >= 2:
                text = await cells[1].inner_text()
                if COMPANY_NAME in text and "Annual Report" in text:
                    download_link = row.locator("a")
                    download = await download_link.click()
                    download_path = await download.path()
                    filename = os.path.join(DOWNLOAD_DIR, f"Annual_Report_{COMPANY_NAME.replace(' ', '_')}_{YEAR}.pdf")
                    os.rename(download_path, filename)
                    print(f"📥 Downloaded: {filename}")
                    break
        else:
            print(f"⚠️ No Annual Report found for {COMPANY_NAME} in {YEAR}.")

        await browser.close()
        print("\n✅ Script completed.")

# Run the async function
asyncio.run(scrape_reliance_2025())
