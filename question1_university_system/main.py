"""
Main demonstration file for the University Management System.
Shows comprehensive functionality and integration of all components.
"""

from person import Person, Staff
from student import Student, UndergraduateStudent, GraduateStudent
from faculty import Faculty, Professor, Lecturer, TA
from course import Course
from department import Department

def demonstrate_inheritance():
    """Demonstrate inheritance hierarchy and method overriding."""
    print("=" * 60)
    print("DEMONSTRATING INHERITANCE AND POLYMORPHISM")
    print("=" * 60)
    
    # Create different person types
    people = [
        UndergraduateStudent("Alice Johnson", "S001", "alice@uni.edu", "Computer Science", 2),
        GraduateStudent("Bob Smith", "S002", "bob@uni.edu", "Data Science", "PhD", "Dr. Wilson"),
        Professor("Dr. Wilson", "F001", "wilson@uni.edu", "Computer Science", "Full"),
        Lecturer("Dr. Brown", "F002", "brown@uni.edu", "Mathematics", "Full-time"),
        TA("Carol Davis", "F003", "carol@uni.edu", "Computer Science", "Dr. Wilson"),
        Staff("David Miller", "E001", "david@uni.edu", "Administrator")
    ]
    
    # Demonstrate polymorphism
    for person in people:
        print(f"{person.__class__.__name__:20} | {person.get_responsibilities()}")
    
    print()

def demonstrate_student_management():
    """Demonstrate advanced student management features."""
    print("=" * 60)
    print("DEMONSTRATING STUDENT MANAGEMENT")
    print("=" * 60)
    
    # Create courses with prerequisites
    cs101 = Course("CS101", "Introduction to Programming", 3, 25)
    cs102 = Course("CS102", "Data Structures", 3, 25, ["CS101"])
    math101 = Course("MATH101", "Calculus I", 4, 30)
    
    # Create student
    student = UndergraduateStudent("Emma Wilson", "S003", "emma@uni.edu", "Computer Science", 1)
    
    # Demonstrate enrollment
    print("Enrollment process:")
    student.enroll_course(cs101)
    student.enroll_course(math101)
    
    # Try to enroll in course without prerequisites
    student.enroll_course(cs102)  # Should fail
    
    # Complete CS101 and then enroll in CS102
    student.complete_course("CS101", 3.7)  # Grade A-
    student.enroll_course(cs102)  # Should now succeed
    
    # Complete another course
    student.complete_course("MATH101", 3.3)  # Grade B+
    
    # Show academic status
    print(f"\nStudent GPA: {student.gpa:.2f}")
    print(f"Academic Status: {student.get_academic_status()}")
    print(f"Completed courses: {list(student.completed_courses.keys())}")

def demonstrate_encapsulation():
    """Demonstrate encapsulation and data validation."""
    print("\n" + "=" * 60)
    print("DEMONSTRATING ENCAPSULATION AND VALIDATION")
    print("=" * 60)
    
    # Test validation in Student class
    student = UndergraduateStudent("Test Student", "S999", "test@uni.edu", "Biology", 1)
    
    # Test valid GPA setting through course completion
    try:
        student.complete_course("BIO101", 3.8)  # Valid grade
        print("✓ Valid grade accepted")
    except ValueError as e:
        print(f"✗ Unexpected error: {e}")
    
    # Test invalid grade
    try:
        student.complete_course("BIO102", 5.0)  # Invalid grade
        print("✗ Invalid grade should have been rejected")
    except ValueError as e:
        print(f"✓ Invalid grade correctly rejected: {e}")
    
    # Test course capacity validation
    small_course = Course("TEST101", "Test Course", 1, 2)  # Only 2 seats
    test_students = [
        UndergraduateStudent(f"Student{i}", f"S{i}", f"s{i}@uni.edu", "Test", 1)
        for i in range(3)
    ]
    
    # Enroll students until capacity is reached
    enrolled_count = 0
    for s in test_students:
        if small_course.enroll_student(s):
            enrolled_count += 1
            print(f"✓ Enrolled student {s.person_id}")
        else:
            print(f"✗ Could not enroll student {s.person_id} - course full")
    
    print(f"Final enrollment: {enrolled_count}/{small_course.max_capacity}")

