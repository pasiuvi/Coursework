from student import Student
from faculty import Faculty
from department import Department, Course

def main():
    """Main function to demonstrate the University Management System."""

    print("--- Setting up University System ---")
    
    # 1. Create Department and Courses
    cs_department = Department("Computer Science")
    math_department = Department("Mathematics")

    course1 = Course("Introduction to Python", "CS101", 3)
    course2 = Course("Data Structures", "CS201", 4)
    course3 = Course("Calculus I", "MATH101", 4)
    
    cs_department.add_course(course1)
    cs_department.add_course(course2)
    math_department.add_course(course3)

    print("\n--- Creating and Managing People ---")

    # 2. Create Student and Faculty instances
    student1 = Student("Alice", 20, "S12345", "Computer Science")
    faculty1 = Faculty("Dr. Smith", 45, "F98765", "Computer Science")

    cs_department.add_student(student1)
    cs_department.add_faculty(faculty1)
    
    # 3. Demonstrate Inheritance from Person class
    print("\n--- A. Demonstrating Inheritance ---")
    print(student1.get_details())
    print(faculty1.get_details())

    # 4. Demonstrate Advanced Student Management
    print("\n--- B. Demonstrating Advanced Student Management ---")
    student1.enroll_course("Introduction to Python", 4.0) # Grade A
    student1.enroll_course("Data Structures", 3.0)      # Grade B
    print(f"{student1.name}'s Enrolled Courses: {student1.courses}")
    
    # Calculate GPA and check status
    gpa = student1.calculate_gpa()
    status = student1.get_academic_status()
    print(f"{student1.name}'s GPA: {gpa:.2f}")
    print(f"{student1.name}'s Academic Status: {status}")
    
    student1.drop_course("Data Structures")
    print(f"{student1.name}'s Current Courses: {student1.courses}")

    # 5. Demonstrate Polymorphism
    print("\n--- D. Demonstrating Polymorphism ---")
    people = [student1, faculty1]
    for person in people:
        # The same method call behaves differently for different objects
        print(f"{person.name}'s Responsibilities: {person.get_responsibilities()}")
        
    # 6. Demonstrate Department and Course Management
    print("\n--- E. Demonstrating Department Management ---")
    faculty1.assign_to_course("Introduction to Python")
    cs_department.get_details()
    math_department.get_details()


if __name__ == "__main__":
    main()