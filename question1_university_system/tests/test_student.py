#!/usr/bin/env python3
"""
Unit Tests for Student Class

This module contains unit tests specifically for the Student class and its
inheritance hierarchy. Tests cover:
- Student class initialization and basic functionality
- Course enrollment and dropping
- GPA calculation and academic status
- UndergraduateStudent and GraduateStudent inheritance
- Student management features
"""

import unittest
import sys
import os

# Add the parent directory to Python path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from person import Person
from student import Student, UndergraduateStudent, GraduateStudent


class TestStudent(unittest.TestCase):
    """Test Student class functionality"""
    
    def setUp(self):
        """Set up test instances"""
        self.student = Student("Jane Smith", "S001", "Computer Science")

    def test_student_initialization(self):
        """Test Student class initialization"""
        self.assertEqual(self.student.name, "Jane Smith")
        self.assertEqual(self.student.person_id, "S001")
        self.assertEqual(self.student.major, "Computer Science")
        self.assertEqual(len(self.student.courses), 0)
        self.assertEqual(len(self.student.grades), 0)
        self.assertIsInstance(self.student.courses, list)
        self.assertIsInstance(self.student.grades, dict)

    def test_student_inheritance_from_person(self):
        """Test Student inherits from Person correctly"""
        self.assertIsInstance(self.student, Person)
        self.assertIsInstance(self.student, Student)
        
        # Test inherited methods
        self.assertEqual(self.student.get_responsibilities(), "Study and attend classes")

    def test_course_enrollment(self):
        """Test course enrollment functionality"""
        # Test enrolling in a single course
        self.student.enroll_course("CS101")
        self.assertIn("CS101", self.student.courses)
        self.assertEqual(len(self.student.courses), 1)
        
        # Test enrolling in multiple courses
        self.student.enroll_course("MATH201")
        self.student.enroll_course("ENG101")
        self.assertEqual(len(self.student.courses), 3)
        self.assertIn("MATH201", self.student.courses)
        self.assertIn("ENG101", self.student.courses)
        
        # Test duplicate enrollment (should not add duplicate)
        initial_count = len(self.student.courses)
        self.student.enroll_course("CS101")
        self.assertEqual(len(self.student.courses), initial_count)

    def test_course_dropping(self):
        """Test course dropping functionality"""
        # Enroll in courses first
        self.student.enroll_course("CS101")
        self.student.enroll_course("MATH201")
        self.assertEqual(len(self.student.courses), 2)
        
        # Drop a course
        self.student.drop_course("CS101")
        self.assertNotIn("CS101", self.student.courses)
        self.assertEqual(len(self.student.courses), 1)
        self.assertIn("MATH201", self.student.courses)
        
        # Try to drop a course not enrolled in
        initial_count = len(self.student.courses)
        self.student.drop_course("NONEXISTENT")
        self.assertEqual(len(self.student.courses), initial_count)

    def test_gpa_calculation(self):
        """Test GPA calculation functionality"""
        # Test with no grades
        self.assertEqual(self.student.calculate_gpa(), 0.0)
        
        # Test with single grade
        self.student.grades["CS101"] = 3.7
        self.assertAlmostEqual(self.student.calculate_gpa(), 3.7, places=2)
        
        # Test with multiple grades
        self.student.grades["MATH201"] = 3.5
        self.student.grades["ENG101"] = 3.8
        expected_gpa = (3.7 + 3.5 + 3.8) / 3
        self.assertAlmostEqual(self.student.calculate_gpa(), expected_gpa, places=2)
        
        # Test with perfect grades
        perfect_student = Student("Perfect", "S999", "Test")
        perfect_student.grades = {"TEST1": 4.0, "TEST2": 4.0, "TEST3": 4.0}
        self.assertEqual(perfect_student.calculate_gpa(), 4.0)

    def test_academic_status(self):
        """Test academic status determination"""
        # Test Dean's List (GPA >= 3.5)
        self.student.grades = {"CS101": 3.8, "MATH201": 3.6}
        self.assertEqual(self.student.get_academic_status(), "Dean's List")
        
        # Test Good Standing (2.0 <= GPA < 3.5)
        self.student.grades = {"CS101": 2.5, "MATH201": 2.8}
        self.assertEqual(self.student.get_academic_status(), "Good Standing")
        
        # Test Probation (GPA < 2.0)
        self.student.grades = {"CS101": 1.5, "MATH201": 1.8}
        self.assertEqual(self.student.get_academic_status(), "Probation")
        
        # Test edge cases
        self.student.grades = {"CS101": 3.5}  # Exactly 3.5
        self.assertEqual(self.student.get_academic_status(), "Dean's List")
        
        self.student.grades = {"CS101": 2.0}  # Exactly 2.0
        self.assertEqual(self.student.get_academic_status(), "Good Standing")

    def test_student_string_representation(self):
        """Test Student __str__ method"""
        expected = "Student: Jane Smith (ID: S001, Major: Computer Science)"
        self.assertEqual(str(self.student), expected)


