# Why Data Validation is important?
# Ensure that the data submitted to the API adheres to predefined formats, preventing errors and ensuring consistency.

# What is Flask-Marshmallow? 
'''
    Marshmallow helps with object serialization/deserialization and data validation.
    Define a schema using Marshmallow to validate API requests.
'''

from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
# Part 4: from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy # Import SQLAlchemy for ORM
from marshmallow import fields, ValidationError

app = Flask(__name__)
ma = Marshmallow(app)

# Part 4: Configure SQLAlchemy with database connection details
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/database_name'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:rootuser@localhost/student_db'

# Part 4: Initialize SQLAlchemy
db = SQLAlchemy(app)

# Part 4: # Define the Student Model for SQLAlchemy (maps to the students table in the database)
class Student(db.Model):
    __tablename__ = 'students' #Explicitly specify the table name
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=True, unique=True)
    start_date = db.Column(db.Date, nullable=True)

# Student Schema: Ensures that only the specified fields ('id', 'first_name', 'last_name', 'email', 'start_date') are included in the API's input/output and helps validate that incoming data matches this structure.
class StudentSchema(ma.Schema):
    id = fields.Int(dump_only=True) # dump_only means we dont input data for this field
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.Email(required=True)
    start_date = fields.Date()
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email', 'start_date')

# Create instance of schema
student_schema = StudentSchema()
students_schema = StudentSchema(many=True)

# Part 4: Modify all routes to use SQLAlchemy ORM

# Create Route "get_students" & Test GET endpoint with Postman
@app.route('/get_students')
def get_students():
    students = Student.query.all() # Fetch all students from the database
    return jsonify(students_schema.dump(students)) # Serialize and return the students as JSON

# Create Route "add_student" & Test POST endpoint with Postman
@app.route('/add_student', methods = ['POST'])
def add_student():
    # gets our json data
    data = request.get_json()
    # validate json with schema
    errors = student_schema.validate(data)
    # create conditional based on if errors
    if errors:
        return jsonify(errors), 400
    
    # Create a new student object
    new_student = Student(
        first_name=data["first_name"],
        last_name=data['last_name'],
        email=data['email'],
        start_date = data.get('start_date') # Use .get() for optional fields
    )
    db.session.add(new_student) # Add the new student to the session
    db.session.commit() # Commit the changes to the database

    return jsonify({"message":f"New Student: {new_student.first_name} was added to the database!"})
    
# create a dynamic route "get_student" to grab specific data
@app.route('/students/<int:student_id>', methods = ['GET'])
def get_student(student_id):
    student = Student.query.get(student_id) # Fetch the student by ID
    if not student:
        return jsonify({"message": "Student not found!"}), 404
    return jsonify(student_schema.dump(student)) # Serialize and return the student

# create a dynamic route "update_student"
@app.route('/students/<int:student_id>', methods = ['PUT'])
def update_student(student_id):
    # gets our json data
    data = request.get_json()
    # validate json with schema
    errors = student_schema.validate(data)
    # create conditional based on if errors
    if errors:
        return jsonify(errors), 400
    
    student = Student.query.get_or_404(student_id) # Fetch the student by ID
    if not student:
        return jsonify({"message": "Student not found!"}), 404
    
    # Update student fields
    student.first_name = data['first_name']
    student.last_name = data['last_name']
    student.email = data['email']
    student.start_date = data['start_date']

    db.session.commit() # Commit the changes to the database
    return jsonify({"message":f"{student.first_name} has been updated!"})

# create dynamic route "delete_student"
@app.route('/students/<int:student_id>', methods = ['DELETE'])
def delete_student(student_id):
    student = Student.query.get_or_404(student_id) # Fetch the student by ID
    if not student:
        return jsonify({"message": "Student not found!"}), 404
    
    db.session.delete(student) # Mark the student for deletion
    db.session.commit() # Commit the deletion to the database
    return jsonify({"message":f"{student.first_name} has been deleted!"})

# Initialize the database and create tables
with app.app_context():
    db.create_all()

# Main entry point to run the application
if __name__ == '__main__':
    app.run(debug=True) # Run the Flask app in debug mode