import bcrypt
from flask import Flask, request, url_for, jsonify, make_response, redirect
import flask
import pyodbc

app = Flask(__name__)
con_str = "DRIVER={SQL Server};SERVER=LAPTOP-IP4EHMEC\\SQLEXPRESS;DATABASE=easy_ace;Trusted_Connection=yes"
conn = pyodbc.connect(con_str)
app.config['SECRET_KEY'] = 'thisisthesecretkey'


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route('/user/getbyid/<id>', methods=['GET'])
def get_by_id(id):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE id=?", id)
        results = []
        keys = [i[0] for i in cursor.description]
        for val in cursor.fetchall():
            results.append(dict(zip(keys, val)))
        resp = flask.jsonify(results)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)


@app.route('/user/add', methods=['POST'])
def add_user():
    try:
        id = flask.request.json.get("id")
        username = flask.request.json.get("username")
        password = flask.request.json.get("password")
        sql = 'INSERT INTO Users(id, username, password) VALUES (?, ?, ?)'
        cursor = conn.cursor()
        data = (id, username, password)
        cursor.execute(sql, data)
        conn.commit()
        resp = flask.jsonify('Add successfully')
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)


@app.route('/user/edit', methods=['PUT'])
def update_user():
    try:
        id = flask.request.json.get("id")
        username = flask.request.json.get("username")
        cursor = conn.cursor()
        sql = "update Users set username = ? where id = ?"
        data = (username, id)
        cursor.execute(sql, data)
        conn.commit()
        resp = flask.jsonify({"mess": "success"})
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)


@app.route('/user/delete', methods=['DELETE'])
def delete_user():
    try:
        id = flask.request.json.get("id")
        cursor = conn.cursor()
        sql = "delete Users where id = ?"
        data = (id)
        cursor.execute(sql, id)
        conn.commit()
        resp = flask.jsonify({"mess": "success"})
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)

@app.route('/register', methods = ['POST'])
def register():
    id = request.json.get("id", None)
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if not username:
        return "Missing username", 400
    if not password:
        return "Missing password", 400
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    sql = 'INSERT INTO Users(id, username, password) VALUES (?, ?, ?)'
    cursor = conn.cursor()
    data = (id, username, hashed)
    cursor.execute(sql, data)
    conn.commit()
    return f"Welcome {username}"

@app.route('/login', methods = ['POST'])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if not username:
        return "Missing username", 400
    if not password:
        return "Missing password", 400
    cursor = conn.cursor()
    user = cursor.execute("SELECT * FROM Users WHERE username=?", username)

    results = []
    keys = [i[0] for i in cursor.description]
    for val in cursor.fetchall():
        results.append(dict(zip(keys, val)))

    if not user:
        return "User not found", 404
    if bcrypt.checkpw(password.encode('utf-8'), results[0]["password"].encode('utf-8')) == results[0]["password"].encode('utf-8'):
        return f"Welcome back {username}"
    else:
        return "Wrong password!"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
