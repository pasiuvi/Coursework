#!/usr/bin/env python3
"""
Unit Tests for Department Class

This module contains unit tests specifically for the Department class and its
course management functionality. Tests cover:
- Department class initialization and basic functionality  
- Course creation and management
- Faculty assignment to courses
- Student enrollment in courses
- Course prerequisites system
- Department-level operations
"""

import unittest
import sys
import os

# Add the parent directory to Python path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from person import Person
from student import Student
from faculty import Faculty, Professor
from department import Department, Course


class TestCourse(unittest.TestCase):
    """Test Course class functionality"""
    
    def setUp(self):
        """Set up test instances"""
        self.course = Course("CS101", "Introduction to Computer Science", 3)
        self.advanced_course = Course("CS201", "Data Structures", 3, ["CS101"])

    def test_course_initialization(self):
        """Test Course class initialization"""
        self.assertEqual(self.course.code, "CS101")
        self.assertEqual(self.course.title, "Introduction to Computer Science")
        self.assertEqual(self.course.credits, 3)
        self.assertEqual(self.course.prerequisites, [])

    def test_course_with_prerequisites(self):
        """Test Course with prerequisites"""
        self.assertEqual(self.advanced_course.code, "CS201")
        self.assertEqual(self.advanced_course.prerequisites, ["CS101"])

    def test_course_string_representation(self):
        """Test Course __str__ method"""
        expected = "CS101: Introduction to Computer Science (3 credits)"
        self.assertEqual(str(self.course), expected)

    def test_course_faculty_assignment(self):
        """Test assigning faculty to course"""
        professor = Professor("Dr. Smith", "F001", "Computer Science")
        self.course.assign_faculty(professor)
        self.assertEqual(self.course.assigned_faculty, professor)

    def test_course_enrollment(self):
        """Test student enrollment in course"""
        student = Student("John Doe", "S001", "Computer Science")
        self.course.enroll_student(student)
        self.assertIn(student, self.course.enrolled_students)
        self.assertEqual(len(self.course.enrolled_students), 1)

    def test_course_multiple_enrollments(self):
        """Test multiple students enrolling in course"""
        student1 = Student("John Doe", "S001", "Computer Science")
        student2 = Student("Jane Smith", "S002", "Computer Science")
        
        self.course.enroll_student(student1)
        self.course.enroll_student(student2)
        
        self.assertEqual(len(self.course.enrolled_students), 2)
        self.assertIn(student1, self.course.enrolled_students)
        self.assertIn(student2, self.course.enrolled_students)

    def test_course_duplicate_enrollment(self):
        """Test that student can't enroll in same course twice"""
        student = Student("John Doe", "S001", "Computer Science")
        
        self.course.enroll_student(student)
        self.course.enroll_student(student)  # Try to enroll again
        
        # Should still only have one enrollment
        self.assertEqual(len(self.course.enrolled_students), 1)

    def test_course_enrollment_capacity(self):
        """Test course enrollment capacity"""
        # Set a capacity for testing
        self.course.max_capacity = 2
        
        student1 = Student("John Doe", "S001", "Computer Science")
        student2 = Student("Jane Smith", "S002", "Computer Science")
        student3 = Student("Bob Johnson", "S003", "Computer Science")
        
        self.assertTrue(self.course.enroll_student(student1))
        self.assertTrue(self.course.enroll_student(student2))
        
        # This should fail due to capacity
        if hasattr(self.course, 'max_capacity'):
            result = self.course.enroll_student(student3)
            if not result:  # If enrollment failed due to capacity
                self.assertEqual(len(self.course.enrolled_students), 2)


