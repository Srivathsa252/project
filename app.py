from flask import Flask, request, jsonify
import psycopg2
import os
import time

app = Flask(__name__)

# Database connection with retry
def get_db_connection():
    max_retries = 5
    for i in range(max_retries):
        try:
            conn = psycopg2.connect(
                host=os.getenv("DB_HOST", "postgres-service-2022bcd0020-srivathsa"),  # Default value
                database=os.getenv("D       B_NAME", "tasks_db"),
                user=os.getenv("DB_USER", "postgres"),
                password=os.getenv("DB_PASSWORD", "password"),
                port=os.getenv("DB_PORT", "5432")
            )
            return conn
        except psycopg2.OperationalError as e:
            if i < max_retries - 1:
                print(f"Database connection failed, retrying ({i+1}/{max_retries})...")
                time.sleep(5)  # Wait 5 seconds before retrying
            else:
                raise e

# Create table if not exists
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title VARCHAR(100) NOT NULL,
            description TEXT
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

@app.route('/')
def index():
    return "✅ Flask backend is running! Use the /tasks endpoint to interact with the API."

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (title, description) VALUES (%s, %s) RETURNING id;",
                (data['title'], data['description']))
    task_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"id": task_id, "title": data['title'], "description": data['description']}), 201

@app.route('/', methods=['GET'])
def get_tasks():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks;")
    tasks = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{"id": t[0], "title": t[1], "description": t[2]} for t in tasks])

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE tasks SET title = %s, description = %s WHERE id = %s;",
                (data['title'], data['description'], id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"id": id, "title": data['title'], "description": data['description']})

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id = %s;", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": f"Task {id} deleted"})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
