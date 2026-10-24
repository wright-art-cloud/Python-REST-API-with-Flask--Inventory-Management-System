import requests
from services import fetch_product_from_openfoodfacts

BASE_URL = "http://127.0.0.1:5000/inventory"

def list_inventory():
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        items = response.json()
        print("\n--- Current Inventory ---")
        for item in items:
            print(f"ID: {item['id']} | Name: {item['product_name']} | Brand: {item['brands']} | Qty: {item['quantity']} | Price: ${item['price']}")
    else:
        print("Failed to fetch inventory.")

def get_single_item():
    item_id = input("Enter item ID to fetch: ")
    response = requests.get(f"{BASE_URL}/{item_id}")
    if response.status_code == 200:
        item = response.json()
        print("\n--- Item Details ---")
        print(item)
    else:
        print("Item not found.")

def add_new_item():
    name = input("Enter product name: ")
    brand = input("Enter brand: ")
    try:
        qty = int(input("Enter quantity: "))
        price = float(input("Enter price: "))
    except ValueError:
        print("Invalid number format for quantity or price.")
        return
    
    # Optionally enrich data from OpenFoodFacts API
    api_data = fetch_product_from_openfoodfacts(product_name=name)
    ingredients = api_data.get("ingredients_text", "") if api_data else ""

    payload = {
        "product_name": name,
        "brands": brand,
        "quantity": qty,
        "price": price,
        "ingredients_text": ingredients
    }

    response = requests.post(BASE_URL, json=payload)
    if response.status_code == 201:
        print("Item added successfully!")
    else:
        print("Failed to add item.")

def update_item():
    item_id = input("Enter item ID to update: ")
    print("Leave blank if you don't want to change a field.")
    name = input("New product name: ")
    brand = input("New brand: ")
    qty_str = input("New quantity: ")
    price_str = input("New price: ")

    payload = {}
    if name: payload["product_name"] = name
    if brand: payload["brands"] = brand
    if qty_str: payload["quantity"] = int(qty_str)
    if price_str: payload["price"] = float(price_str)

    response = requests.patch(f"{BASE_URL}/{item_id}", json=payload)
    if response.status_code == 200:
        print("Item updated successfully!")
    else:
        print("Failed to update item.")

def delete_item():
    item_id = input("Enter item ID to delete: ")
    response = requests.delete(f"{BASE_URL}/{item_id}")
    if response.status_code == 200:
        print("Item deleted successfully!")
    else:
        print("Item not found.")

def search_external_api():
    query = input("Enter product name or barcode to search on OpenFoodFacts: ")
    # Check if input is digits (barcode) or text (name)
    if query.isdigit():
        result = fetch_product_from_openfoodfacts(barcode=query)
    else:
        result = fetch_product_from_openfoodfacts(product_name=query)
        
    if result:
        print("\n--- External API Result ---")
        print(result)
    else:
        print("Product not found on OpenFoodFacts.")

def main_menu():
    while True:
        print("\n=== Inventory Management CLI ===")
        print("1. View All Inventory")
        print("2. View Single Item")
        print("3. Add New Item")
        print("4. Update Item")
        print("5. Delete Item")
        print("6. Search OpenFoodFacts API")
        print("7. Exit")
        
        choice = input("Choose an option (1-7): ")
        if choice == '1':
            list_inventory()
        elif choice == '2':
            get_single_item()
        elif choice == '3':
            add_new_item()
        elif choice == '4':
            update_item()
        elif choice == '5':
            delete_item()
        elif choice == '6':
            search_external_api()
        elif choice == '7':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1-7.")

if __name__ == "__main__":
    main_menu()