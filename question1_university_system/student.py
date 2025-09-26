"""
Student module containing student-related classes.

This module defines various student types and secure record handling
for the university management system.
"""

from typing import Dict, List, Any
from person import Person


class Student(Person):
    """
    Base class for all student types in the university system.
    
    Attributes:
        name (str): The student's full name.
        person_id (str): Unique identifier for the student.
        major (str): The student's major field of study.
        courses (List[str]): List of enrolled course codes.
        grades (Dict[str, float]): Dictionary mapping course codes to grades.
    """
    
    def __init__(self, name: str, person_id: str, major: str) -> None:
        """
        Initialize a Student instance.
        
        Args:
            name: The student's full name.
            person_id: Unique identifier for the student.
            major: The student's major field of study.
        """
        super().__init__(name, person_id)
        self.major = major
        self.courses: List[str] = []
        self.grades: Dict[str, float] = {}

    def enroll_course(self, course_code: str) -> None:
        """
        Enroll the student in a course.
        
        Args:
            course_code: The code of the course to enroll in.
        """
        if course_code not in self.courses:
            self.courses.append(course_code)

    def drop_course(self, course_code: str) -> None:
        """
        Drop a course for the student.
        
        Args:
            course_code: The code of the course to drop.
        """
        if course_code in self.courses:
            self.courses.remove(course_code)
            # Also remove grade if it exists
            self.grades.pop(course_code, None)

    def calculate_gpa(self) -> float:
        """
        Calculate the student's GPA based on current grades.
        
        Returns:
            The calculated GPA as a float, or 0.0 if no grades exist.
        """
        if not self.grades:
            return 0.0
        total = sum(self.grades.values())
        return round(total / len(self.grades), 2)

    def get_academic_status(self) -> str:
        """
        Determine the student's academic status based on GPA.
        
        Returns:
            Academic status as a string ("Dean's List", "Good Standing", or "Probation").
        """
        gpa = self.calculate_gpa()
        if gpa >= 3.5:
            return "Dean's List"
        elif gpa >= 2.0:
            return "Good Standing"
        else:
            return "Probation"

    def get_responsibilities(self) -> str:
        """
        Get the responsibilities specific to students.
        
        Returns:
            A string describing student responsibilities.
        """
        return "Study and attend classes"

    def __str__(self) -> str:
        """Return a string representation of the student."""
        return f"{self.__class__.__name__}: {self.name} (ID: {self.person_id}, Major: {self.major})"


class UndergraduateStudent(Student):
    """
    Class representing undergraduate students.
    
    Inherits all functionality from Student with potential for
    undergraduate-specific features.
    """
    
    def get_degree_type(self) -> str:
        """
        Get the degree type for undergraduate students.
        
        Returns:
            The degree type as a string.
        """
        return "Bachelor's Degree"


class GraduateStudent(Student):
    """
    Class representing graduate students.
    
    Inherits all functionality from Student with potential for
    graduate-specific features.
    """
    
    def get_degree_type(self) -> str:
        """
        Get the degree type for graduate students.
        
        Returns:
            The degree type as a string.
        """
        return "Master's/Doctoral Degree"


class SecureStudentRecord:
    """
    Secure wrapper for student records with controlled access to GPA.
    
    This class provides a secure interface for accessing and modifying
    student GPA information with validation.
    
    Attributes:
        __student (Student): The student whose record is being secured.
        __gpa (float): The student's GPA with controlled access.
    """
    
    def __init__(self, student: Student) -> None:
        """
        Initialize a secure student record.
        
        Args:
            student: The student instance to create a secure record for.
        """
        self.__student = student
        self.__gpa = student.calculate_gpa()

    @property
    def gpa(self) -> float:
        """
        Get the student's GPA.
        
        Returns:
            The student's current GPA.
        """
        return self.__gpa

    @gpa.setter
    def gpa(self, value: float) -> None:
        """
        Set the student's GPA with validation.
        
        Args:
            value: The new GPA value to set.
            
        Raises:
            ValueError: If the GPA is not between 0.0 and 4.0.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("GPA must be a number")
        if not 0.0 <= value <= 4.0:
            raise ValueError("GPA must be between 0.0 and 4.0")
        self.__gpa = float(value)

    def get_student_info(self) -> str:
        """
        Get formatted student information.
        
        Returns:
            A formatted string containing student name, ID, and GPA.
        """
        return f"Name: {self.__student.name}, ID: {self.__student.person_id}, GPA: {self.__gpa:.2f}"

    def update_gpa_from_student(self) -> None:
        """Update the secure GPA from the student's current calculated GPA."""
        self.__gpa = self.__student.calculate_gpa()
