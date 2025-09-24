import json
import os
from person import Person, Staff
from student import Student, UndergraduateStudent, GraduateStudent, SecureStudentRecord
from faculty import Faculty, Professor, Lecturer, TA
from department import Department, Course

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_FILE = os.path.join(SCRIPT_DIR, 'database.json')

def load_database():
    """Load data from JSON file and convert to objects"""
    if not os.path.exists(DATABASE_FILE):
        return [], [], []
    
    try:
        with open(DATABASE_FILE, 'r') as f:
            data = json.load(f)
        
        # Convert JSON data back to objects
        departments = []
        courses = []
        people = []
        
        # Load people first
        for person_data in data.get('people', []):
            person = create_person_from_data(person_data)
            if person:
                people.append(person)
        
        # Load departments
        for dept_data in data.get('departments', []):
            dept = Department(dept_data['name'])
            # Add faculty and students by ID reference
            for faculty_id in dept_data.get('faculty_ids', []):
                faculty = next((p for p in people if p.id == faculty_id and isinstance(p, Faculty)), None)
                if faculty:
                    dept.add_faculty(faculty)
            for student_id in dept_data.get('student_ids', []):
                student = next((p for p in people if p.id == student_id and isinstance(p, Student)), None)
                if student:
                    dept.add_student(student)
            departments.append(dept)
        
        # Load courses
        for course_data in data.get('courses', []):
            course = Course(
                course_data['name'],
                course_data['code'],
                course_data['max_enrollment'],
                course_data.get('prerequisites', [])
            )
            # Add enrolled students
            for student_id in course_data.get('enrolled_student_ids', []):
                student = next((p for p in people if p.id == student_id and isinstance(p, Student)), None)
                if student:
                    course.enrolled_students.append(student)
            # Assign faculty
            faculty_id = course_data.get('faculty_id')
            if faculty_id:
                faculty = next((p for p in people if p.id == faculty_id and isinstance(p, Faculty)), None)
                if faculty:
                    course.faculty = faculty
            courses.append(course)
        
        return departments, courses, people
    
    except Exception as e:
        print(f"Error loading database: {e}")
        return [], [], []

def create_person_from_data(person_data):
    """Create person object from JSON data"""
    person_type = person_data['type']
    name = person_data['name']
    person_id = person_data['id']
    
    if person_type == 'UndergraduateStudent':
        person = UndergraduateStudent(name, person_id, person_data['major'])
    elif person_type == 'GraduateStudent':
        person = GraduateStudent(name, person_id, person_data['major'])
    elif person_type == 'Professor':
        person = Professor(name, person_id, person_data['department'])
    elif person_type == 'Lecturer':
        person = Lecturer(name, person_id, person_data['department'])
    elif person_type == 'TA':
        person = TA(name, person_id, person_data['department'])
    elif person_type == 'Staff':
        person = Staff(name, person_id)
    else:
        return None
    
    # Load additional data for students
    if isinstance(person, Student):
        person.courses = person_data.get('courses', [])
        person.grades = person_data.get('grades', {})
    
    return person

def save_database(departments, courses, people):
    """Save data to JSON file"""
    try:
        data = {
            'departments': [],
            'courses': [],
            'people': []
        }
        
        # Convert people to JSON
        for person in people:
            person_data = {
                'type': person.__class__.__name__,
                'name': person.name,
                'id': person.id
            }
            
            if isinstance(person, Student):
                person_data['major'] = person.major
                person_data['courses'] = person.courses
                person_data['grades'] = person.grades
            elif isinstance(person, Faculty):
                person_data['department'] = person.department
            
            data['people'].append(person_data)
        
        # Convert departments to JSON
        for dept in departments:
            dept_data = {
                'name': dept.name,
                'faculty_ids': [f.id for f in dept.faculty],
                'student_ids': [s.id for s in dept.students]
            }
            data['departments'].append(dept_data)
        
        # Convert courses to JSON
        for course in courses:
            course_data = {
                'name': course.name,
                'code': course.code,
                'max_enrollment': course.max_enrollment,
                'prerequisites': course.prerequisites,
                'enrolled_student_ids': [s.id for s in course.enrolled_students],
                'faculty_id': course.faculty.id if course.faculty else None
            }
            data['courses'].append(course_data)
        
        with open(DATABASE_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        
        return True
    
    except Exception as e:
        print(f"Error saving database: {e}")
        return False