class TestUndergraduateStudent(unittest.TestCase):
    """Test UndergraduateStudent class inheritance"""
    
    def setUp(self):
        """Set up test instances"""
        self.undergrad = UndergraduateStudent("Alice Johnson", "S002", "Mathematics")

    def test_undergraduate_initialization(self):
        """Test UndergraduateStudent initialization"""
        self.assertEqual(self.undergrad.name, "Alice Johnson")
        self.assertEqual(self.undergrad.person_id, "S002")
        self.assertEqual(self.undergrad.major, "Mathematics")

    def test_undergraduate_inheritance(self):
        """Test UndergraduateStudent inherits correctly"""
        self.assertIsInstance(self.undergrad, UndergraduateStudent)
        self.assertIsInstance(self.undergrad, Student)
        self.assertIsInstance(self.undergrad, Person)

    def test_undergraduate_functionality(self):
        """Test UndergraduateStudent has all Student functionality"""
        # Test course enrollment
        self.undergrad.enroll_course("MATH101")
        self.assertIn("MATH101", self.undergrad.courses)
        
        # Test GPA calculation
        self.undergrad.grades["MATH101"] = 3.5
        self.assertEqual(self.undergrad.calculate_gpa(), 3.5)
        
        # Test academic status
        self.assertEqual(self.undergrad.get_academic_status(), "Dean's List")
        
        # Test responsibilities
        self.assertEqual(self.undergrad.get_responsibilities(), "Study and attend classes")

    def test_undergraduate_string_representation(self):
        """Test UndergraduateStudent __str__ method"""
        expected = "UndergraduateStudent: Alice Johnson (ID: S002, Major: Mathematics)"
        self.assertEqual(str(self.undergrad), expected)


class TestGraduateStudent(unittest.TestCase):
    """Test GraduateStudent class inheritance and specific features"""
    
    def setUp(self):
        """Set up test instances"""
        self.grad = GraduateStudent("Bob Wilson", "S003", "Physics")

    def test_graduate_initialization(self):
        """Test GraduateStudent initialization"""
        self.assertEqual(self.grad.name, "Bob Wilson")
        self.assertEqual(self.grad.person_id, "S003")
        self.assertEqual(self.grad.major, "Physics")

    def test_graduate_inheritance(self):
        """Test GraduateStudent inherits correctly"""
        self.assertIsInstance(self.grad, GraduateStudent)
        self.assertIsInstance(self.grad, Student)
        self.assertIsInstance(self.grad, Person)

    def test_graduate_specific_features(self):
        """Test GraduateStudent specific methods"""
        # Test degree type method
        self.assertEqual(self.grad.get_degree_type(), "Master's/Doctoral Degree")

    def test_graduate_functionality(self):
        """Test GraduateStudent has all Student functionality"""
        # Test course enrollment
        self.grad.enroll_course("PHYS501")
        self.assertIn("PHYS501", self.grad.courses)
        
        # Test GPA calculation
        self.grad.grades["PHYS501"] = 3.9
        self.assertEqual(self.grad.calculate_gpa(), 3.9)
        
        # Test academic status
        self.assertEqual(self.grad.get_academic_status(), "Dean's List")

    def test_graduate_string_representation(self):
        """Test GraduateStudent __str__ method"""
        expected = "GraduateStudent: Bob Wilson (ID: S003, Major: Physics)"
        self.assertEqual(str(self.grad), expected)