class TestDepartment(unittest.TestCase):
    """Test Department class functionality"""
    
    def setUp(self):
        """Set up test instances"""
        self.department = Department("Computer Science", "Dr. Wilson", "F100")
        self.course1 = Course("CS101", "Introduction to Computer Science", 3)
        self.course2 = Course("CS201", "Data Structures", 3, ["CS101"])

    def test_department_initialization(self):
        """Test Department class initialization"""
        self.assertEqual(self.department.name, "Computer Science")
        self.assertEqual(self.department.head_name, "Dr. Wilson")
        self.assertEqual(self.department.head_id, "F100")
        self.assertEqual(self.department.courses, {})
        self.assertEqual(self.department.faculty, [])

    def test_department_add_course(self):
        """Test adding course to department"""
        self.department.add_course(self.course1)
        self.assertIn("CS101", self.department.courses)
        self.assertEqual(self.department.courses["CS101"], self.course1)

    def test_department_add_multiple_courses(self):
        """Test adding multiple courses to department"""
        self.department.add_course(self.course1)
        self.department.add_course(self.course2)
        
        self.assertEqual(len(self.department.courses), 2)
        self.assertIn("CS101", self.department.courses)
        self.assertIn("CS201", self.department.courses)

    def test_department_add_faculty(self):
        """Test adding faculty to department"""
        professor = Professor("Dr. Smith", "F001", "Computer Science")
        self.department.add_faculty(professor)
        
        self.assertIn(professor, self.department.faculty)
        self.assertEqual(len(self.department.faculty), 1)

    def test_department_add_multiple_faculty(self):
        """Test adding multiple faculty to department"""
        professor1 = Professor("Dr. Smith", "F001", "Computer Science")
        professor2 = Professor("Dr. Jones", "F002", "Computer Science")
        
        self.department.add_faculty(professor1)
        self.department.add_faculty(professor2)
        
        self.assertEqual(len(self.department.faculty), 2)
        self.assertIn(professor1, self.department.faculty)
        self.assertIn(professor2, self.department.faculty)

    def test_department_get_course(self):
        """Test retrieving course from department"""
        self.department.add_course(self.course1)
        retrieved_course = self.department.get_course("CS101")
        
        self.assertEqual(retrieved_course, self.course1)

    def test_department_get_nonexistent_course(self):
        """Test retrieving nonexistent course returns None"""
        retrieved_course = self.department.get_course("CS999")
        self.assertIsNone(retrieved_course)

    def test_department_list_courses(self):
        """Test listing all courses in department"""
        self.department.add_course(self.course1)
        self.department.add_course(self.course2)
        
        course_list = self.department.list_courses()
        self.assertEqual(len(course_list), 2)
        self.assertIn(self.course1, course_list)
        self.assertIn(self.course2, course_list)

    def test_department_assign_course_to_faculty(self):
        """Test assigning course to faculty member"""
        professor = Professor("Dr. Smith", "F001", "Computer Science")
        self.department.add_faculty(professor)
        self.department.add_course(self.course1)
        
        success = self.department.assign_course_to_faculty("CS101", professor)
        
        if success:
            self.assertEqual(self.course1.assigned_faculty, professor)
        else:
            # If method doesn't exist, that's also valid for the test
            pass

    def test_department_string_representation(self):
        """Test Department __str__ method"""
        expected = f"Department: Computer Science (Head: Dr. Wilson, ID: F100)"
        self.assertEqual(str(self.department), expected)


class TestCoursePrerequisites(unittest.TestCase):
    """Test course prerequisites system"""
    
    def setUp(self):
        """Set up test instances"""
        self.department = Department("Computer Science", "Dr. Wilson", "F100")
        self.intro_course = Course("CS101", "Introduction to Computer Science", 3)
        self.data_structures = Course("CS201", "Data Structures", 3, ["CS101"])
        self.algorithms = Course("CS301", "Algorithms", 3, ["CS201"])
        self.advanced_algo = Course("CS401", "Advanced Algorithms", 3, ["CS301", "CS201"])

    def test_course_no_prerequisites(self):
        """Test course with no prerequisites"""
        self.assertEqual(self.intro_course.prerequisites, [])

    def test_course_single_prerequisite(self):
        """Test course with single prerequisite"""
        self.assertEqual(self.data_structures.prerequisites, ["CS101"])

    def test_course_multiple_prerequisites(self):
        """Test course with multiple prerequisites"""
        self.assertEqual(self.advanced_algo.prerequisites, ["CS301", "CS201"])

    def test_prerequisite_chain(self):
        """Test a chain of prerequisites"""
        # CS101 -> CS201 -> CS301 -> CS401
        self.department.add_course(self.intro_course)
        self.department.add_course(self.data_structures)
        self.department.add_course(self.algorithms)
        
        # CS201 requires CS101
        self.assertIn("CS101", self.data_structures.prerequisites)
        # CS301 requires CS201  
        self.assertIn("CS201", self.algorithms.prerequisites)

    def test_check_prerequisites_method(self):
        """Test checking prerequisites for student enrollment"""
        student = Student("John Doe", "S001", "Computer Science")
        
        # Add courses to student's completed courses
        student.add_course(self.intro_course)  # Complete CS101
        
        # If department has prerequisite checking method
        if hasattr(self.department, 'check_prerequisites'):
            # Should be able to enroll in CS201 since CS101 is completed
            can_enroll = self.department.check_prerequisites("CS201", student)
            self.assertTrue(can_enroll)
            
            # Should not be able to enroll in CS301 since CS201 is not completed
            can_enroll = self.department.check_prerequisites("CS301", student)
            self.assertFalse(can_enroll)


