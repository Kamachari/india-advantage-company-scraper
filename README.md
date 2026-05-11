````markdown
# 🚀 India Advantage Company Scraper

A high-performance, automated web scraping system built using Python and Playwright to extract structured company data from India Advantage directory listings. The project is designed to efficiently collect, clean, and export business intelligence data for analytics, lead generation, and research workflows.

The scraper is optimized for speed, scalability, and data consistency using parallel processing and robust parsing techniques.

---

# ✨ Features

- 🔍 Automated scraping of company listings (A–Z directory traversal)
- ⚡ Parallel execution using multi-threading for faster data extraction
- 🧠 Structured parsing of company profiles (name, email, website, phone, industry, address)
- 🧹 Intelligent data cleaning and normalization (phone, email, location formatting)
- 📊 Deduplication and missing value handling
- 🕒 Timestamp tracking for each record
- 📁 Export to Excel (.xlsx) format for business use
- 🛡️ Error handling for failed pages and network interruptions
- 🔄 Scalable design supporting large dataset extraction

---

# 📦 Requirements & Installation

## 🔧 Prerequisites

- Python 3.8+
- pip package manager

## 📚 Install Dependencies

```bash
pip install pandas beautifulsoup4 playwright openpyxl
````

## 🌐 Install Playwright Browsers

```bash
playwright install
```

---

# ▶️ Usage

Run the scraper using:

```bash
python scraper.py
```

The script will:

1. Iterate through company listings (A–Z)
2. Scrape up to 3 companies per letter
3. Extract detailed profile data
4. Clean and structure the dataset
5. Export results into an Excel file

---

## 🧪 Example Workflow

```python
if __name__ == "__main__":
    main()
```

---

# ⚙️ Configuration

You can modify the scraping behavior using the following parameters:

```python
BASE_URL = "https://indiaadvantage.co.in/company-list"
LETTERS = list("abcdefghijklmnopqrstuvwxyz")
MAX_COMPANIES_PER_LETTER = 3
OUTPUT_FILE = "cleaned_leads.xlsx"
```

### 🔧 Performance Tuning

Inside `main()`:

```python
ThreadPoolExecutor(max_workers=5)
```

* Increase workers → faster scraping (risk of blocking)
* Decrease workers → safer but slower execution

---

# 📤 Output Format

The final dataset is exported as an Excel file:

### Columns:

* Sr. No.
* Company Name
* Email
* Website
* Phone
* Address
* Location
* Industry
* Timestamp

---

## 📊 Sample Output

| Sr. No. | Company Name | Email                               | Phone      | Location  |
| ------- | ------------ | ----------------------------------- | ---------- | --------- |
| 1       | ABC Pvt Ltd  | [info@abc.com](mailto:info@abc.com) | 9876543210 | Hyderabad |

---

# ⚠️ Limitations & Ethical Considerations

* ⚠️ This scraper is intended for educational and research purposes only
* 📜 Users must comply with the target website’s Terms of Service
* 🤖 Respect `robots.txt` rules and avoid excessive request rates
* 🚫 High concurrency may lead to temporary IP blocking
* ⏱️ Recommended delay or worker limit for safe scraping

---

# 🛠️ Troubleshooting

### ❌ Playwright not installed correctly

```bash
playwright install
```

---

### ❌ Empty results

* Check selectors (`div.companyname`, `compinform`)
* Ensure website structure hasn’t changed

---

### ❌ Slow execution

* Reduce `wait_for_timeout`
* Enable headless mode:

```python
headless=True
```

---

### ❌ Blocking issues

* Reduce `max_workers`
* Add delay between requests
* Use headless mode with stealth enhancements

---

# 🤝 Contributing

Contributions are welcome!

### Steps:

1. Fork the repository
2. Create a feature branch
3. Commit changes with clear messages
4. Submit a pull request

Improvements in parsing accuracy, speed optimization, and scalability are highly encouraged.

---

# 📄 License

This project is licensed under the MIT License.

---

# 📬 Contact / Support

For issues, suggestions, or collaboration:

* GitHub Issues: Create an issue in the repository
* Email: [kamachariburagapalli@gmail.com](mailto:your-email@example.com)

---


---
```
