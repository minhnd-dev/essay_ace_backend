import bcrypt
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
conn = sqlite3.connect("test.db", check_same_thread=False)


@app.route('/user/getbyid/<id>', methods=['GET'])
def get_by_id(id):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id=?", id)
        results = []
        keys = [i[0] for i in cursor.description]
        for val in cursor.fetchall():
            results.append(dict(zip(keys, val)))
        resp = jsonify(results)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)


@app.route('/user/add', methods=['POST'])
def add_user():
    try:
        id = request.json.get("id")
        user_name = request.json.get("user_name")
        password = request.json.get("password")
        sql = 'INSERT INTO users(id, user_name, password) VALUES (?, ?, ?)'
        cursor = conn.cursor()
        data = (id, user_name, password)
        cursor.execute(sql, data)
        conn.commit()
        resp = jsonify('Add successfully')
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)


@app.route('/user/edit', methods=['PUT'])
def update_user():
    try:
        id = request.json.get("id")
        user_name = request.json.get("user_name")
        cursor = conn.cursor()
        sql = "update users set user_name = ? where id = ?"
        data = (user_name, id)
        cursor.execute(sql, data)
        conn.commit()
        resp = jsonify({"mess": "success"})
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)


@app.route('/user/delete', methods=['DELETE'])
def delete_user():
    try:
        id = request.json.get("id")
        cursor = conn.cursor()
        sql = "delete users where id = ?"
        data = (id)
        cursor.execute(sql, id)
        conn.commit()
        resp = jsonify({"mess": "success"})
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)


@app.route('/register', methods=['POST'])
def register():
    id = request.json.get("id", None)
    user_name = request.json.get("user_name", None)
    password = request.json.get("password", None)
    if not user_name:
        return "Missing user_name", 400
    if not password:
        return "Missing password", 400
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    sql = 'INSERT INTO users(id, user_name, password) VALUES (?, ?, ?)'
    cursor = conn.cursor()
    data = (id, user_name, hashed)
    cursor.execute(sql, data)
    conn.commit()
    return f"Welcome {user_name}"


@app.route('/login', methods=['POST'])
def login():
    user_name = request.json.get("user_name", None)
    password = request.json.get("password", None)
    if not user_name:
        return "Missing user_name", 400
    if not password:
        return "Missing password", 400
    cursor = conn.cursor()
    user = cursor.execute("SELECT * FROM users WHERE user_name=?", (user_name, ))

    results = []
    keys = [i[0] for i in cursor.description]
    for val in cursor.fetchall():
        results.append(dict(zip(keys, val)))

    if not user:
        return "User not found", 404
    if bcrypt.checkpw(password.encode('utf-8'), results[0]["password"]):
        return f"Welcome back {user_name}"
    else:
        return "Wrong password!"


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
