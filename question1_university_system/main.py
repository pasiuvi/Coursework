from person import Person, Staff
from student import Student, UndergraduateStudent, GraduateStudent, SecureStudentRecord
from faculty import Faculty, Professor, Lecturer, TA
from department import Department, Course

# Create department
cs_dept = Department("Computer Science")

# Create faculty
prof = Professor("Dr. Smith", "F001", "CS")
lect = Lecturer("Ms. Johnson", "F002", "CS")
ta = TA("Alex Brown", "F003", "CS")

cs_dept.add_faculty(prof)
cs_dept.add_faculty(lect)
cs_dept.add_faculty(ta)

# Create courses
intro_cs = Course("Introduction to CS", "CS101", 50)
adv_cs = Course("Advanced CS", "CS201", 30, ["CS101"])

cs_dept.add_course(intro_cs)
cs_dept.add_course(adv_cs)

# Assign faculty to courses
intro_cs.assign_faculty(prof)
adv_cs.assign_faculty(lect)

# Create students
undergrad = UndergraduateStudent("John Doe", "S001", "CS")
grad = GraduateStudent("Jane Doe", "S002", "CS")

cs_dept.add_student(undergrad)
cs_dept.add_student(grad)

# Enroll students
undergrad.enroll_course("CS101")
grad.enroll_course("CS101")
grad.enroll_course("CS201")

# Simulate grades
undergrad.grades["CS101"] = 3.5
grad.grades["CS101"] = 4.0
grad.grades["CS201"] = 3.8

# Secure record
secure_undergrad = SecureStudentRecord(undergrad)

# Demonstrate polymorphism
people = [prof, lect, ta, undergrad, grad]

print("Responsibilities:")
for person in people:
    print(f"{person.name} ({person.__class__.__name__}): {person.get_responsibilities()}")

print("\nWorkloads for faculty:")
for fac in [prof, lect, ta]:
    print(f"{fac.name}: {fac.calculate_workload()}")

print(f"\n{undergrad.name} GPA: {undergrad.calculate_gpa()}")
print(f"{undergrad.name} Status: {undergrad.get_academic_status()}")

print(f"\nSecure Record: {secure_undergrad.get_student_info()}")

# Try invalid GPA
try:
    secure_undergrad.gpa = 5.0
except ValueError as e:
    print(f"Error: {e}")
