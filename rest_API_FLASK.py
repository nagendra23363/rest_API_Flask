from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory storage (dictionary)
# Key: user_id, Value: user details
users = {
    1: {"name": "Oggy", "email": "oggy@example.com"},
    2: {"name": "Jack", "email": "Jack@example.com"}
}

# 1. GET all users
@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users), 200


# 2. GET a single user by ID
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = users.get(user_id)
    if user:
        return jsonify({user_id: user}), 200
    return jsonify({"error": "User not found"}), 404


# 3. POST - Create a new user
@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data or "name" not in data or "email" not in data:
        return jsonify({"error": "Name and email are required"}), 400

    new_id = max(users.keys(), default=0) + 1
    users[new_id] = {"name": data["name"], "email": data["email"]}
    return jsonify({"message": "User created", "user_id": new_id}), 201


# 4. PUT - Update a user
@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    users[user_id].update({
        "name": data.get("name", users[user_id]["name"]),
        "email": data.get("email", users[user_id]["email"])
    })
    return jsonify({"message": "User updated", user_id: users[user_id]}), 200


# 5. DELETE - Remove a user
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    if user_id in users:
        deleted_user = users.pop(user_id)
        return jsonify({"message": "User deleted", "deleted": deleted_user}), 200
    return jsonify({"error": "User not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
