import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# Step 1: Define target websites
# -------------------------------
urls = [
    "http://quotes.toscrape.com/",          # Quotes & authors
    "http://books.toscrape.com/catalogue/", # Book titles & prices
    "https://httpbin.org/html"              # Dummy site (structure test)
]

# Storage
all_data = []

# -------------------------------
# Step 2: Scraping Logic
# -------------------------------
def scrape_quotes(url):
    data = []
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    quotes = soup.find_all("span", class_="text")
    authors = soup.find_all("small", class_="author")
    
    for q, a in zip(quotes, authors):
        data.append({
            "type": "quote",
            "content": q.text.strip(),
            "author": a.text.strip(),
            "price/review": None
        })
    return data

def scrape_books(url):
    data = []
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    books = soup.find_all("article", class_="product_pod")
    
    for b in books:
        title = b.h3.a["title"]
        price = b.find("p", class_="price_color").text
        data.append({
            "type": "book",
            "content": title,
            "author": None,
            "price/review": price
        })
    return data

# -------------------------------
# Step 3: Call scrapers
# -------------------------------
all_data.extend(scrape_quotes(urls[0]))
all_data.extend(scrape_books(urls[1]))

# -------------------------------
# Step 4: Store in CSV
# -------------------------------
df = pd.DataFrame(all_data)
df.to_csv("scraped_data.csv", index=False)
print("✅ Data saved in scraped_data.csv")

# -------------------------------
# Step 5: Data Analysis
# -------------------------------
print("\nSample Data:\n", df.head())

# Count quotes vs books
count_type = df["type"].value_counts()

# Visualization
plt.figure(figsize=(6,4))
count_type.plot(kind="bar", color=["skyblue", "salmon"])
plt.title("Data Distribution: Quotes vs Books")
plt.xlabel("Data Type")
plt.ylabel("Count")
plt.show()
