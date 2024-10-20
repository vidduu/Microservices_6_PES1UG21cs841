from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://mongo:27017/"
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

client = MongoClient("mongodb://mongo:27017/")
db = client.ecommerce
orders = db.orders

@app.route('/')
def hello_geek():
    return '<h1>Orders Microservice working</h2>'


@app.route('/getallorders', methods=['GET'])
def get_orders():
    orders = list(db.orders.find())
    for order in orders:
        order['_id'] = str(order['_id'])
        order['date'] = order['date'].strftime("%Y-%m-%d %H:%M:%S")
    return jsonify(orders)

@app.route('/orders', methods=['POST'])
def create_order():
    new_order = request.json
    order_id = orders.insert_one(new_order).inserted_id
    return jsonify({'order_id': str(order_id)})

@app.route('/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    order = db.orders.find_one({'_id': ObjectId(order_id)})
    if order is None:
        return jsonify({'error': 'Order not found'}), 404
    order['_id'] = str(order['_id'])
    order['date'] = order['date'].strftime("%Y-%m-%d %H:%M:%S")
    return jsonify(order)

@app.route('/orders/<order_id>', methods=['PUT'])
def update_order(order_id):
    updated_order = request.json
    orders.update_one({'_id': ObjectId(order_id)}, {'$set': updated_order})
    return jsonify({'message': 'Order updated'})

@app.route('/orders/<order_id>', methods=['DELETE'])
def delete_order(order_id):
    orders.delete_one({'_id': ObjectId(order_id)})
    return jsonify({'message': 'Order deleted'})



if __name__ == '__main__':
    app.run(port=5000,debug=True)