def demonstrate_department_management():
    """Demonstrate comprehensive department management."""
    print("\n" + "=" * 60)
    print("DEMONSTRATING DEPARTMENT MANAGEMENT")
    print("=" * 60)
    
    # Create computer science department
    cs_dept = Department("Computer Science", "CS")
    
    # Create faculty
    prof = Professor("Dr. Adams", "F010", "adams@uni.edu", "Computer Science", "Associate")
    lecturer = Lecturer("Dr. Baker", "F011", "baker@uni.edu", "Computer Science", "Full-time")
    
    # Create courses
    courses = [
        Course("CS101", "Programming Fundamentals", 3, 30),
        Course("CS201", "Algorithms", 3, 25, ["CS101"]),
        Course("CS301", "Machine Learning", 3, 20, ["CS201"])
    ]
    
    # Create students
    students = [
        UndergraduateStudent("Frank Lee", "S010", "frank@uni.edu", "Computer Science", 2),
        GraduateStudent("Grace Kim", "S011", "grace@uni.edu", "AI", "Masters", "Dr. Adams")
    ]
    
    # Add everything to department
    cs_dept.add_faculty(prof)
    cs_dept.add_faculty(lecturer)
    
    for course in courses:
        cs_dept.add_course(course)
    
    for student in students:
        cs_dept.add_student(student)
    
    # Assign faculty to courses
    prof.assign_course(courses[2])  # Machine Learning
    lecturer.assign_course(courses[0])  # Programming Fundamentals
    
    # Enroll students
    students[0].enroll_course(courses[0])
    students[1].enroll_course(courses[2])
    
    # Demonstrate department statistics
    stats = cs_dept.get_department_stats()
    print("Department Statistics:")
    for key, value in stats.items():
        if key not in ['courses', 'faculty']:  # Skip long lists for brevity
            print(f"  {key}: {value}")
    
    print("\nCourse Availability:")
    for course_info in cs_dept.list_courses_with_availability():
        print(f"  {course_info['course_code']}: {course_info['enrolled']}/{course_info['capacity']}")

def demonstrate_workload_calculation():
    """Demonstrate polymorphism in workload calculation."""
    print("\n" + "=" * 60)
    print("DEMONSTRATING WORKLOAD CALCULATION POLYMORPHISM")
    print("=" * 60)
    
    # Create different faculty types
    prof = Professor("Dr. Clark", "F020", "clark@uni.edu", "Physics", "Full")
    lecturer = Lecturer("Dr. Davis", "F021", "davis@uni.edu", "Physics", "Part-time")
    ta = TA("Eve Johnson", "F022", "eve@uni.edu", "Physics", "Dr. Clark")
    
    # Create courses
    physics_courses = [
        Course("PHY101", "Classical Mechanics", 3, 30),
        Course("PHY102", "Electromagnetism", 3, 25)
    ]
    
    # Assign courses and additional responsibilities
    prof.assign_course(physics_courses[0])
    prof.add_research_grant("Quantum Computing Research")
    prof.add_advisee(GraduateStudent("Mike", "S020", "mike@uni.edu", "Physics", "PhD"))
    
    lecturer.assign_course(physics_courses[1])
    
    ta.assign_course(physics_courses[0])
    ta.assign_lab_section("PHY101-Lab1")
    ta.assign_grading("PHY101 Midterm")
    
    faculty_members = [prof, lecturer, ta]
    
    for faculty in faculty_members:
        workload = faculty.calculate_workload()
        print(f"{faculty.__class__.__name__:12} | Workload: {workload:2d} | {faculty.get_responsibilities()}")

def main():
    """Main demonstration function."""
    print("UNIVERSITY MANAGEMENT SYSTEM DEMONSTRATION")
    print("=" * 60)
    
    # Run all demonstrations
    demonstrate_inheritance()
    demonstrate_student_management()
    demonstrate_encapsulation()
    demonstrate_department_management()
    demonstrate_workload_calculation()
    
    print("\n" + "=" * 60)
    print("DEMONSTRATION COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()