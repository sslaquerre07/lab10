from flask import Flask, request, jsonify, send_from_directory
import json
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def load_products():
    with open('products.json', 'r') as f:
        return json.load(f)['products']
    
@app.route('/products', methods=['GET'])
@app.route('/products/<int:product_id>', methods=['GET'])
def get_products(product_id = None):
    products = load_products()
    if product_id is None:
        #Returns all products wrapped in an object with the products key
        return jsonify({"products":products})
    else:
        product = next((p for p in products if p['id'] == product_id), None)
        #If a specific product is requested,
        #Wrap is in an objec with the products key
        return jsonify(product) if product else ('', 404)
    
@app.route('/products/add', methods=["POST"])
def add_product():
    new_product = request.json
    products = load_products()
    new_product['id'] = len(products) + 1
    products.append(new_product)
    with open('products.json', 'w') as f:
        json.dump({"products": products}, f)
    return jsonify(new_product), 201

@app.route('/product-images/<path:filename>')
def get_image(filename):
    return send_from_directory('product-images', filename)

# # @app.route('/products', methods=["PUT"])
# @app.route('/products/<int:product_id>', methods=['PUT'])
# def update_product(product_id):
#     products = load_products()
#     if product_id is None:
#         return jsonify({"products":products})
#     else:
#         # product = next((p for p in products if p['id'] == product_id), None)
#         # new_product = request.json
#         # products[product_id] = new_product
#         # with open('products.json', 'w') as f:
#         #     json.dump({"products": products}, f)
#         # return jsonify(new_product), 201
#         for product in products:
#             if product["id"] == product_id:
#                 updated_product = request.json
#                 product.update(updated_product)
#                 return jsonify(product)

@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    products = load_products()
    
    for product in products:
        if product["id"] == product_id:
            updated_product = request.json
            product.update(updated_product)
            with open('products.json', 'w') as f:
                json.dump({"products": products}, f)
            return jsonify(product)
    
    return jsonify({"error": "Product not found"}), 404

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    products = load_products()

    products = [product for product in products if product["id"] != product_id]
    with open('products.json', 'w') as f:
        json.dump({"products": products}, f)
    return jsonify(products)

if __name__ == '__main__':
    app.run(debug=True)
