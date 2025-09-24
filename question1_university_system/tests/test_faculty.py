#!/usr/bin/env python3
"""
Unit Tests for Faculty Class

This module contains unit tests specifically for the Faculty class and its
inheritance hierarchy. Tests cover:
- Faculty class initialization and basic functionality
- Method overriding (get_responsibilities, calculate_workload)
- Professor, Lecturer, and TA inheritance
- Polymorphic behavior across faculty types
- Faculty-specific features
"""

import unittest
import sys
import os

# Add the parent directory to Python path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from person import Person
from faculty import Faculty, Professor, Lecturer, TA


class TestFaculty(unittest.TestCase):
    """Test Faculty class functionality"""
    
    def setUp(self):
        """Set up test instances"""
        self.faculty = Faculty("Dr. Base", "F001", "Mathematics")

    def test_faculty_initialization(self):
        """Test Faculty class initialization"""
        self.assertEqual(self.faculty.name, "Dr. Base")
        self.assertEqual(self.faculty.person_id, "F001")
        self.assertEqual(self.faculty.department, "Mathematics")

    def test_faculty_inheritance_from_person(self):
        """Test Faculty inherits from Person correctly"""
        self.assertIsInstance(self.faculty, Person)
        self.assertIsInstance(self.faculty, Faculty)
        
    def test_faculty_responsibilities(self):
        """Test Faculty get_responsibilities method"""
        self.assertEqual(self.faculty.get_responsibilities(), "Teach and research")
        
        # Should be different from Person's default
        person = Person("Test", "T001")
        self.assertNotEqual(self.faculty.get_responsibilities(), person.get_responsibilities())

    def test_faculty_workload(self):
        """Test Faculty calculate_workload method"""
        self.assertEqual(self.faculty.calculate_workload(), "Standard workload")

    def test_faculty_string_representation(self):
        """Test Faculty __str__ method"""
        expected = "Faculty: Dr. Base (ID: F001, Dept: Mathematics)"
        self.assertEqual(str(self.faculty), expected)


class TestProfessor(unittest.TestCase):
    """Test Professor class inheritance and functionality"""
    
    def setUp(self):
        """Set up test instances"""
        self.professor = Professor("Dr. Smith", "F002", "Computer Science")

    def test_professor_initialization(self):
        """Test Professor initialization inherits correctly"""
        self.assertEqual(self.professor.name, "Dr. Smith")
        self.assertEqual(self.professor.person_id, "F002")
        self.assertEqual(self.professor.department, "Computer Science")

    def test_professor_inheritance(self):
        """Test Professor inherits from Faculty and Person"""
        self.assertIsInstance(self.professor, Professor)
        self.assertIsInstance(self.professor, Faculty)
        self.assertIsInstance(self.professor, Person)

    def test_professor_method_overriding(self):
        """Test Professor overrides Faculty methods correctly"""
        # Test responsibilities override
        expected_resp = "Teach, conduct research, mentor graduate students, and publish papers"
        self.assertEqual(self.professor.get_responsibilities(), expected_resp)
        
        # Test workload override
        expected_workload = "High workload with research responsibilities"
        self.assertEqual(self.professor.calculate_workload(), expected_workload)
        
        # Should be different from base Faculty
        base_faculty = Faculty("Base", "F999", "Test")
        self.assertNotEqual(self.professor.get_responsibilities(), base_faculty.get_responsibilities())
        self.assertNotEqual(self.professor.calculate_workload(), base_faculty.calculate_workload())

    def test_professor_string_representation(self):
        """Test Professor __str__ method"""
        expected = "Professor: Dr. Smith (ID: F002, Dept: Computer Science)"
        self.assertEqual(str(self.professor), expected)


