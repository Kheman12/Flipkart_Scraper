Here's a complete professional documentation for your script, formatted with clear sections for **overview**, **requirements**, **components**, **usage**, and **function descriptions**:

---

# 📄 Flipkart Laptop Scraper Documentation

## 🧾 Overview

This Python script uses **Crawl4AI** to scrape **laptop listings from Flipkart**, extracting structured product data like name, price, description, and rating. It paginates through the search results, stops automatically when no more data is available, and exports the results to an Excel file (`laptops.xlsx`).

The crawler uses a **CSS selector-based schema** with Crawl4AI's `JsonCssExtractionStrategy`, processes pages asynchronously, and runs a headless browser to simulate real-user behavior.

---

## 📦 Requirements

* Python 3.8+
* crawl4ai
* pandas
* pydantic

### Install required packages

```bash
pip install crawl4ai pandas pydantic openpyxl
```

---

## 🧱 Components

### 1. **Data Model: `Items`**

A `pydantic.BaseModel` that represents a structured item:

```python
class Items(BaseModel):
    name: str
    description: str
    price: str
    rating: str
```

---

### 2. **Extraction Schema**

CSS selectors are used to locate data on each product listing:

```python
schema = {
    "name": "Laptops",
    "baseSelector": "a.CGtC98",
    "fields": [
        {"name": "Name", "selector": "div.KzDlHZ", "type": "text"},
        {"name": "Price", "selector": "div.Nx9bqj._4b5DiR", "type": "text"},
        {"name": "Description", "selector": "div._6NESgJ", "type": "text"},
        {"name": "rating", "selector": "div.XQDdHH", "type": "text"},
    ]
}
```

---

### 3. **Browser & Crawler Configurations**

* `BrowserConfig`: Sets headless mode and persistent context.
* `CrawlerRunConfig`: Defines strategies for content extraction, tag filtering, full-page scanning, and user simulation.

---

## 🚀 Function: `scrape_items()`

### Description

Main coroutine that:

* Builds the extraction strategy.
* Sets up the browser and crawler.
* Iteratively scrapes Flipkart search result pages.
* Stops when no more items are found or on error.
* Saves the collected data to an Excel file.

### Key Features

* Full-page scrolling (`scan_full_page=True`)
* Overlay removal
* Image and external link exclusion
* Structured data output to Excel
* Error and progress logging

---

## 🖥️ How to Run

Execute the script directly:

```bash
python script_name.py
```

Example output:

```
📄 Scraping page 1: https://www.flipkart.com/search?q=laptops&page=1
📄 Scraping page 2: https://www.flipkart.com/search?q=laptops&page=2
...
✅ Scraping completed. Total items: 120. Saved to laptops.xlsx
```

---

## 📁 Output

An Excel file named `laptops.xlsx` containing all extracted product data in tabular form with the following columns:

* **Name**
* **Price**
* **Description**
* **Rating**

---


