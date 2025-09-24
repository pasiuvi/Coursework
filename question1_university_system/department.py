"""
Department module containing Course and Department classes.

This module defines the core academic structures for managing
courses and departments in the university system.
"""

from typing import List, Optional, Tuple, Any


class Course:
    """
    Represents a course in the university system.
    
    Attributes:
        name (str): The full name of the course.
        code (str): The unique course code.
        max_enrollment (int): Maximum number of students that can enroll.
        prerequisites (List[str]): List of prerequisite course codes.
        enrolled_students (List[Any]): List of enrolled student objects.
        faculty (Optional[Any]): The faculty member assigned to teach the course.
    """
    
    def __init__(self, name: str, code: str, max_enrollment: int, 
                 prerequisites: Optional[List[str]] = None) -> None:
        """
        Initialize a Course instance.
        
        Args:
            name: The full name of the course.
            code: The unique course code.
            max_enrollment: Maximum number of students that can enroll.
            prerequisites: List of prerequisite course codes.
        """
        self.name = name
        self.code = code
        self.max_enrollment = max_enrollment
        self.prerequisites = prerequisites or []
        self.enrolled_students: List[Any] = []
        self.faculty: Optional[Any] = None

    def enroll_student(self, student: Any) -> Tuple[bool, str]:
        """
        Enroll a student in the course with validation.
        
        Args:
            student: The student object to enroll.
            
        Returns:
            A tuple containing (success_status, message).
            success_status is True if enrollment succeeded, False otherwise.
            message contains details about the enrollment result.
        """
        # Check if student is already enrolled
        if student in self.enrolled_students:
            return False, "Student is already enrolled in this course"
        
        # Check enrollment capacity
        current_enrollment = len(self.enrolled_students)
        if current_enrollment >= self.max_enrollment:
            return False, (f"Course is full "
                          f"({current_enrollment}/{self.max_enrollment})")
        
        # Check prerequisites
        missing_prereqs = []
        for prereq in self.prerequisites:
            # Skip generic 'degree' prerequisite for undergraduate students
            if prereq == "degree" and hasattr(student, 'major'):
                continue
            if not hasattr(student, 'courses') or prereq not in student.courses:
                missing_prereqs.append(prereq)
        
        if missing_prereqs:
            return False, f"Missing prerequisites: {', '.join(missing_prereqs)}"
        
        # Enroll the student
        self.enrolled_students.append(student)
        if hasattr(student, 'enroll_course'):
            student.enroll_course(self.code)
        return True, "Enrollment successful"

    def assign_faculty(self, faculty: Any) -> None:
        """
        Assign a faculty member to teach the course.
        
        Args:
            faculty: The faculty member to assign to the course.
        """
        self.faculty = faculty

    def get_enrollment_info(self) -> str:
        """
        Get formatted enrollment information for the course.
        
        Returns:
            A string with enrollment details.
        """
        current = len(self.enrolled_students)
        return f"{self.code}: {current}/{self.max_enrollment} students enrolled"

    def __str__(self) -> str:
        """Return a string representation of the course."""
        return f"Course: {self.name} ({self.code})"

    def __repr__(self) -> str:
        """Return a detailed string representation for debugging."""
        return (f"Course(name='{self.name}', code='{self.code}', "
                f"max_enrollment={self.max_enrollment})")


class Department:
    """
    Represents a department in the university system.
    
    Attributes:
        name (str): The name of the department.
        faculty (List[Any]): List of faculty members in the department.
        courses (List[Course]): List of courses offered by the department.
        students (List[Any]): List of students in the department.
    """
    
    def __init__(self, name: str) -> None:
        """
        Initialize a Department instance.
        
        Args:
            name: The name of the department.
        """
        self.name = name
        self.faculty: List[Any] = []
        self.courses: List[Course] = []
        self.students: List[Any] = []

    def add_faculty(self, faculty: Any) -> None:
        """
        Add a faculty member to the department.
        
        Args:
            faculty: The faculty member to add.
        """
        if faculty not in self.faculty:
            self.faculty.append(faculty)

    def add_course(self, course: Course) -> None:
        """
        Add a course to the department's offerings.
        
        Args:
            course: The course to add to the department.
        """
        if course not in self.courses:
            self.courses.append(course)

    def add_student(self, student: Any) -> None:
        """
        Add a student to the department.
        
        Args:
            student: The student to add to the department.
        """
        if student not in self.students:
            self.students.append(student)

    def remove_faculty(self, faculty: Any) -> bool:
        """
        Remove a faculty member from the department.
        
        Args:
            faculty: The faculty member to remove.
            
        Returns:
            True if the faculty member was removed, False if not found.
        """
        if faculty in self.faculty:
            self.faculty.remove(faculty)
            return True
        return False

    def remove_student(self, student: Any) -> bool:
        """
        Remove a student from the department.
        
        Args:
            student: The student to remove.
            
        Returns:
            True if the student was removed, False if not found.
        """
        if student in self.students:
            self.students.remove(student)
            return True
        return False

    def get_department_stats(self) -> dict:
        """
        Get statistics about the department.
        
        Returns:
            A dictionary containing department statistics.
        """
        return {
            'name': self.name,
            'faculty_count': len(self.faculty),
            'course_count': len(self.courses),
            'student_count': len(self.students)
        }

    def __str__(self) -> str:
        """Return a string representation of the department."""
        return f"Department: {self.name}"

    def __repr__(self) -> str:
        """Return a detailed string representation for debugging."""
        return f"Department(name='{self.name}')"