class TestLecturer(unittest.TestCase):
    """Test Lecturer class inheritance and functionality"""
    
    def setUp(self):
        """Set up test instances"""
        self.lecturer = Lecturer("Mr. Brown", "F003", "Mathematics")

    def test_lecturer_initialization(self):
        """Test Lecturer initialization inherits correctly"""
        self.assertEqual(self.lecturer.name, "Mr. Brown")
        self.assertEqual(self.lecturer.person_id, "F003")
        self.assertEqual(self.lecturer.department, "Mathematics")

    def test_lecturer_inheritance(self):
        """Test Lecturer inherits from Faculty and Person"""
        self.assertIsInstance(self.lecturer, Lecturer)
        self.assertIsInstance(self.lecturer, Faculty)
        self.assertIsInstance(self.lecturer, Person)

    def test_lecturer_method_overriding(self):
        """Test Lecturer overrides Faculty methods correctly"""
        # Test responsibilities override
        expected_resp = "Teach courses and support student learning"
        self.assertEqual(self.lecturer.get_responsibilities(), expected_resp)
        
        # Test workload override
        expected_workload = "Teaching-focused workload"
        self.assertEqual(self.lecturer.calculate_workload(), expected_workload)

    def test_lecturer_string_representation(self):
        """Test Lecturer __str__ method"""
        expected = "Lecturer: Mr. Brown (ID: F003, Dept: Mathematics)"
        self.assertEqual(str(self.lecturer), expected)


class TestTA(unittest.TestCase):
    """Test TA (Teaching Assistant) class inheritance and functionality"""
    
    def setUp(self):
        """Set up test instances"""
        self.ta = TA("Sarah Davis", "F004", "Physics")

    def test_ta_initialization(self):
        """Test TA initialization inherits correctly"""
        self.assertEqual(self.ta.name, "Sarah Davis")
        self.assertEqual(self.ta.person_id, "F004")
        self.assertEqual(self.ta.department, "Physics")

    def test_ta_inheritance(self):
        """Test TA inherits from Faculty and Person"""
        self.assertIsInstance(self.ta, TA)
        self.assertIsInstance(self.ta, Faculty)
        self.assertIsInstance(self.ta, Person)

    def test_ta_method_overriding(self):
        """Test TA overrides Faculty methods correctly"""
        # Test responsibilities override
        expected_resp = "Assist with teaching, grading, and student support"
        self.assertEqual(self.ta.get_responsibilities(), expected_resp)
        
        # Test workload override
        expected_workload = "Assist in teaching and grading"
        self.assertEqual(self.ta.calculate_workload(), expected_workload)

    def test_ta_string_representation(self):
        """Test TA __str__ method"""
        expected = "TA: Sarah Davis (ID: F004, Dept: Physics)"
        self.assertEqual(str(self.ta), expected)


class TestFacultyPolymorphism(unittest.TestCase):
    """Test polymorphic behavior across faculty types"""
    
    def setUp(self):
        """Set up test instances of all faculty types"""
        self.faculty = Faculty("Dr. Base", "F001", "Mathematics")
        self.professor = Professor("Dr. Smith", "F002", "Computer Science")
        self.lecturer = Lecturer("Mr. Brown", "F003", "Mathematics")
        self.ta = TA("Sarah Davis", "F004", "Physics")
        self.faculty_list = [self.faculty, self.professor, self.lecturer, self.ta]

    def test_polymorphic_responsibilities(self):
        """Test polymorphic behavior of get_responsibilities method"""
        expected_responsibilities = [
            "Teach and research",
            "Teach, conduct research, mentor graduate students, and publish papers",
            "Teach courses and support student learning",
            "Assist with teaching, grading, and student support"
        ]
        
        actual_responsibilities = [f.get_responsibilities() for f in self.faculty_list]
        self.assertEqual(actual_responsibilities, expected_responsibilities)

    def test_polymorphic_workload(self):
        """Test polymorphic behavior of calculate_workload method"""
        expected_workloads = [
            "Standard workload",
            "High workload with research responsibilities",
            "Teaching-focused workload",
            "Assist in teaching and grading"
        ]
        
        actual_workloads = [f.calculate_workload() for f in self.faculty_list]
        self.assertEqual(actual_workloads, expected_workloads)

    def test_unique_behaviors(self):
        """Test that all faculty types have unique behaviors"""
        # Test that all have different responsibilities
        responsibilities = [f.get_responsibilities() for f in self.faculty_list]
        self.assertEqual(len(set(responsibilities)), 4)  # All should be unique
        
        # Test that all have different workloads  
        workloads = [f.calculate_workload() for f in self.faculty_list]
        self.assertEqual(len(set(workloads)), 4)  # All should be unique

    def test_common_interface(self):
        """Test that all faculty types share common interface"""
        for faculty in self.faculty_list:
            # Test common methods exist
            self.assertTrue(hasattr(faculty, 'get_responsibilities'))
            self.assertTrue(hasattr(faculty, 'calculate_workload'))
            
            # Test common attributes exist
            self.assertTrue(hasattr(faculty, 'name'))
            self.assertTrue(hasattr(faculty, 'person_id'))
            self.assertTrue(hasattr(faculty, 'department'))
            
            # Test all are instances of Faculty and Person
            self.assertIsInstance(faculty, Faculty)
            self.assertIsInstance(faculty, Person)

    def test_method_call_consistency(self):
        """Test that method calls work consistently across all types"""
        for faculty in self.faculty_list:
            # Test that methods return strings
            self.assertIsInstance(faculty.get_responsibilities(), str)
            self.assertIsInstance(faculty.calculate_workload(), str)
            
            # Test that methods return non-empty strings
            self.assertTrue(len(faculty.get_responsibilities()) > 0)
            self.assertTrue(len(faculty.calculate_workload()) > 0)


