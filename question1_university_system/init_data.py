"""
Initialize sample data for the university system
"""
from person import Person, Staff
from student import Student, UndergraduateStudent, GraduateStudent, SecureStudentRecord
from faculty import Faculty, Professor, Lecturer, TA
from department import Department, Course
from database_manager import save_database

def initialize_sample_data():
    """Initialize the database with sample data"""
    # Clear existing data and create sample data
    departments = []
    courses = []
    people = []
    
    # Create sample departments
    cs_dept = Department("Computer Science")
    math_dept = Department("Mathematics")
    phys_dept = Department("Physics")
    departments.extend([cs_dept, math_dept, phys_dept])
    
    # Create sample courses
    cs101 = Course("Introduction to Programming", "CS101", 30, [])
    cs201 = Course("Data Structures", "CS201", 25, ["CS101"])
    math101 = Course("Calculus I", "MATH101", 40, [])
    math201 = Course("Linear Algebra", "MATH201", 35, ["MATH101"])
    phys101 = Course("Physics I", "PHYS101", 30, ["MATH101"])
    courses.extend([cs101, cs201, math101, math201, phys101])
    
    # Create sample faculty
    prof_smith = Professor("Dr. John Smith", "F001", "Computer Science", 15)
    prof_johnson = Professor("Dr. Sarah Johnson", "F002", "Mathematics", 12)
    lecturer_brown = Lecturer("Ms. Emily Brown", "F003", "Computer Science", 8)
    ta_wilson = TA("Mike Wilson", "F004", "Computer Science", 2)
    people.extend([prof_smith, prof_johnson, lecturer_brown, ta_wilson])
    
    # Create sample students
    undergrad1 = UndergraduateStudent("Alice Cooper", "S001", "Computer Science")
    undergrad2 = UndergraduateStudent("Bob Davis", "S002", "Mathematics")
    grad1 = GraduateStudent("Charlie Evans", "S003", "Computer Science", "Machine Learning")
    grad2 = GraduateStudent("Diana Foster", "S004", "Physics", "Quantum Computing")
    people.extend([undergrad1, undergrad2, grad1, grad2])
    
    # Assign faculty to departments
    cs_dept.add_faculty(prof_smith)
    cs_dept.add_faculty(lecturer_brown)
    cs_dept.add_faculty(ta_wilson)
    math_dept.add_faculty(prof_johnson)
    
    # Assign students to departments
    cs_dept.add_student(undergrad1)
    cs_dept.add_student(grad1)
    math_dept.add_student(undergrad2)
    phys_dept.add_student(grad2)
    
    # Assign faculty to courses
    cs101.assign_faculty(prof_smith)
    cs201.assign_faculty(prof_smith)
    math101.assign_faculty(prof_johnson)
    math201.assign_faculty(prof_johnson)
    phys101.assign_faculty(prof_johnson)  # Cross-department teaching
    
    # Enroll students in courses
    try:
        cs101.enroll_student(undergrad1)
        cs101.enroll_student(undergrad2)  # Cross-department enrollment
        cs201.enroll_student(grad1)
        math101.enroll_student(undergrad1)
        math101.enroll_student(undergrad2)
        math201.enroll_student(grad1)
        phys101.enroll_student(grad2)
    except Exception as e:
        print(f"Warning: Could not enroll some students: {e}")
    
    # Save the sample data to the database
    save_database(departments, courses, people)
    print("Sample data initialized successfully!")