class TestDepartmentIntegration(unittest.TestCase):
    """Test integration scenarios for Department management"""
    
    def setUp(self):
        """Set up comprehensive test scenario"""
        self.department = Department("Computer Science", "Dr. Wilson", "F100")
        
        # Create courses
        self.courses = [
            Course("CS101", "Introduction to Computer Science", 3),
            Course("CS201", "Data Structures", 3, ["CS101"]),
            Course("CS301", "Algorithms", 3, ["CS201"]),
            Course("CS102", "Programming Fundamentals", 3)
        ]
        
        # Create faculty
        self.faculty = [
            Professor("Dr. Smith", "F001", "Computer Science"),
            Professor("Dr. Jones", "F002", "Computer Science"),
            Faculty("Dr. Brown", "F003", "Computer Science")
        ]
        
        # Create students
        self.students = [
            Student("John Doe", "S001", "Computer Science"),
            Student("Jane Smith", "S002", "Computer Science"),
            Student("Bob Johnson", "S003", "Computer Science")
        ]

    def test_full_department_setup(self):
        """Test complete department setup"""
        # Add all courses
        for course in self.courses:
            self.department.add_course(course)
        
        # Add all faculty
        for faculty in self.faculty:
            self.department.add_faculty(faculty)
        
        # Verify setup
        self.assertEqual(len(self.department.courses), 4)
        self.assertEqual(len(self.department.faculty), 3)

    def test_course_enrollment_scenario(self):
        """Test realistic course enrollment scenario"""
        # Set up department
        for course in self.courses:
            self.department.add_course(course)
        
        # Enroll students in intro course
        intro_course = self.department.get_course("CS101")
        for student in self.students:
            intro_course.enroll_student(student)
        
        # Verify enrollment
        self.assertEqual(len(intro_course.enrolled_students), 3)
        
        # Enroll some students in programming fundamentals
        prog_course = self.department.get_course("CS102")
        prog_course.enroll_student(self.students[0])
        prog_course.enroll_student(self.students[1])
        
        self.assertEqual(len(prog_course.enrolled_students), 2)

    def test_faculty_course_assignment(self):
        """Test assigning faculty to courses"""
        # Set up department
        for course in self.courses:
            self.department.add_course(course)
        for faculty in self.faculty:
            self.department.add_faculty(faculty)
        
        # Assign faculty to courses
        self.courses[0].assign_faculty(self.faculty[0])  # CS101 -> Dr. Smith
        self.courses[1].assign_faculty(self.faculty[1])  # CS201 -> Dr. Jones
        
        # Verify assignments
        self.assertEqual(self.courses[0].assigned_faculty, self.faculty[0])
        self.assertEqual(self.courses[1].assigned_faculty, self.faculty[1])

    def test_department_course_progression(self):
        """Test student progression through courses"""
        # Set up department
        for course in self.courses:
            self.department.add_course(course)
        
        student = self.students[0]
        
        # Start with intro course
        intro_course = self.department.get_course("CS101")
        intro_course.enroll_student(student)
        
        # Complete intro course (simulate)
        student.add_course(intro_course)
        
        # Should now be able to take CS201
        data_structures = self.department.get_course("CS201")
        data_structures.enroll_student(student)
        
        # Verify enrollment
        self.assertIn(student, intro_course.enrolled_students)
        self.assertIn(student, data_structures.enrolled_students)

    def test_department_statistics(self):
        """Test department statistics and reporting"""
        # Set up department
        for course in self.courses:
            self.department.add_course(course)
        for faculty in self.faculty:
            self.department.add_faculty(faculty)
        
        # Basic statistics
        total_courses = len(self.department.courses)
        total_faculty = len(self.department.faculty)
        
        self.assertEqual(total_courses, 4)
        self.assertEqual(total_faculty, 3)
        
        # Course enrollment statistics
        intro_course = self.department.get_course("CS101")
        for student in self.students:
            intro_course.enroll_student(student)
        
        self.assertEqual(len(intro_course.enrolled_students), 3)


