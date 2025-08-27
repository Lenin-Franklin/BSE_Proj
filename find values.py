from bs4 import BeautifulSoup

with open("bse_page.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

for sel in soup.find_all("select"):
    print("ID:", sel.get("id"), "| Name:", sel.get("name"))

    # Print first 10 options for preview
    opts = sel.find_all("option")
    for o in opts[:10]:
        print("   ->", o.text.strip())
    print("------")