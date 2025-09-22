"""
Faculty classes for the University Management System.
Includes Professor, Lecturer, and TA specializations.
"""

from person import Person
from typing import List, Optional

class Faculty(Person):
    """Base Faculty class with teaching responsibilities."""
    
    def __init__(self, name: str, faculty_id: str, email: str, department: str, office: str = None):
        super().__init__(name, faculty_id, email, department)
        self._office = office
        self._assigned_courses = []  # List of Course objects
        self._office_hours = []
    
    def assign_course(self, course) -> bool:
        """Assign a course to this faculty member."""
        if course not in self._assigned_courses:
            self._assigned_courses.append(course)
            course.assign_faculty(self)
            return True
        return False
    
    def calculate_workload(self) -> int:
        """Calculate teaching workload in credit hours."""
        return sum(course.credits for course in self._assigned_courses)
    
    def get_responsibilities(self) -> str:
        workload = self.calculate_workload()
        return f"Teaching {workload} credit hours. Courses: {len(self._assigned_courses)}"
    
    def add_office_hours(self, day: str, time: str):
        """Add office hours schedule."""
        self._office_hours.append(f"{day}: {time}")
    
    @property
    def assigned_courses(self) -> List:
        return self._assigned_courses.copy()
    
    @property
    def office(self) -> str:
        return self._office


class Professor(Faculty):
    """Professor specialization with research responsibilities."""
    
    def __init__(self, name: str, faculty_id: str, email: str, department: str, 
                 rank: str, office: str = None):
        super().__init__(name, faculty_id, email, department, office)
        self._rank = rank  # e.g., "Assistant", "Associate", "Full"
        self._research_grants = []
        self._advisees = []  # Graduate students advised
    
    def get_responsibilities(self) -> str:
        base_resp = super().get_responsibilities()
        return f"{base_resp}. {self._rank} Professor with {len(self._research_grants)} grants, advising {len(self._advisees)} students"
    
    def add_research_grant(self, grant: str):
        """Add a research grant."""
        self._research_grants.append(grant)
    
    def add_advisee(self, student):
        """Add a graduate student advisee."""
        if student not in self._advisees:
            self._advisees.append(student)
            student.advisor = self.name
    
    def calculate_workload(self) -> int:
        """Professor workload includes research and advising."""
        teaching_load = super().calculate_workload()
        research_load = len(self._research_grants) * 3  # Estimate research workload
        advisee_load = len(self._advisees) * 1  # Estimate advising workload
        return teaching_load + research_load + advisee_load


class Lecturer(Faculty):
    """Lecturer specialization focused on teaching."""
    
    def __init__(self, name: str, faculty_id: str, email: str, department: str, 
                 contract_type: str, office: str = None):
        super().__init__(name, faculty_id, email, department, office)
        self._contract_type = contract_type  # "Full-time" or "Part-time"
        self._max_courses = 4 if contract_type == "Full-time" else 2
    
    def get_responsibilities(self) -> str:
        base_resp = super().get_responsibilities()
        return f"{base_resp}. {self._contract_type} Lecturer"
    
    def can_teach_more(self) -> bool:
        """Check if lecturer can teach more courses."""
        return len(self._assigned_courses) < self._max_courses


class TA(Faculty):
    """Teaching Assistant - typically a graduate student with teaching duties."""
    
    def __init__(self, name: str, faculty_id: str, email: str, department: str, 
                 supervisor: str, office: str = None):
        super().__init__(name, faculty_id, email, department, office)
        self._supervisor = supervisor  # Professor who supervises
        self._lab_sections = []
        self._grading_assignments = []
    
    def get_responsibilities(self) -> str:
        base_resp = super().get_responsibilities()
        return f"{base_resp}. TA supervised by {self._supervisor}, teaching {len(self._lab_sections)} lab sections"
    
    def assign_lab_section(self, lab_section: str):
        """Assign a lab section to the TA."""
        self._lab_sections.append(lab_section)
    
    def assign_grading(self, assignment: str):
        """Assign grading duties."""
        self._grading_assignments.append(assignment)
    
    def calculate_workload(self) -> int:
        """TA workload includes lab teaching and grading."""
        teaching_load = super().calculate_workload()
        lab_load = len(self._lab_sections) * 2
        grading_load = len(self._grading_assignments)
        return teaching_load + lab_load + grading_load