class TestFacultyIntegration(unittest.TestCase):
    """Test integration scenarios for Faculty classes"""
    
    def test_department_faculty_scenario(self):
        """Test scenario with multiple faculty types in same department"""
        cs_faculty = [
            Faculty("Dr. General", "F100", "Computer Science"),
            Professor("Dr. Research", "F101", "Computer Science"),
            Lecturer("Mr. Teacher", "F102", "Computer Science"),
            TA("Ms. Helper", "F103", "Computer Science")
        ]
        
        # All should be in same department
        for faculty in cs_faculty:
            self.assertEqual(faculty.department, "Computer Science")
        
        # All should have different roles/responsibilities
        responsibilities = [f.get_responsibilities() for f in cs_faculty]
        self.assertEqual(len(set(responsibilities)), 4)

    def test_faculty_hierarchy_validation(self):
        """Test that faculty hierarchy relationships are correct"""
        professor = Professor("Test Prof", "F200", "Test")
        lecturer = Lecturer("Test Lecturer", "F201", "Test")
        ta = TA("Test TA", "F202", "Test")
        
        # Test direct inheritance
        self.assertTrue(issubclass(Professor, Faculty))
        self.assertTrue(issubclass(Lecturer, Faculty))
        self.assertTrue(issubclass(TA, Faculty))
        
        # Test transitive inheritance
        self.assertTrue(issubclass(Professor, Person))
        self.assertTrue(issubclass(Lecturer, Person))
        self.assertTrue(issubclass(TA, Person))
        
        # Test instance relationships
        self.assertIsInstance(professor, (Professor, Faculty, Person))
        self.assertIsInstance(lecturer, (Lecturer, Faculty, Person))
        self.assertIsInstance(ta, (TA, Faculty, Person))


def run_faculty_tests():
    """Run tests for Faculty classes only"""
    print("🧪 RUNNING FACULTY CLASS TESTS")
    print("=" * 60)
    print("Testing Faculty class hierarchy:")
    print("• Faculty base class functionality")
    print("• Professor inheritance and research focus")
    print("• Lecturer inheritance and teaching focus")
    print("• TA inheritance and assistant role")
    print("• Polymorphic behavior across faculty types")
    print("• Integration scenarios")
    print("=" * 60)
    
    # Create test suite for Faculty classes
    test_suite = unittest.TestSuite()
    
    # Add Faculty test classes
    faculty_test_classes = [
        TestFaculty,
        TestProfessor,
        TestLecturer,
        TestTA,
        TestFacultyPolymorphism,
        TestFacultyIntegration
    ]
    
    for test_class in faculty_test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(test_suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print("🎯 FACULTY TESTS RESULTS SUMMARY")
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
        print(f"\n✅ ALL FACULTY TESTS PASSED! Faculty classes are fully functional.")
    else:
        print(f"\n⚠️  Some Faculty tests failed. Please check the issues above.")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_faculty_tests()
    sys.exit(0 if success else 1)
