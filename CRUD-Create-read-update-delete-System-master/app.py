from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client["student_db"]
collection = db["students"]

@app.route('/')
def index():
    students = collection.find()
    return render_template('index.html', students=students)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        student = {
            'name': request.form['name'],
            'student_id': request.form['student_id'],
            'email': request.form['email'],
            'phone': request.form['phone'],
            'dept': request.form['dept']
        }
        collection.insert_one(student)
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/update/<student_id>', methods=['GET', 'POST'])
def update(student_id):
    student = collection.find_one({'student_id': student_id})
    if request.method == 'POST':
        updated_student = {
            'name': request.form['name'],
            'student_id': request.form['student_id'],
            'email': request.form['email'],
            'phone': request.form['phone'],
            'dept': request.form['dept']
        }
        collection.update_one({'student_id': student_id}, {"$set": updated_student})
        return redirect(url_for('index'))
    return render_template('update.html', student=student)

@app.route('/delete/<student_id>')
def delete(student_id):
    collection.delete_one({'student_id': student_id})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
