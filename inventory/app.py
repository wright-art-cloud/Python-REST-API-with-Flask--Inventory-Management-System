from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated in-memory database array (mock inventory)
inventory = [
    {
        "id": 1,
        "product_name": "Organic Almond Milk",
        "brands": "Silk",
        "quantity": 50,
        "price": 3.99,
        "ingredients_text": "Filtered water, almonds, cane sugar, ..."
    },
    {
        "id": 2,
        "product_name": "Greek Yogurt",
        "brands": "Chobani",
        "quantity": 30,
        "price": 1.49,
        "ingredients_text": "Cultured pasteurized nonfat milk, live and active cultures."
    }
]

# GET /inventory -> Fetch all items
@app.route('/inventory', methods=['GET'])
def get_inventory():
    return jsonify(inventory), 200

# GET /inventory/<id> -> Fetch a single item
@app.route('/inventory/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((i for i in inventory if i["id"] == item_id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item), 200

# POST /inventory -> Add a new item
@app.route('/inventory', methods=['POST'])
def add_item():
    data = request.get_json()
    if not data or not data.get("product_name"):
        return jsonify({"error": "Invalid input, product_name is required"}), 400
    
    new_id = max([i["id"] for i in inventory], default=0) + 1
    new_item = {
        "id": new_id,
        "product_name": data.get("product_name"),
        "brands": data.get("brands", ""),
        "quantity": data.get("quantity", 0),
        "price": data.get("price", 0.0),
        "ingredients_text": data.get("ingredients_text", "")
    }
    inventory.append(new_item)
    return jsonify(new_item), 201

# PATCH /inventory/<id> -> Update an item (stock level, price, etc.)
@app.route('/inventory/<int:item_id>', methods=['PATCH'])
def update_item(item_id):
    item = next((i for i in inventory if i["id"] == item_id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "No update data provided"}), 400

    item["product_name"] = data.get("product_name", item["product_name"])
    item["brands"] = data.get("brands", item["brands"])
    item["quantity"] = data.get("quantity", item["quantity"])
    item["price"] = data.get("price", item["price"])
    item["ingredients_text"] = data.get("ingredients_text", item["ingredients_text"])

    return jsonify(item), 200

# DELETE /inventory/<id> -> Remove an item
@app.route('/inventory/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global inventory
    item = next((i for i in inventory if i["id"] == item_id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    
    inventory = [i for i in inventory if i["id"] != item_id]
    return jsonify({"message": "Item deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)