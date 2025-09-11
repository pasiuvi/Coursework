class Course:
    """A class to represent a university course."""
    def __init__(self, course_name, course_code, credits):
        """
        Initializes a Course object.
        Args:
            course_name (str): The name of the course.
            course_code (str): The unique code for the course.
            credits (int): The number of credits for the course.
        """
        self.course_name = course_name
        self.course_code = course_code
        self.credits = credits

class Department:
    """A class to represent a university department."""
    def __init__(self, department_name):
        """
        Initializes a Department object.
        Args:
            department_name (str): The name of the department.
        """
        self.department_name = department_name
        self.courses = {}
        self.faculty = []
        self.students = []

    def add_course(self, course):
        """Adds a course to the department."""
        if course.course_code not in self.courses:
            self.courses[course.course_code] = course.course_name
            print(f"Course '{course.course_name}' added to the {self.department_name} department.")

    def add_faculty(self, faculty_member):
        """Adds a faculty member to the department."""
        self.faculty.append(faculty_member)
        print(f"Faculty member {faculty_member.name} added to the {self.department_name} department.")

    def add_student(self, student):
        """Adds a student to the department."""
        self.students.append(student)
        print(f"Student {student.name} added to the {self.department_name} department.")

    def get_details(self):
        """Prints the details of the department."""
        print("-" * 30)
        print(f"Department: {self.department_name}")
        
        # Print courses
        course_names = list(self.courses.values())
        print(f"Courses offered: {', '.join(course_names) if course_names else 'None'}")

        # Print faculty
        faculty_names = [f.name for f in self.faculty]
        print(f"Faculty members: {', '.join(faculty_names) if faculty_names else 'None'}")
        
        # Print students
        student_names = [s.name for s in self.students]
        print(f"Students enrolled: {', '.join(student_names) if student_names else 'None'}")
        print("-" * 30)