import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST', 'db'),
        database=os.environ.get('DB_NAME', 'portal'),
        user=os.environ.get('DB_USER', 'admin'),
        password=os.environ.get('DB_PASSWORD', 'secretpassword'),
        port=os.environ.get('DB_PORT', '5432')
    )
    return conn

# Initialize table on startup
def init_db():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS students (
                roll_no VARCHAR(50) PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                class_name VARCHAR(50) NOT NULL
            );
        ''')
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Database connection failed: {e}")

init_db()

@app.route('/api/students', methods=['GET', 'POST'])
def handle_students():
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        data = request.json
        try:
            cur.execute(
                "INSERT INTO students (roll_no, name, class_name) VALUES (%s, %s, %s)",
                (data['roll_no'], data['name'], data['class_name'])
            )
            conn.commit()
            result = {"roll_no": data['roll_no'], "name": data['name'], "class_name": data['class_name']}
            cur.close()
            conn.close()
            return jsonify(result), 201
        except Exception as e:
            conn.rollback()
            cur.close()
            conn.close()
            return jsonify({"error": str(e)}), 400

    cur.execute("SELECT roll_no, name, class_name FROM students;")
    students_records = cur.fetchall()
    cur.close()
    conn.close()

    students_list = []
    for r in students_records:
        students_list.append({"roll_no": r[0], "name": r[1], "class_name": r[2]})

    return jsonify(students_list)

@app.route('/api/students/<roll_no>', methods=['DELETE'])
def delete_student(roll_no):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM students WHERE roll_no = %s;", (roll_no,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Deleted successfully"}), 200
    except Exception as e:
        cur.close()
        conn.close()
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)