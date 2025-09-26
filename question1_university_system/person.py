"""
Person module containing base Person class and Staff subclass.

This module defines the basic Person class and its subclasses for representing
university personnel in the university management system.
"""

from typing import Any


class Person:
    """
    Base class representing a person in the university system.
    
    Attributes:
        name (str): The person's full name.
        person_id (str): Unique identifier for the person.
    """
    
    def __init__(self, name: str, person_id: str) -> None:
        """
        Initialize a Person instance.
        
        Args:
            name: The person's full name.
            person_id: Unique identifier for the person.
        """
        self.name = name
        self.person_id = person_id  # Changed from 'id' to avoid shadowing built-in

    def get_responsibilities(self) -> str:
        """
        Get the general responsibilities of the person.
        
        Returns:
            A string describing general responsibilities.
        """
        return "General responsibilities"

    def __str__(self) -> str:
        """Return a string representation of the person."""
        return f"{self.__class__.__name__}: {self.name} (ID: {self.person_id})"

    def __repr__(self) -> str:
        """Return a detailed string representation for debugging."""
        return f"{self.__class__.__name__}(name='{self.name}', person_id='{self.person_id}')"


class Staff(Person):
    """
    Staff class representing administrative personnel.
    
    Inherits from Person and provides staff-specific functionality.
    
    Attributes:
        name (str): The staff member's full name (inherited from Person).
        person_id (str): Unique identifier for the staff member (inherited from Person).
        department (str): The department the staff member works in.
    """
    
    def __init__(self, name: str, person_id: str, department: str = "Administration") -> None:
        """
        Initialize a Staff instance.
        
        Args:
            name: The staff member's full name.
            person_id: Unique identifier for the staff member.
            department: The department the staff member works in (default: "Administration").
        """
        super().__init__(name, person_id)
        self.department = department
    
    def get_responsibilities(self) -> str:
        """
        Get the responsibilities specific to staff members.
        
        Returns:
            A string describing administrative duties.
        """
        return "Administrative duties"
    
    def __str__(self) -> str:
        """Return a string representation of the staff member."""
        return (f"{self.__class__.__name__}: {self.name} "
                f"(ID: {self.person_id}, Dept: {self.department})")
