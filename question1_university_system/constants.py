"""
Constants for the university management system.

This module defines common constants used throughout the application
to ensure consistency and maintainability.
"""

# Grade point scale
MIN_GPA = 0.0
MAX_GPA = 4.0

# Academic status thresholds
DEANS_LIST_THRESHOLD = 3.5
GOOD_STANDING_THRESHOLD = 2.0

# Default course settings
DEFAULT_MAX_ENROLLMENT = 30
DEFAULT_MIN_ENROLLMENT = 1

# Database settings
DATABASE_FILENAME = 'database.json'
DATABASE_ENCODING = 'utf-8'
DATABASE_INDENT = 2

# Web application settings
DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 5000
DEBUG_MODE = True

# Person ID prefixes (for consistency)
STUDENT_ID_PREFIX = 'S'
FACULTY_ID_PREFIX = 'F'
STAFF_ID_PREFIX = 'ST'

# Course code patterns
COURSE_CODE_MIN_LENGTH = 2
COURSE_CODE_MAX_LENGTH = 10

# Common prerequisite types
COMMON_PREREQUISITES = [
    'degree',
    'permission',
    'senior_standing',
    'junior_standing',
    'advisor_approval'
]

# Academic levels
UNDERGRADUATE_LEVEL = 'undergraduate'
GRADUATE_LEVEL = 'graduate'

# Faculty types
FACULTY_TYPES = [
    'Professor',
    'Lecturer', 
    'TA'
]

# Student types
STUDENT_TYPES = [
    'UndergraduateStudent',
    'GraduateStudent'
]

# Message types for web interface
MESSAGE_SUCCESS = 'success'
MESSAGE_ERROR = 'error'
MESSAGE_WARNING = 'warning'
MESSAGE_INFO = 'info'

# Validation messages
ERROR_INVALID_GPA = "GPA must be between {min_gpa} and {max_gpa}"
ERROR_COURSE_FULL = "Course is full ({current}/{max})"
ERROR_MISSING_PREREQUISITES = "Missing prerequisites: {prereqs}"
ERROR_ALREADY_ENROLLED = "Student is already enrolled in this course"
ERROR_NOT_FOUND = "{item_type} with ID {item_id} not found"

SUCCESS_ENROLLMENT = "Enrollment successful"
SUCCESS_DATABASE_SAVE = "Database saved successfully"
SUCCESS_OPERATION = "Operation completed successfully"