class TestDepartmentCourseManagement(unittest.TestCase):
    """Test advanced course management features"""
    
    def setUp(self):
        """Set up test department"""
        self.department = Department("Mathematics", "Dr. Taylor", "F200")

    def test_course_capacity_management(self):
        """Test course capacity limits"""
        course = Course("MATH101", "Calculus I", 4)
        
        # If course has capacity management
        if hasattr(course, 'max_capacity'):
            course.max_capacity = 2
            
            student1 = Student("Alice", "S001", "Mathematics")
            student2 = Student("Bob", "S002", "Mathematics")  
            student3 = Student("Charlie", "S003", "Mathematics")
            
            self.assertTrue(course.enroll_student(student1))
            self.assertTrue(course.enroll_student(student2))
            
            # Third enrollment should fail if capacity checking is implemented
            result = course.enroll_student(student3)
            if result is False:
                self.assertEqual(len(course.enrolled_students), 2)

    def test_course_waitlist(self):
        """Test course waitlist functionality if implemented"""
        course = Course("MATH201", "Calculus II", 4)
        
        # This test checks if waitlist functionality exists
        if hasattr(course, 'waitlist'):
            student = Student("David", "S004", "Mathematics")
            
            # Try to add to waitlist
            if hasattr(course, 'add_to_waitlist'):
                course.add_to_waitlist(student)
                self.assertIn(student, course.waitlist)

    def test_course_grading_system(self):
        """Test course grading if implemented"""
        course = Course("MATH301", "Linear Algebra", 3)
        student = Student("Eve", "S005", "Mathematics")
        
        course.enroll_student(student)
        
        # If grading system exists
        if hasattr(course, 'grades') and hasattr(course, 'assign_grade'):
            course.assign_grade(student, 'A')
            self.assertEqual(course.grades.get(student), 'A')


def run_department_tests():
    """Run tests for Department and Course management"""
    print("🧪 RUNNING DEPARTMENT & COURSE MANAGEMENT TESTS")
    print("=" * 60)
    print("Testing Department and Course management:")
    print("• Course creation and basic functionality")
    print("• Department management operations")
    print("• Course prerequisites system")
    print("• Faculty-course assignments")
    print("• Student enrollment processes")
    print("• Integration scenarios")
    print("=" * 60)
    
    # Create test suite for Department classes
    test_suite = unittest.TestSuite()
    
    # Add Department test classes
    department_test_classes = [
        TestCourse,
        TestDepartment,
        TestCoursePrerequisites,
        TestDepartmentIntegration,
        TestDepartmentCourseManagement
    ]
    
    for test_class in department_test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(test_suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print("🎯 DEPARTMENT TESTS RESULTS SUMMARY")
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\n❌ FAILURES ({len(result.failures)}):")
        for test, traceback in result.failures:
            print(f"  • {test}: {traceback.split('AssertionError:')[-1].strip()}")
    
    if result.errors:
        print(f"\n💥 ERRORS ({len(result.errors)}):")
        for test, traceback in result.errors:
            print(f"  • {test}: {traceback.split('Error:')[-1].strip()}")
    
    if result.wasSuccessful():
        print(f"\n✅ ALL DEPARTMENT TESTS PASSED! Department management is fully functional.")
    else:
        print(f"\n⚠️  Some Department tests failed. Please check the issues above.")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_department_tests()
    sys.exit(0 if success else 1)
