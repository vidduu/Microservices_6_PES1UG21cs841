from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://mongo:27017/"
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True



client = MongoClient("mongodb://mongo:27017/")
db = client.ecommerce
products = db.products

@app.route('/')
def hello_geek():
    return '<h1>Products Microservice working</h2>'

@app.route('/getallproducts', methods=['GET'])
def get_products():
    products = list(db.products.find())
    for product in products:
        product['_id'] = str(product['_id'])
    return jsonify(products)

@app.route('/products', methods=['POST'])
def create_product():
    new_product = request.json
    product_id = products.insert_one(new_product).inserted_id
    return jsonify({'product_id': str(product_id)})

@app.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
    product = db.products.find_one({'_id': ObjectId(product_id)})
    if product is None:
        return jsonify({'error': 'Product not found'}), 404
    product['_id'] = str(product['_id'])
    return jsonify(product)

@app.route('/products/<product_id>', methods=['PUT'])
def update_product(product_id):
    updated_product = request.json
    products.update_one({'_id': ObjectId(product_id)}, {'$set': updated_product})
    return jsonify({'message': 'Product updated'})

@app.route('/products/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    products.delete_one({'_id': ObjectId(product_id)})
    return jsonify({'message': 'Product deleted'})


if __name__ == '__main__':
    app.run(port=5050,debug=True)
    