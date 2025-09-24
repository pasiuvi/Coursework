"""
Faculty module containing faculty-related classes.

This module defines various faculty types and their specific
responsibilities and workload calculations for the university system.
"""

from typing import Any
from person import Person


class Faculty(Person):
    """
    Base class for all faculty members in the university system.
    
    Attributes:
        name (str): The faculty member's full name.
        person_id (str): Unique identifier for the faculty member.
        department (str): The department the faculty member belongs to.
    """
    
    def __init__(self, name: str, person_id: str, department: str) -> None:
        """
        Initialize a Faculty instance.
        
        Args:
            name: The faculty member's full name.
            person_id: Unique identifier for the faculty member.
            department: The department the faculty member belongs to.
        """
        super().__init__(name, person_id)
        self.department = department

    def get_responsibilities(self) -> str:
        """
        Get the responsibilities specific to faculty members.
        
        Returns:
            A string describing faculty responsibilities.
        """
        return "Teach and research"

    def calculate_workload(self) -> str:
        """
        Calculate and return the faculty member's workload.
        
        Returns:
            A string describing the standard workload.
        """
        return "Standard workload"

    def __str__(self) -> str:
        """Return a string representation of the faculty member."""
        return (f"{self.__class__.__name__}: {self.name} "
                f"(ID: {self.person_id}, Dept: {self.department})")


class Professor(Faculty):
    """
    Class representing professors with research focus.
    
    Professors typically have higher workloads due to research
    responsibilities in addition to teaching.
    """
    
    def calculate_workload(self) -> str:
        """
        Calculate workload specific to professors.
        
        Returns:
            A string describing the professor's high workload.
        """
        return "High workload with research responsibilities"

    def get_responsibilities(self) -> str:
        """
        Get the responsibilities specific to professors.
        
        Returns:
            A string describing professor responsibilities.
        """
        return "Teach, conduct research, mentor graduate students, and publish papers"


class Lecturer(Faculty):
    """
    Class representing lecturers focused primarily on teaching.
    
    Lecturers have teaching-focused responsibilities with less
    emphasis on research compared to professors.
    """
    
    def calculate_workload(self) -> str:
        """
        Calculate workload specific to lecturers.
        
        Returns:
            A string describing the lecturer's teaching-focused workload.
        """
        return "Teaching-focused workload"

    def get_responsibilities(self) -> str:
        """
        Get the responsibilities specific to lecturers.
        
        Returns:
            A string describing lecturer responsibilities.
        """
        return "Teach courses and support student learning"


class TA(Faculty):
    """
    Class representing Teaching Assistants.
    
    TAs typically assist professors and lecturers with teaching
    duties and have lighter workloads.
    """
    
    def calculate_workload(self) -> str:
        """
        Calculate workload specific to teaching assistants.
        
        Returns:
            A string describing the TA's assistant workload.
        """
        return "Assist in teaching and grading"

    def get_responsibilities(self) -> str:
        """
        Get the responsibilities specific to teaching assistants.
        
        Returns:
            A string describing TA responsibilities.
        """
        return "Assist with teaching, grading, and student support"
