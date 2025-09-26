"""
Flask web application for the university management system.

This module provides a web interface for managing university data
including departments, courses, faculty, and students.
"""

from flask import Flask, render_template, request, redirect, url_for
from typing import Optional, List, Any

from person import Person, Staff
from student import Student, UndergraduateStudent, GraduateStudent, SecureStudentRecord
from faculty import Faculty, Professor, Lecturer, TA
from department import Department, Course
from database_manager import load_database, save_database

app = Flask(__name__)

# Load data from JSON database
departments, courses, people = load_database()


@app.route('/')
def home():
    """
    Home page displaying all departments, courses, and people.
    
    Returns:
        Rendered home template with university data.
    """
    return render_template('home.html', 
                         departments=departments, 
                         courses=courses, 
                         people=people)


@app.route('/add_department', methods=['GET', 'POST'])
def add_department():
    """
    Add a new department to the system.
    
    Returns:
        GET: Rendered add_department template.
        POST: Redirect to home page after adding department.
    """
    if request.method == 'POST':
        name = request.form['name']
        if name:  # Basic validation
            dept = Department(name)
            departments.append(dept)
            save_database(departments, courses, people)
        return redirect(url_for('home'))
    return render_template('add_department.html')


@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    """
    Add a new course to the system.
    
    Returns:
        GET: Rendered add_course template with existing courses.
        POST: Redirect to home page after adding course.
    """
    if request.method == 'POST':
        name = request.form['name']
        code = request.form['code']
        try:
            max_enrollment = int(request.form['max_enrollment'])
        except ValueError:
            max_enrollment = 30  # Default value if conversion fails
        
        # Get prerequisites from dropdown selection only
        prereqs = request.form.getlist('prerequisite_courses')
        
        course = Course(name, code, max_enrollment, prereqs)
        courses.append(course)
        save_database(departments, courses, people)
        return redirect(url_for('home'))
    
    # Pass existing courses to the template for prerequisite selection
    return render_template('add_course.html', existing_courses=courses)


@app.route('/add_person', methods=['GET', 'POST'])
def add_person():
    """
    Add a new person (student, faculty, or staff) to the system.
    
    Returns:
        GET: Rendered add_person template with departments.
        POST: Redirect to home page after adding person.
    """
    if request.method == 'POST':
        person_type = request.form['type']
        name = request.form['name']
        person_id = request.form['id']
        
        print(f"DEBUG: Adding person - Type: {person_type}, Name: {name}, ID: {person_id}")
        
        person = None
        if person_type == 'student':
            major = request.form['major']
            subtype = request.form['student_subtype']
            if subtype == 'undergrad':
                person = UndergraduateStudent(name, person_id, major)
            else:
                person = GraduateStudent(name, person_id, major)
        elif person_type == 'faculty':
            department = request.form['department']
            subtype = request.form['faculty_subtype']
            if subtype == 'professor':
                person = Professor(name, person_id, department)
            elif subtype == 'lecturer':
                person = Lecturer(name, person_id, department)
            elif subtype == 'ta':
                person = TA(name, person_id, department)
            else:
                # Fallback - this shouldn't happen with proper form values
                person = TA(name, person_id, department)
        elif person_type == 'staff':
            # Get staff department (default to Administration if not provided)
            staff_department = request.form.get('staff_department', 'Administration')
            person = Staff(name, person_id, staff_department)
        else:
            # Fallback for unknown types
            person = Staff(name, person_id)
        
        if person:
            people.append(person)
            print(f"DEBUG: Person created and added: {person}")
            success = save_database(departments, courses, people)
            print(f"DEBUG: Database save result: {success}")
        else:
            print("DEBUG: Failed to create person!")
        return redirect(url_for('home'))
    
    # Pass departments to the template for dropdown selection
    return render_template('add_person.html', departments=departments)


@app.route('/enroll', methods=['GET', 'POST'])
def enroll():
    """
    Enroll a student in a course.
    
    Returns:
        GET: Rendered enroll template with students and courses.
        POST: Rendered enroll template with enrollment result message.
    """
    message = None
    message_type = None
    
    if request.method == 'POST':
        student_id = request.form['student_id']
        course_code = request.form['course_code']
        student = next((p for p in people 
                       if isinstance(p, Student) and p.person_id == student_id), None)
        course = next((c for c in courses if c.code == course_code), None)
        
        if not student:
            message = f"Student with ID {student_id} not found"
            message_type = "error"
        elif not course:
            message = f"Course with code {course_code} not found"
            message_type = "error"
        else:
            success, msg = course.enroll_student(student)
            message = msg
            message_type = "success" if success else "error"
            
            if success:
                save_database(departments, courses, people)
        
        return render_template('enroll.html', students=[p for p in people if isinstance(p, Student)], 
                             courses=courses, message=message, message_type=message_type)
    
    students = [p for p in people if isinstance(p, Student)]
    return render_template('enroll.html', students=students, courses=courses)

