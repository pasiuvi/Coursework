"""
Database management module for the university system.

This module provides functionality to load and save university data
to/from JSON files, converting between JSON and Python objects.
"""

import json
import os
from typing import List, Tuple, Optional, Dict, Any

from person import Person, Staff
from student import Student, UndergraduateStudent, GraduateStudent, SecureStudentRecord
from faculty import Faculty, Professor, Lecturer, TA
from department import Department, Course

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_FILE = os.path.join(SCRIPT_DIR, 'database.json')


def load_database() -> Tuple[List[Department], List[Course], List[Person]]:
    """
    Load data from JSON file and convert to objects.
    
    Returns:
        A tuple containing (departments, courses, people) lists.
        Returns empty lists if database file doesn't exist or there's an error.
    """
    if not os.path.exists(DATABASE_FILE):
        return [], [], []
    
    try:
        with open(DATABASE_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Convert JSON data back to objects
        departments = []
        courses = []
        people = []
        
        # Load people first
        for person_data in data.get('people', []):
            person = create_person_from_data(person_data)
            if person:
                people.append(person)
        
        # Load departments
        for dept_data in data.get('departments', []):
            dept = Department(dept_data['name'])
            # Add faculty and students by ID reference
            for faculty_id in dept_data.get('faculty_ids', []):
                faculty = next((p for p in people 
                              if p.person_id == faculty_id and isinstance(p, Faculty)), None)
                if faculty:
                    dept.add_faculty(faculty)
            for student_id in dept_data.get('student_ids', []):
                student = next((p for p in people 
                              if p.person_id == student_id and isinstance(p, Student)), None)
                if student:
                    dept.add_student(student)
            departments.append(dept)
        
        # Load courses
        for course_data in data.get('courses', []):
            course = Course(
                course_data['name'],
                course_data['code'],
                course_data['max_enrollment'],
                course_data.get('prerequisites', [])
            )
            # Add enrolled students
            for student_id in course_data.get('enrolled_student_ids', []):
                student = next((p for p in people 
                              if p.person_id == student_id and isinstance(p, Student)), None)
                if student:
                    course.enrolled_students.append(student)
            # Assign faculty
            faculty_id = course_data.get('faculty_id')
            if faculty_id:
                faculty = next((p for p in people 
                              if p.person_id == faculty_id and isinstance(p, Faculty)), None)
                if faculty:
                    course.faculty = faculty
            courses.append(course)
        
        # Assign courses to departments after all courses are loaded
        for dept_data in data.get('departments', []):
            dept_name = dept_data['name']
            department = next((d for d in departments if d.name == dept_name), None)
            if department:
                for course_code in dept_data.get('course_codes', []):
                    course = next((c for c in courses if c.code == course_code), None)
                    if course and course not in department.courses:
                        department.add_course(course)
        
        return departments, courses, people
    
    except Exception as e:
        print(f"Error loading database: {e}")
        return [], [], []


def create_person_from_data(person_data: Dict[str, Any]) -> Optional[Person]:
    """
    Create person object from JSON data.
    
    Args:
        person_data: Dictionary containing person information from JSON.
        
    Returns:
        A Person object of the appropriate type, or None if creation fails.
    """
    try:
        person_type = person_data['type']
        name = person_data['name']
        
        # Handle both old 'id' and new 'person_id' field names for backward compatibility
        person_id = person_data.get('person_id') or person_data.get('id')
        if not person_id:
            print(f"Warning: No ID found for person {name}")
            return None
        
        if person_type == 'UndergraduateStudent':
            person = UndergraduateStudent(name, person_id, person_data['major'])
        elif person_type == 'GraduateStudent':
            person = GraduateStudent(name, person_id, person_data['major'])
        elif person_type == 'Professor':
            person = Professor(name, person_id, person_data['department'])
        elif person_type == 'Lecturer':
            person = Lecturer(name, person_id, person_data['department'])
        elif person_type == 'TA':
            person = TA(name, person_id, person_data['department'])
        elif person_type == 'Staff':
            person = Staff(name, person_id)
        else:
            return None
        
        # Load additional data for students
        if isinstance(person, Student):
            person.courses = person_data.get('courses', [])
            person.grades = person_data.get('grades', {})
        
        return person
    
    except KeyError as e:
        print(f"Missing required field in person data: {e}")
        return None
    except Exception as e:
        print(f"Error creating person from data: {e}")
        return None


def save_database(departments: List[Department], courses: List[Course], 
                 people: List[Person]) -> bool:
    """
    Save data to JSON file.
    
    Args:
        departments: List of Department objects to save.
        courses: List of Course objects to save.
        people: List of Person objects to save.
        
    Returns:
        True if save was successful, False otherwise.
    """
    try:
        data = {
            'departments': [],
            'courses': [],
            'people': []
        }
        
        # Convert people to JSON
        for person in people:
            person_data = {
                'type': person.__class__.__name__,
                'name': person.name,
                'person_id': person.person_id  # Updated field name
            }
            
            if isinstance(person, Student):
                person_data['major'] = person.major
                person_data['courses'] = person.courses
                person_data['grades'] = person.grades
            elif isinstance(person, Faculty):
                person_data['department'] = person.department
            
            data['people'].append(person_data)
        
        # Convert departments to JSON
        for dept in departments:
            dept_data = {
                'name': dept.name,
                'faculty_ids': [f.person_id for f in dept.faculty],  # Updated field name
                'student_ids': [s.person_id for s in dept.students],  # Updated field name
                'course_codes': [c.code for c in dept.courses]
            }
            data['departments'].append(dept_data)
        
        # Convert courses to JSON
        for course in courses:
            course_data = {
                'name': course.name,
                'code': course.code,
                'max_enrollment': course.max_enrollment,
                'prerequisites': course.prerequisites,
                'enrolled_student_ids': [s.person_id for s in course.enrolled_students],  # Updated field name
                'faculty_id': course.faculty.person_id if course.faculty else None  # Updated field name
            }
            data['courses'].append(course_data)
        
        with open(DATABASE_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return True
    
    except Exception as e:
        print(f"Error saving database: {e}")
        return False


def validate_database_integrity(departments: List[Department], courses: List[Course], 
                               people: List[Person]) -> List[str]:
    """
    Validate the integrity of the database objects.
    
    Args:
        departments: List of Department objects to validate.
        courses: List of Course objects to validate.
        people: List of Person objects to validate.
        
    Returns:
        List of validation error messages. Empty list if no errors found.
    """
    errors = []
    
    # Check for duplicate person IDs
    person_ids = [p.person_id for p in people]
    if len(person_ids) != len(set(person_ids)):
        errors.append("Duplicate person IDs found")
    
    # Check for duplicate course codes
    course_codes = [c.code for c in courses]
    if len(course_codes) != len(set(course_codes)):
        errors.append("Duplicate course codes found")
    
    # Check for duplicate department names
    dept_names = [d.name for d in departments]
    if len(dept_names) != len(set(dept_names)):
        errors.append("Duplicate department names found")
    
    return errors
