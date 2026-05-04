from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# In-memory data store for demonstration
students = [
    {"roll_no": "343", "name": "Aman", "class_name": "5th"}
]
teachers = [
    {"teacher_id": "T101", "name": "Mrs. Sharma", "subject": "Math"}
]

@app.route('/api/students', methods=['GET', 'POST'])
def handle_students():
    if request.method == 'POST':
        data = request.json
        new_student = {
            "roll_no": data.get('roll_no'),
            "name": data.get('name'),
            "class_name": data.get('class_name')
        }
        students.append(new_student)
        return jsonify(new_student), 201
    return jsonify(students)

@app.route('/api/students/<roll_no>', methods=['DELETE'])
def delete_student(roll_no):
    global students
    students = [s for s in students if s['roll_no'] != roll_no]
    return jsonify({"message": "Deleted successfully"}), 200

@app.route('/api/teachers', methods=['GET', 'POST'])
def handle_teachers():
    if request.method == 'POST':
        data = request.json
        new_teacher = {
            "teacher_id": data.get('teacher_id'),
            "name": data.get('name'),
            "subject": data.get('subject')
        }
        teachers.append(new_teacher)
        return jsonify(new_teacher), 201
    return jsonify(teachers)

@app.route('/api/teachers/<teacher_id>', methods=['DELETE'])
def delete_teacher(teacher_id):
    global teachers
    teachers = [t for t in teachers if t['teacher_id'] != teacher_id]
    return jsonify({"message": "Deleted successfully"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)