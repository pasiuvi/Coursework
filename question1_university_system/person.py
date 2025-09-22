"""
Base Person class and related classes for the University Management System.
Demonstrates inheritance hierarchy and polymorphism.
"""

from abc import ABC, abstractmethod
from typing import List, Optional

class Person(ABC):
    """
    Abstract base class representing a person in the university system.
    Implements core attributes and methods common to all person types.
    """
    
    def __init__(self, name: str, person_id: str, email: str, department: str = None):
        """
        Initialize a Person with basic information.
        
        Args:
            name (str): Full name of the person
            person_id (str): Unique identifier
            email (str): Contact email
            department (str): Department affiliation
        """
        self._name = name
        self._person_id = person_id
        self._email = email
        self._department = department
    
    @abstractmethod
    def get_responsibilities(self) -> str:
        """Return role-specific responsibilities. Must be implemented by subclasses."""
        pass
    
    def get_contact_info(self) -> str:
        """Return formatted contact information."""
        return f"Name: {self._name}, ID: {self._person_id}, Email: {self._email}"
    
    # Property getters with validation
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, value: str):
        if not value or not isinstance(value, str):
            raise ValueError("Name must be a non-empty string")
        self._name = value
    
    @property
    def person_id(self) -> str:
        return self._person_id
    
    @property
    def email(self) -> str:
        return self._email
    
    @email.setter
    def email(self, value: str):
        if "@" not in value:
            raise ValueError("Email must contain @ symbol")
        self._email = value
    
    @property
    def department(self) -> str:
        return self._department
    
    @department.setter
    def department(self, value: str):
        self._department = value
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self._name} ({self._person_id})"
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self._name}', '{self._person_id}', '{self._email}')"


class Staff(Person):
    """
    Staff member class representing administrative and support staff.
    """
    
    def __init__(self, name: str, person_id: str, email: str, position: str, department: str = None):
        super().__init__(name, person_id, email, department)
        self._position = position
        self._assigned_tasks = []
    
    def get_responsibilities(self) -> str:
        return f"Administrative duties as {self._position}. Current tasks: {len(self._assigned_tasks)}"
    
    def assign_task(self, task: str):
        """Assign a new task to the staff member."""
        self._assigned_tasks.append(task)
    
    def complete_task(self, task: str):
        """Remove a completed task."""
        if task in self._assigned_tasks:
            self._assigned_tasks.remove(task)
    
    @property
    def position(self) -> str:
        return self._position