class TestStudentIntegration(unittest.TestCase):
    """Test integration scenarios for Student classes"""
    
    def test_multiple_students_scenario(self):
        """Test scenario with multiple students of different types"""
        # Create students
        regular = Student("Regular Student", "S100", "General")
        undergrad = UndergraduateStudent("Undergrad Student", "S101", "CS")
        grad = GraduateStudent("Graduate Student", "S102", "Math")
        
        students = [regular, undergrad, grad]
        
        # Enroll all in same course
        for student in students:
            student.enroll_course("GEN101")
            student.grades["GEN101"] = 3.7
        
        # Test all have same GPA
        for student in students:
            self.assertAlmostEqual(student.calculate_gpa(), 3.7, places=2)
            self.assertEqual(student.get_academic_status(), "Dean's List")
        
        # Test polymorphism - all respond to same methods
        for student in students:
            self.assertTrue(hasattr(student, 'enroll_course'))
            self.assertTrue(hasattr(student, 'calculate_gpa'))
            self.assertTrue(hasattr(student, 'get_academic_status'))

    def test_comprehensive_student_workflow(self):
        """Test complete student management workflow"""
        student = UndergraduateStudent("Test Student", "S200", "Engineering")
        
        # Phase 1: Initial enrollment
        courses_phase1 = ["ENG101", "MATH101", "CHEM101"]
        for course in courses_phase1:
            student.enroll_course(course)
        
        self.assertEqual(len(student.courses), 3)
        
        # Phase 2: Add grades
        grades_phase1 = {"ENG101": 3.5, "MATH101": 3.8, "CHEM101": 3.6}
        student.grades.update(grades_phase1)
        
        first_gpa = student.calculate_gpa()
        self.assertAlmostEqual(first_gpa, 3.63, places=2)
        self.assertEqual(student.get_academic_status(), "Dean's List")
        
        # Phase 3: Add more courses
        courses_phase2 = ["ENG102", "MATH102"]
        for course in courses_phase2:
            student.enroll_course(course)
        
        grades_phase2 = {"ENG102": 3.9, "MATH102": 3.7}
        student.grades.update(grades_phase2)
        
        final_gpa = student.calculate_gpa()
        expected_gpa = sum(grades_phase1.values() + list(grades_phase2.values())) / 5
        self.assertAlmostEqual(final_gpa, expected_gpa, places=2)
        
        # Phase 4: Drop a course
        student.drop_course("CHEM101")
        self.assertNotIn("CHEM101", student.courses)
        self.assertEqual(len(student.courses), 4)


def run_student_tests():
    """Run tests for Student classes only"""
    print("🧪 RUNNING STUDENT CLASS TESTS")
    print("=" * 60)
    print("Testing Student class hierarchy:")
    print("• Student base class functionality")
    print("• Course enrollment and management")
    print("• GPA calculation and academic status")
    print("• UndergraduateStudent inheritance")
    print("• GraduateStudent inheritance and features")
    print("• Integration scenarios")
    print("=" * 60)
    
    # Create test suite for Student classes
    test_suite = unittest.TestSuite()
    
    # Add Student test classes
    student_test_classes = [
        TestStudent,
        TestUndergraduateStudent,
        TestGraduateStudent,
        TestStudentIntegration
    ]
    
    for test_class in student_test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(test_suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print("🎯 STUDENT TESTS RESULTS SUMMARY")
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
        print(f"\n✅ ALL STUDENT TESTS PASSED! Student classes are fully functional.")
    else:
        print(f"\n⚠️  Some Student tests failed. Please check the issues above.")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_student_tests()
    sys.exit(0 if success else 1)
