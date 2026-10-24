import requests

def fetch_product_from_openfoodfacts(barcode=None, product_name=None):
    """
    Queries the OpenFoodFacts API either by barcode or by product name search.
    Returns a formatted dictionary with key product details, or None if not found/error.
    """
    try:
        if barcode:
            url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == 1:
                    prod = data.get("product", {})
                    return {
                        "product_name": prod.get("product_name", "Unknown Product"),
                        "brands": prod.get("brands", "Unknown Brand"),
                        "ingredients_text": prod.get("ingredients_text", "No ingredients listed"),
                    }
        elif product_name:
            url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={product_name}&search_simple=1&action=process&json=1"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                products = data.get("products", [])
                if products:
                    prod = products[0]
                    return {
                        "product_name": prod.get("product_name", "Unknown Product"),
                        "brands": prod.get("brands", "Unknown Brand"),
                        "ingredients_text": prod.get("ingredients_text", "No ingredients listed"),
                    }
    except requests.RequestException as e:
        print(f"API request failed: {e}")
        
    return None