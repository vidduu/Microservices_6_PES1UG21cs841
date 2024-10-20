from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://mongo:27017/"
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

client = MongoClient("mongodb://mongo:27017/")
db = client.ecommerce
users = db.users

@app.route('/')
def hello_geek():
    return '<h1>Users Microservice working</h2>'

@app.route('/getallusers', methods=['GET'])
def get_users():
    users = db.users.find()
    users_list = []
    for user in users:
        user['_id'] = str(user['_id'])
        users_list.append(user)
    return jsonify(users_list)

@app.route('/users', methods=['POST'])
def create_user():
    new_user = request.json
    user_id = users.insert_one(new_user).inserted_id
    return jsonify({'user_id': str(user_id)})


@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = db.users.find_one({'_id': ObjectId(user_id)})
    if user is None:
        return jsonify({'error': 'User not found'})
    
    user['_id'] = str(user['_id'])
    return jsonify(user)

@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    updated_user = request.json
    users.update_one({'_id': ObjectId(user_id)}, {'$set': updated_user})
    return jsonify({'message': 'User updated'})

@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    users.delete_one({'_id': ObjectId(user_id)})
    return jsonify({'message': 'User deleted'})



if __name__ == '__main__':
    app.run(debug=True,port=5100)
