import requests
from bs4 import BeautifulSoup
import pandas as pd

def search_snapdeal(query):
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = f"https://www.snapdeal.com/search?keyword={query.replace(' ', '%20')}"
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = []

    products = soup.select("div.product-tuple-description")

    for product in products:
        name = product.select_one("p.product-title")
        price = product.select_one("span.lfloat.product-price")
        rating = "No Rating"  

        if name and price:
            results.append({
                "Website": "Snapdeal",
                "Product Name": name.text.strip(),
                "Price": price.text.strip(),
                "Rating": rating
            })

    return results

def search_croma(query):
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = f"https://www.croma.com/searchB?q={query.replace(' ', '%20')}"
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = []

    products = soup.select("div.product")

    for product in products:
        name = product.select_one("h3.product-title")
        price = product.select_one("span.amount")
        rating = product.select_one("div.rating")  

        if name and price:
            results.append({
                "Website": "Croma",
                "Product Name": name.get_text(strip=True),
                "Price": price.get_text(strip=True),
                "Rating": rating.get_text(strip=True) if rating else "No Rating"
            })

    return results

def save_to_excel(data, filename='product_results.xlsx'):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    print(f"\n Results saved to {filename}")

def show_results(data):
    print("\n Products Found:\n")
    for idx, item in enumerate(data, 1):
        print(f"{idx}. [{item['Website']}] {item['Product Name']}")
        print(f"   Price : {item['Price']}")
        print(f"   Rating: {item['Rating']}\n")

def main():
    query = input("Enter product name to search: ").strip()

    print("\n Searching on Snapdeal...")
    snapdeal_data = search_snapdeal(query)

    print(" Searching on Croma...")
    croma_data = search_croma(query)

    all_data = snapdeal_data + croma_data

    if all_data:
        show_results(all_data)
        save_to_excel(all_data)
    else:
        print(" No results found. Try another keyword.")

if __name__ == "__main__":
    main()