@app.route('/manage_grades', methods=['GET', 'POST'])
def manage_grades():
    if request.method == 'POST':
        student_id = request.form['student_id']
        course_code = request.form['course_code']
        grade = float(request.form['grade'])
        student = next((p for p in people if isinstance(p, Student) and p.person_id == student_id), None)
        if student and 0.0 <= grade <= 4.0:
            student.grades[course_code] = grade
        save_database(departments, courses, people)
        return redirect(url_for('manage_grades'))
    students = [p for p in people if isinstance(p, Student)]
    return render_template('manage_grades.html', students=students, courses=courses)

@app.route('/student_details/<student_id>')
def student_details(student_id):
    student = next((p for p in people if isinstance(p, Student) and p.person_id == student_id), None)
    if student:
        try:
            secure_record = SecureStudentRecord(student)
            return render_template('student_details.html', student=student, secure_record=secure_record)
        except Exception:
            return render_template('student_details.html', student=student, secure_record=None)
    return redirect(url_for('home'))

@app.route('/assign_faculty', methods=['GET', 'POST'])
def assign_faculty():
    if request.method == 'POST':
        faculty_id = request.form['faculty_id']
        course_code = request.form['course_code']
        faculty = next((p for p in people if isinstance(p, Faculty) and p.person_id == faculty_id), None)
        course = next((c for c in courses if c.code == course_code), None)
        if faculty and course:
            course.assign_faculty(faculty)
        save_database(departments, courses, people)
        return redirect(url_for('home'))
    faculty_members = [p for p in people if isinstance(p, Faculty)]
    return render_template('assign_faculty.html', faculty_members=faculty_members, courses=courses)

@app.route('/faculty_workload')
def faculty_workload():
    faculty_members = [p for p in people if isinstance(p, Faculty)]
    return render_template('faculty_workload.html', faculty_members=faculty_members, courses=courses)

@app.route('/drop_course', methods=['GET', 'POST'])
def drop_course():
    if request.method == 'POST':
        student_id = request.form['student_id']
        course_code = request.form['course_code']
        student = next((p for p in people if isinstance(p, Student) and p.person_id == student_id), None)
        course = next((c for c in courses if c.code == course_code), None)
        if student and course:
            student.drop_course(course_code)
            if student in course.enrolled_students:
                course.enrolled_students.remove(student)
        save_database(departments, courses, people)
        return redirect(url_for('home'))
    students = [p for p in people if isinstance(p, Student)]
    return render_template('drop_course.html', students=students)

@app.route('/department_management')
def department_management():
    return render_template('department_management.html', departments=departments, people=people, courses=courses)

@app.route('/assign_course_to_department', methods=['POST'])
def assign_course_to_department():
    dept_name = request.form['department']
    course_code = request.form['course_code']
    department = next((d for d in departments if d.name == dept_name), None)
    course = next((c for c in courses if c.code == course_code), None)
    if department and course:
        if course not in department.courses:
            department.add_course(course)
    save_database(departments, courses, people)
    return redirect(url_for('department_management'))

@app.route('/assign_to_department', methods=['POST'])
def assign_to_department():
    dept_name = request.form['department']
    person_id = request.form['person_id']
    department = next((d for d in departments if d.name == dept_name), None)
    person = next((p for p in people if p.person_id == person_id), None)
    if department and person:
        if isinstance(person, Student):
            department.add_student(person)
        elif isinstance(person, Faculty):
            department.add_faculty(person)
    save_database(departments, courses, people)
    return redirect(url_for('department_management'))

@app.route('/database_admin')
def database_admin():
    """
    Display database administration interface.
    
    Returns:
        Rendered database_admin template with all database objects.
    """
    return render_template('database_admin.html', 
                         departments=departments, 
                         courses=courses, 
                         people=people)


@app.route('/reset_database', methods=['POST'])
def reset_database():
    """
    Reset the database by clearing all data.
    
    Returns:
        Redirect to database_admin page.
    """
    global departments, courses, people
    departments.clear()
    courses.clear()
    people.clear()
    save_database(departments, courses, people)
    return redirect(url_for('database_admin'))


@app.route('/load_sample_data', methods=['POST'])
def load_sample_data():
    """
    Load sample data into the database.
    
    Returns:
        Redirect to database_admin page.
    """
    # This would require an init_data module which isn't available
    # For now, we'll just redirect back
    return redirect(url_for('database_admin'))


def main():
    """Main function to run the Flask application."""
    app.run(debug=True)


if __name__ == '__main__':
    main()
