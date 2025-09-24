# University Management System

A comprehensive university management system built with Python and Flask, following PEP 8 standards and best practices.

## Features

- **Person Management**: Students, faculty, and staff with polymorphic behavior
- **Course Management**: Course creation, enrollment, and prerequisite handling
- **Department Management**: Department organization and faculty assignment
- **Grade Management**: Student grade tracking and GPA calculation
- **Secure Records**: Encapsulated student records with validation
- **Web Interface**: Flask-based web application for easy management
- **Database Persistence**: JSON-based data storage with backup and restore

## Project Structure

```
question1_university_system/
├── person.py              # Base Person class and Staff subclass
├── student.py             # Student classes and secure record handling
├── faculty.py             # Faculty classes with different roles
├── department.py          # Department and Course classes
├── database_manager.py    # Database operations and persistence
├── main.py               # Command-line demonstration script
├── app.py                # Flask web application
├── assign_courses_to_dept.py    # Utility script for course assignment
├── debug_enrollment.py          # Debugging utility for enrollment issues
├── demonstrate_prerequisites.py # Prerequisite system demonstration
├── database.json         # JSON database file (created automatically)
└── templates/            # HTML templates for web interface
    ├── home.html
    ├── add_course.html
    ├── add_department.html
    ├── add_person.html
    ├── enroll.html
    ├── student_details.html
    └── ...
```

## Installation

1. Ensure Python 3.8+ is installed
2. Install required dependencies:
   ```bash
   pip install flask
   ```
3. Navigate to the project directory:
   ```bash
   cd question1_university_system
   ```

## Usage

### Command Line Interface

Run the main demonstration script:
```bash
python main.py
```

This will demonstrate:
- Object creation and polymorphism
- Student enrollment and grade management
- Faculty workload calculation
- Secure record handling

### Web Interface

1. Start the Flask application:
   ```bash
   python app.py
   ```

2. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

3. Use the web interface to:
   - Add departments, courses, and people
   - Enroll students in courses
   - Manage grades and faculty assignments
   - View student details and academic status

### Utility Scripts

#### Course Assignment
Assign courses to departments:
```bash
python assign_courses_to_dept.py
```

#### Debug Enrollment
Debug enrollment issues:
```bash
python debug_enrollment.py
```

#### Prerequisite Demonstration
Show prerequisite system features:
```bash
python demonstrate_prerequisites.py
```

## Classes and Architecture

### Core Classes

- **Person**: Base class with common attributes and methods
- **Student**: Student management with courses and grades
  - **UndergraduateStudent**: Undergraduate-specific features
  - **GraduateStudent**: Graduate-specific features
- **Faculty**: Faculty management with workload calculation
  - **Professor**: Research-focused faculty
  - **Lecturer**: Teaching-focused faculty  
  - **TA**: Teaching assistant role
- **Staff**: Administrative personnel
- **Course**: Course management with enrollment and prerequisites
- **Department**: Department organization and management
- **SecureStudentRecord**: Secure access to student GPA data

### Design Patterns

- **Inheritance**: Person → Student/Faculty/Staff hierarchy
- **Polymorphism**: Common interface for all person types
- **Encapsulation**: Private attributes in SecureStudentRecord
- **Composition**: Department contains courses and people

## Code Quality Standards

This project follows:

- **PEP 8**: Python style guide compliance
- **Type Hints**: Full type annotation support
- **Docstrings**: Comprehensive documentation for all functions and classes
- **Error Handling**: Proper exception handling and validation
- **Separation of Concerns**: Clear module boundaries and responsibilities

## Database Schema

The system uses JSON for data persistence with the following structure:

```json
{
  "people": [
    {
      "type": "UndergraduateStudent",
      "name": "John Doe",
      "person_id": "S001",
      "major": "Computer Science",
      "courses": ["CS101"],
      "grades": {"CS101": 3.5}
    }
  ],
  "departments": [
    {
      "name": "Computer Science",
      "faculty_ids": ["F001"],
      "student_ids": ["S001"],
      "course_codes": ["CS101"]
    }
  ],
  "courses": [
    {
      "name": "Introduction to CS",
      "code": "CS101",
      "max_enrollment": 50,
      "prerequisites": [],
      "enrolled_student_ids": ["S001"],
      "faculty_id": "F001"
    }
  ]
}
```

## API Reference

### Key Methods

#### Student Management
- `student.enroll_course(course_code)`: Enroll in a course
- `student.drop_course(course_code)`: Drop a course
- `student.calculate_gpa()`: Calculate current GPA
- `student.get_academic_status()`: Get academic standing

#### Course Management
- `course.enroll_student(student)`: Enroll a student with validation
- `course.assign_faculty(faculty)`: Assign faculty to course
- `course.get_enrollment_info()`: Get enrollment statistics

#### Department Management
- `department.add_faculty(faculty)`: Add faculty member
- `department.add_student(student)`: Add student
- `department.add_course(course)`: Add course offering
- `department.get_department_stats()`: Get department statistics

## Contributing

1. Follow PEP 8 style guidelines
2. Add type hints to all functions
3. Include comprehensive docstrings
4. Write unit tests for new features
5. Update this README for significant changes

## License

This project is for educational purposes as part of a university coursework assignment.
