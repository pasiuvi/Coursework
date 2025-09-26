#!/usr/bin/env python3
"""
Unit Tests for Person Class

This module contains unit tests specifically for the Person class and its
direct inheritance (Staff class). Tests cover:
- Person class initialization
- Method functionality (get_responsibilities)
- String representation
- Staff inheritance from Person
- Method overriding
"""

import unittest
import sys
import os

# Add the parent directory to Python path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from person import Person, Staff


class TestPerson(unittest.TestCase):
    """Test Person class functionality"""
    
    def setUp(self):
        """Set up test instances"""
        self.person = Person("John Doe", "P001")

    def test_person_initialization(self):
        """Test Person class initialization"""
        self.assertEqual(self.person.name, "John Doe")
        self.assertEqual(self.person.person_id, "P001")
        
    def test_person_responsibilities(self):
        """Test Person get_responsibilities method"""
        self.assertEqual(self.person.get_responsibilities(), "General responsibilities")
        
    def test_person_string_representation(self):
        """Test Person __str__ method"""
        expected = "Person: John Doe (ID: P001)"
        self.assertEqual(str(self.person), expected)

    def test_person_repr_method(self):
        """Test Person __repr__ method"""
        expected = "Person(name='John Doe', person_id='P001')"
        self.assertEqual(repr(self.person), expected)


class TestStaff(unittest.TestCase):
    """Test Staff class inheritance and functionality"""
    
    def setUp(self):
        """Set up test instances"""
        self.staff = Staff("Admin User", "ST001", "HR")

    def test_staff_initialization(self):
        """Test Staff class initialization with proper inheritance"""
        # Test inherited attributes from Person
        self.assertEqual(self.staff.name, "Admin User")
        self.assertEqual(self.staff.person_id, "ST001")
        
        # Test Staff-specific attributes
        self.assertEqual(self.staff.department, "HR")

    def test_staff_inheritance_from_person(self):
        """Test Staff inherits from Person correctly"""
        self.assertIsInstance(self.staff, Person)
        self.assertIsInstance(self.staff, Staff)

    def test_staff_method_overriding(self):
        """Test Staff overrides Person methods correctly"""
        # Test method overriding
        self.assertEqual(self.staff.get_responsibilities(), "Administrative duties")
        # Should be different from Person's default
        person = Person("Test", "T001")
        self.assertNotEqual(self.staff.get_responsibilities(), person.get_responsibilities())

    def test_staff_string_representation(self):
        """Test Staff __str__ method"""
        expected = "Staff: Admin User (ID: ST001, Dept: HR)"
        self.assertEqual(str(self.staff), expected)

    def test_staff_default_department(self):
        """Test Staff with default department parameter"""
        default_staff = Staff("Default User", "ST002")
        self.assertEqual(default_staff.department, "Administration")


def run_person_tests():
    """Run tests for Person class only"""
    print("🧪 RUNNING PERSON CLASS TESTS")
    print("=" * 60)
    print("Testing Person base class and Staff inheritance:")
    print("• Person class initialization and methods")
    print("• Staff inheritance from Person")
    print("• Method overriding in Staff")
    print("• String representations")
    print("=" * 60)
    
    # Create test suite for Person classes
    test_suite = unittest.TestSuite()
    
    # Add Person test classes
    person_test_classes = [TestPerson, TestStaff]
    
    for test_class in person_test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(test_suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print("🎯 PERSON TESTS RESULTS SUMMARY")
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
        print(f"\n✅ ALL PERSON TESTS PASSED! Person and Staff classes are functional.")
    else:
        print(f"\n⚠️  Some Person tests failed. Please check the issues above.")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_person_tests()
    sys.exit(0 if success else 1)
