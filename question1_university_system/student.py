from person import Person

class Student(Person):
    def __init__(self, name, id, major):
        super().__init__(name, id)
        self.major = major
        self.courses = []
        self.grades = {}  # course_code: grade

    def enroll_course(self, course_code):
        if course_code not in self.courses:
            self.courses.append(course_code)

    def drop_course(self, course_code):
        if course_code in self.courses:
            self.courses.remove(course_code)

    def calculate_gpa(self):
        if not self.grades:
            return 0.0
        total = sum(self.grades.values())
        return total / len(self.grades)

    def get_academic_status(self):
        gpa = self.calculate_gpa()
        if gpa >= 3.5:
            return "Dean's List"
        elif gpa >= 2.0:
            return "Good Standing"
        else:
            return "Probation"

    def get_responsibilities(self):
        return "Study and attend classes"


class UndergraduateStudent(Student):
    pass


class GraduateStudent(Student):
    pass


class SecureStudentRecord:
    def __init__(self, student):
        self.__student = student
        self.__gpa = student.calculate_gpa()

    @property
    def gpa(self):
        return self.__gpa

    @gpa.setter
    def gpa(self, value):
        if 0.0 <= value <= 4.0:
            self.__gpa = value
        else:
            raise ValueError("GPA must be between 0.0 and 4.0")

    def get_student_info(self):
        return f"Name: {self.__student.name}, ID: {self.__student.id}, GPA: {self.__gpa}"
