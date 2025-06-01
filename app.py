import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request, jsonify

load_dotenv()

app = Flask(__name__)
url = os.environ.get("DATABASE_URL")
conn = psycopg2.connect(url)

@app.route("/users", methods=["GET"])
def get_users():
    with conn.cursor() as cur:
        cur.execute("SELECT id, name, age FROM users;")
        rows = cur.fetchall()
        users = [{"id": row[0], "name": row[1], "age": row[2]} for row in rows]
    return jsonify(users), 200

@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    name = data.get("name")
    age = data.get("age")
    with conn.cursor() as cur:
        cur.execute("INSERT INTO users (name, age) VALUES (%s, %s) RETURNING id;", (name, age))
        user_id = cur.fetchone()[0]
        conn.commit()
    return jsonify({"id": user_id, "name": name, "age": age}), 201

@app.route("/")
def index():
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                age INT NOT NULL
            );
        """)
        conn.commit()
    return "Hello World!"

if __name__ == "__main__":
    app.run(debug=True)