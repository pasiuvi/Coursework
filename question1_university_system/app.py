from flask import Flask, render_template, request, redirect, url_for
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
    return render_template('home.html', departments=departments, courses=courses, people=people)

@app.route('/add_department', methods=['GET', 'POST'])
def add_department():
    if request.method == 'POST':
        name = request.form['name']
        dept = Department(name)
        departments.append(dept)
        save_database(departments, courses, people)
        return redirect(url_for('home'))
    return render_template('add_department.html')

@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        name = request.form['name']
        code = request.form['code']
        max_enrollment = int(request.form['max_enrollment'])
        prereqs = request.form.get('prerequisites', '').split(',') if request.form.get('prerequisites') else []
        course = Course(name, code, max_enrollment, prereqs)
        courses.append(course)
        save_database(departments, courses, people)
        return redirect(url_for('home'))
    return render_template('add_course.html')

@app.route('/add_person', methods=['GET', 'POST'])
def add_person():
    if request.method == 'POST':
        person_type = request.form['type']
        name = request.form['name']
        person_id = request.form['id']
        if person_type == 'student':
            major = request.form['major']
            subtype = request.form['subtype']
            if subtype == 'undergrad':
                person = UndergraduateStudent(name, person_id, major)
            else:
                person = GraduateStudent(name, person_id, major)
        elif person_type == 'faculty':
            department = request.form['department']
            subtype = request.form['subtype']
            if subtype == 'professor':
                person = Professor(name, person_id, department)
            elif subtype == 'lecturer':
                person = Lecturer(name, person_id, department)
            else:
                person = TA(name, person_id, department)
        else:
            person = Staff(name, person_id)
        people.append(person)
        save_database(departments, courses, people)
        return redirect(url_for('home'))
    return render_template('add_person.html')

@app.route('/enroll', methods=['GET', 'POST'])
def enroll():
    if request.method == 'POST':
        student_id = request.form['student_id']
        course_code = request.form['course_code']
        student = next((p for p in people if isinstance(p, Student) and p.id == student_id), None)
        course = next((c for c in courses if c.code == course_code), None)
        if student and course:
            course.enroll_student(student)
        save_database(departments, courses, people)
        return redirect(url_for('home'))
    students = [p for p in people if isinstance(p, Student)]
    return render_template('enroll.html', students=students, courses=courses)

@app.route('/manage_grades', methods=['GET', 'POST'])
def manage_grades():
    if request.method == 'POST':
        student_id = request.form['student_id']
        course_code = request.form['course_code']
        grade = float(request.form['grade'])
        student = next((p for p in people if isinstance(p, Student) and p.id == student_id), None)
        if student and 0.0 <= grade <= 4.0:
            student.grades[course_code] = grade
        save_database(departments, courses, people)
        return redirect(url_for('manage_grades'))
    students = [p for p in people if isinstance(p, Student)]
    return render_template('manage_grades.html', students=students, courses=courses)

@app.route('/student_details/<student_id>')
def student_details(student_id):
    student = next((p for p in people if isinstance(p, Student) and p.id == student_id), None)
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
        faculty = next((p for p in people if isinstance(p, Faculty) and p.id == faculty_id), None)
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
    return render_template('faculty_workload.html', faculty_members=faculty_members)

@app.route('/drop_course', methods=['GET', 'POST'])
def drop_course():
    if request.method == 'POST':
        student_id = request.form['student_id']
        course_code = request.form['course_code']
        student = next((p for p in people if isinstance(p, Student) and p.id == student_id), None)
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
    return render_template('department_management.html', departments=departments, people=people)

@app.route('/assign_to_department', methods=['POST'])
def assign_to_department():
    dept_name = request.form['department']
    person_id = request.form['person_id']
    department = next((d for d in departments if d.name == dept_name), None)
    person = next((p for p in people if p.id == person_id), None)
    if department and person:
        if isinstance(person, Student):
            department.add_student(person)
        elif isinstance(person, Faculty):
            department.add_faculty(person)
    save_database(departments, courses, people)
    return redirect(url_for('department_management'))

@app.route('/database_admin')
def database_admin():
    return render_template('database_admin.html', departments=departments, courses=courses, people=people)

@app.route('/reset_database', methods=['POST'])
def reset_database():
    global departments, courses, people
    departments.clear()
    courses.clear()
    people.clear()
    save_database(departments, courses, people)
    return redirect(url_for('database_admin'))

@app.route('/load_sample_data', methods=['POST'])
def load_sample_data():
    from init_data import initialize_sample_data
    initialize_sample_data()
    global departments, courses, people
    departments, courses, people = load_database()
    return redirect(url_for('database_admin'))

if __name__ == '__main__':
    app.run(debug=True)
