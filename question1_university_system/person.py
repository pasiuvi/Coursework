"""A base class to represent a person in the university.(students, faculty, staff)""" 
class Person:
    def __init__(self, name, age):
        """Initializes a Person object."""
        self.name = name #Name of the person
        self.age = age #Age of the person

    #Method to return general details of person
    def get_details(self):
        return f"Name: {self.name}, Age: {self.age}"
    
    #Method to returning general responsibilities, can be overridden by subclasses
    def get_responsibilities(self):
        return "General responsibilities"