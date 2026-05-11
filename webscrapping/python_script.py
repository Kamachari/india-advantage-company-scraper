import pandas as pd
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from concurrent.futures import ThreadPoolExecutor, as_completed
import re
from datetime import datetime

# ==========================================
# CONFIGURATION
# ==========================================

BASE_URL = "https://indiaadvantage.co.in/company-list"

LETTERS = [
    "a","b","c","d","e","f","g","h","i","j",
    "k","l","m","n","o","p","q","r","s","t",
    "u","v","w","x","y","z"
]

MAX_COMPANIES_PER_LETTER = 3
OUTPUT_FILE = "cleaned_leads.xlsx"


# ==========================================
# GET COMPANY PROFILE LINKS
# ==========================================

def scrape_company_links(page, letter):

    url = f"{BASE_URL}/{letter}"
    print(f"\nOpening: {url}")

    page.goto(url, timeout=60000, wait_until="domcontentloaded")
    page.wait_for_selector("div.companyname", timeout=15000)
    html = page.inner_html("body")
    soup = BeautifulSoup(html, "html.parser")

    company_links = []
    company_tags = soup.select("div.companyname a")

    for tag in company_tags:

        href = tag.get("href")
        company_name = tag.get_text(strip=True)

        if not href:
            continue

        if "/company-profile/" in href:

            full_url = f"https://indiaadvantage.co.in{href}"

            company_links.append({
                "company_name": company_name,
                "profile_url": full_url
            })

            print(company_name)
            print(full_url)
            print("-" * 50)

        if len(company_links) >= MAX_COMPANIES_PER_LETTER:
            break

    return company_links

# ==========================================
# clean phone number function
# ==========================================

def clean_phone(phone):

    if not phone:
        return "N/A"

    phone = str(phone).strip()

    if phone.upper() == "NA":
        return "N/A"

    # split multiple numbers
    parts = re.split(r'[\/,|]', phone)

    for p in parts:

        # remove spaces and hyphens
        num = p.replace("-", "").replace(" ", "")

        # keep digits only
        num = re.sub(r'\D', '', num)

        if not num:
            continue

        # CASE 1: mobile / normal number (10 digits)
        if len(num) == 10:
            return num

        # CASE 2: landline starting with 0 → remove first 0
        if num.startswith("0") and len(num) > 10:
            num = num[1:]

        # return cleaned landline if valid
        if len(num) >= 8:
            return num

    return "N/A"

# ==========================================
# GET COMPANY DETAILS
# ==========================================

def scrape_company_details(page, profile_url):

    print(f"\nOpening Profile: {profile_url}")

    page.goto(profile_url, timeout=60000)
    page.wait_for_timeout(3000)

    soup = BeautifulSoup(page.content(), "html.parser")

    info_card = soup.find("div", class_="compinform compborderbox")

    if not info_card:
        print("Info card not found")
        return None

    # DEFAULT VALUES
    company_name = "N/A"
    email = "N/A"
    website = "N/A"
    address = "N/A"
    location = "N/A"
    phone = "N/A"
    industry = "N/A"

    # COMPANY NAME
    title = soup.find("h1")
    if title:
        company_name = title.get_text(strip=True)

    # EMAIL
    email_tag = info_card.find("a", href=lambda x: x and "mailto:" in x)
    if email_tag:
        email = email_tag.get_text(strip=True)

    # WEBSITE
    website_tag = info_card.find("a", href=lambda x: x and "http" in x)
    if website_tag:
        website = website_tag.get_text(strip=True)

    # PHONE
    phone_tag = info_card.find("a", href=lambda x: x and "tel:" in x)
    if phone_tag:
        raw_phone = phone_tag.get_text(strip=True)
        phone = clean_phone(raw_phone)
    full_text = info_card.get_text(" ", strip=True)

    # ADDRESS
    address_text = ""
    for p in info_card.find_all("p"):
        text = p.get_text(" ", strip=True)

        if "Address" in text:
            address_text = (
                text.replace("Address :", "")
                    .replace("Address:", "")
                    .strip()
            )
            address_text = re.sub(r'\s+', ' ', address_text)
            address = address_text
            break

    # LOCATION
    location_match = re.search(r'([A-Za-z\s]+)-\d{6}', address_text)
    if location_match:
        location = location_match.group(1).strip().replace(",", "")

    # INDUSTRY
    industry_match = re.search(r'Industry\s*:\s*([A-Za-z &]+)', full_text)
    if industry_match:
        industry = industry_match.group(1).strip()

    # TIMESTAMP ADDED HERE
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {
        "Company Name": company_name,
        "Email": email,
        "Website": website,
        "Address": address,
        "Location": location,
        "Phone": phone,
        "Industry": industry,
        "Timestamp": timestamp
    }


# ==========================================
# CLEAN DATA
# ==========================================

def clean_data(records):

    df = pd.DataFrame(records)

    df.drop_duplicates(inplace=True)
    df.fillna("N/A", inplace=True)

    df["Company Name"] = df["Company Name"].astype(str).str.strip().str.title()
    df["Email"] = df["Email"].astype(str).str.lower()
    df["Location"] = df["Location"].astype(str).str.title()

    # ADD Sr. No.
    df.insert(0, "Sr. No.", range(1, len(df) + 1))

    return df


# ==========================================
# SAVE EXCEL
# ==========================================

def save_excel(df):

    df.to_excel(OUTPUT_FILE, index=False)
    print(f"\nExcel Saved: {OUTPUT_FILE}")

# ==========================================
# PARALLEL WORKER FUNCTION
# ==========================================

def process_letter(letter):

    records = []

    with sync_playwright() as playwright:

        browser = playwright.chromium.launch(headless=True)

        context = browser.new_context()
        page = context.new_page()

        try:

            company_links = scrape_company_links(page, letter)

            for company in company_links:

                record = scrape_company_details(
                    page,
                    company["profile_url"]
                )

                if record:
                    records.append(record)

        except Exception as e:
            print(f"Error in letter {letter}: {e}")

        browser.close()

    return records


# ==========================================
# MAIN
# ==========================================

def main():

    all_records = []

    with ThreadPoolExecutor(max_workers=5) as executor:

        futures = [
            executor.submit(process_letter, letter)
            for letter in LETTERS
        ]

        for future in as_completed(futures):

            result = future.result()

            if result:
                all_records.extend(result)

    if not all_records:
        print("No records collected.")
        return

    cleaned_df = clean_data(all_records)
    save_excel(cleaned_df)

    print("\nCompleted Successfully")


# ==========================================
# RUN SCRIPT
# ==========================================

if __name__ == "__main__":
    main()