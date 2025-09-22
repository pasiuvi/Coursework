"""
Department class for managing university department structure.
Handles faculty, courses, and students within a department.
"""

from typing import List, Dict
from course import Course

class Department:
    """
    Represents a university department with faculty, courses, and students.
    Demonstrates comprehensive management capabilities.
    """
    
    def __init__(self, name: str, code: str):
        """
        Initialize a department.
        
        Args:
            name (str): Department name (e.g., "Computer Science")
            code (str): Department code (e.g., "CS")
        """
        self._name = name
        self._code = code
        self._faculty = []  # List of Faculty objects
        self._courses = []  # List of Course objects
        self._students = []  # List of Student objects
    
    def add_faculty(self, faculty) -> bool:
        """Add a faculty member to the department."""
        if faculty not in self._faculty:
            self._faculty.append(faculty)
            faculty.department = self._name
            return True
        return False
    
    def add_course(self, course: Course) -> bool:
        """Add a course to the department's offerings."""
        if course not in self._courses:
            self._courses.append(course)
            return True
        return False
    
    def add_student(self, student) -> bool:
        """Add a student to the department."""
        if student not in self._students:
            self._students.append(student)
            student.department = self._name
            return True
        return False
    
    def get_course_by_code(self, course_code: str) -> Course:
        """Retrieve a course by its code."""
        for course in self._courses:
            if course.course_code == course_code:
                return course
        raise ValueError(f"Course {course_code} not found in department")
    
    def get_faculty_by_id(self, faculty_id: str):
        """Retrieve a faculty member by ID."""
        for faculty in self._faculty:
            if faculty.person_id == faculty_id:
                return faculty
        return None
    
    def get_student_by_id(self, student_id: str):
        """Retrieve a student by ID."""
        for student in self._students:
            if student.person_id == student_id:
                return student
        return None
    
    def get_department_stats(self) -> dict:
        """Return comprehensive department statistics."""
        return {
            'name': self._name,
            'code': self._code,
            'faculty_count': len(self._faculty),
            'course_count': len(self._courses),
            'student_count': len(self._students),
            'courses': [course.course_code for course in self._courses],
            'faculty': [f.name for f in self._faculty]
        }
    
    def list_courses_with_availability(self) -> List[dict]:
        """List all courses with their enrollment status."""
        return [course.get_enrollment_info() for course in self._courses]
    
    # Property getters
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def code(self) -> str:
        return self._code
    
    @property
    def faculty(self) -> List:
        return self._faculty.copy()
    
    @property
    def courses(self) -> List[Course]:
        return self._courses.copy()
    
    @property
    def students(self) -> List:
        return self._students.copy()
    
    def __str__(self) -> str:
        return f"{self._name} Department ({self._code})"
    
    def __repr__(self) -> str:
        return f"Department('{self._name}', '{self._code}')"