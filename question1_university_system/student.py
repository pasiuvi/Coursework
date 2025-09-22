"""
Student classes for the University Management System.
Includes undergraduate and graduate student specializations.
"""

from person import Person
from typing import List, Dict, Optional
from enum import Enum

class AcademicStatus(Enum):
    """Enum representing different academic statuses."""
    DEANS_LIST = "Dean's List"
    GOOD_STANDING = "Good Standing"
    PROBATION = "Academic Probation"
    WARNING = "Warning"

class Student(Person):
    """
    Base Student class with course enrollment and GPA functionality.
    """
    
    def __init__(self, name: str, student_id: str, email: str, major: str, department: str = None):
        super().__init__(name, student_id, email, department)
        self._major = major
        self._enrolled_courses = {}  # course_code: course_object
        self._completed_courses = {}  # course_code: {'grade': grade, 'credits': credits}
        self._gpa = 0.0
        self._academic_status = AcademicStatus.GOOD_STANDING
    
    def enroll_course(self, course) -> bool:
        """
        Enroll student in a course if prerequisites are met and seats available.
        
        Args:
            course: Course object to enroll in
            
        Returns:
            bool: True if enrollment successful, False otherwise
        """
        if course.course_code in self._enrolled_courses:
            print(f"Already enrolled in {course.course_code}")
            return False
        
        # Check prerequisites
        if not self._check_prerequisites(course):
            print(f"Prerequisites not met for {course.course_code}")
            return False
        
        # Check seat availability
        if not course.has_available_seats():
            print(f"No available seats in {course.course_code}")
            return False
        
        # Enroll student
        if course.enroll_student(self):
            self._enrolled_courses[course.course_code] = course
            print(f"Successfully enrolled in {course.course_code}")
            return True
        
        return False
    
    def drop_course(self, course_code: str) -> bool:
        """Drop a course from current enrollment."""
        if course_code in self._enrolled_courses:
            course = self._enrolled_courses[course_code]
            if course.drop_student(self):
                del self._enrolled_courses[course_code]
                print(f"Dropped {course_code} successfully")
                return True
        print(f"Not enrolled in {course_code}")
        return False
    
    def _check_prerequisites(self, course) -> bool:
        """Check if student meets all course prerequisites."""
        if not course.prerequisites:
            return True
        
        completed_codes = set(self._completed_courses.keys())
        return all(prereq in completed_codes for prereq in course.prerequisites)
    
    def complete_course(self, course_code: str, grade: float) -> bool:
        """
        Mark a course as completed with a grade.
        
        Args:
            course_code (str): Code of the course to complete
            grade (float): Grade received (0.0-4.0 scale)
            
        Returns:
            bool: True if successful
        """
        if course_code not in self._enrolled_courses:
            print(f"Not enrolled in {course_code}")
            return False
        
        if not 0.0 <= grade <= 4.0:
            raise ValueError("Grade must be between 0.0 and 4.0")
        
        course = self._enrolled_courses[course_code]
        self._completed_courses[course_code] = {
            'grade': grade,
            'credits': course.credits,
            'course': course
        }
        
        # Remove from enrolled courses
        del self._enrolled_courses[course_code]
        
        # Recalculate GPA
        self.calculate_gpa()
        
        return True
    
    def calculate_gpa(self) -> float:
        """Calculate cumulative GPA based on completed courses."""
        if not self._completed_courses:
            self._gpa = 0.0
            return self._gpa
        
        total_points = 0
        total_credits = 0
        
        for course_data in self._completed_courses.values():
            grade = course_data['grade']
            credits = course_data['credits']
            total_points += grade * credits
            total_credits += credits
        
        self._gpa = total_points / total_credits if total_credits > 0 else 0.0
        self._update_academic_status()
        return self._gpa
    
    def _update_academic_status(self):
        """Update academic status based on current GPA."""
        if self._gpa >= 3.5:
            self._academic_status = AcademicStatus.DEANS_LIST
        elif self._gpa >= 2.0:
            self._academic_status = AcademicStatus.GOOD_STANDING
        elif self._gpa >= 1.0:
            self._academic_status = AcademicStatus.WARNING
        else:
            self._academic_status = AcademicStatus.PROBATION
    
    def get_academic_status(self) -> str:
        """Get current academic status."""
        return self._academic_status.value
    
    def get_responsibilities(self) -> str:
        return f"Student responsibilities: Attend classes, complete assignments, maintain {self._academic_status.value} status"
    
    # Property getters and setters with validation
    @property
    def major(self) -> str:
        return self._major
    
    @major.setter
    def major(self, value: str):
        if not value:
            raise ValueError("Major cannot be empty")
        self._major = value
    
    @property
    def gpa(self) -> float:
        return self._gpa
    
    @property
    def enrolled_courses(self) -> dict:
        return self._enrolled_courses.copy()
    
    @property
    def completed_courses(self) -> dict:
        return self._completed_courses.copy()


class UndergraduateStudent(Student):
    """Undergraduate student specialization."""
    
    def __init__(self, name: str, student_id: str, email: str, major: str, year: int, department: str = None):
        super().__init__(name, student_id, email, major, department)
        self._year = year
        self._max_credits_per_semester = 18
    
    def get_responsibilities(self) -> str:
        base_resp = super().get_responsibilities()
        return f"{base_resp}. Undergraduate year {self._year} with max {self._max_credits_per_semester} credits/semester"
    
    @property
    def year(self) -> int:
        return self._year
    
    @year.setter
    def year(self, value: int):
        if not 1 <= value <= 4:
            raise ValueError("Undergraduate year must be between 1 and 4")
        self._year = value


class GraduateStudent(Student):
    """Graduate student specialization with research focus."""
    
    def __init__(self, name: str, student_id: str, email: str, major: str, 
                 degree_type: str, advisor: str = None, department: str = None):
        super().__init__(name, student_id, email, major, department)
        self._degree_type = degree_type  # "Masters" or "PhD"
        self._advisor = advisor
        self._research_topic = None
        self._max_credits_per_semester = 12
    
    def get_responsibilities(self) -> str:
        base_resp = super().get_responsibilities()
        research_info = f", Research: {self._research_topic}" if self._research_topic else ""
        return f"{base_resp}. {self._degree_type} student{research_info}"
    
    def set_research_topic(self, topic: str):
        """Set the student's research topic."""
        self._research_topic = topic
    
    @property
    def degree_type(self) -> str:
        return self._degree_type
    
    @property
    def advisor(self) -> str:
        return self._advisor
    
    @advisor.setter
    def advisor(self, value: str):
        self._advisor = value