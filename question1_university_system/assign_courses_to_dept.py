#!/usr/bin/env python3
"""
Course assignment utility for the university system.

This script assigns courses to departments in the university database.
It's a utility script for database management and course organization.
"""

import sys
import os
from typing import List, Tuple, Any

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database_manager import load_database, save_database
from department import Department, Course
from person import Person


def display_current_state(departments: List[Department], courses: List[Course]) -> None:
    """
    Display the current state of departments and courses.
    
    Args:
        departments: List of departments in the system.
        courses: List of courses in the system.
    """
    print(f"Current departments: {len(departments)}")
    for dept in departments:
        print(f"  - {dept.name} (Courses: {len(dept.courses)})")
    
    print(f"\nCurrent courses: {len(courses)}")
    for course in courses:
        print(f"  - {course.name} ({course.code})")


def assign_courses_to_departments() -> None:
    """
    Assign courses to departments in the university system.
    
    This function loads the database, assigns courses to the first available
    department, and saves the updated state back to the database.
    """
    print("=" * 50)
    print("ASSIGNING COURSES TO DEPARTMENTS")
    print("=" * 50)
    
    # Load current database
    departments, courses, people = load_database()
    
    display_current_state(departments, courses)
    
    # Example: Assign all courses to the first department
    if departments and courses:
        target_dept = departments[0]  # Use first department as target
        
        print(f"\nAssigning courses to '{target_dept.name}' department...")
        
        assigned_count = 0
        for course in courses:
            if course not in target_dept.courses:
                target_dept.add_course(course)
                print(f"  ✅ Added {course.name} to {target_dept.name}")
                assigned_count += 1
            else:
                print(f"  ℹ️  {course.name} already in {target_dept.name}")
        
        # Save updated database
        if assigned_count > 0:
            success = save_database(departments, courses, people)
            if success:
                print(f"\n✅ Database updated successfully! ({assigned_count} courses assigned)")
            else:
                print("\n❌ Failed to save database changes")
        else:
            print("\n✅ No changes needed - all courses already assigned")
        
        # Show final state
        print(f"\n'{target_dept.name}' department statistics:")
        stats = target_dept.get_department_stats()
        for key, value in stats.items():
            print(f"  - {key.replace('_', ' ').title()}: {value}")
    
    else:
        print("\n❌ No departments or courses found in the database!")
        print("Please add departments and courses first.")


def main() -> None:
    """Main function to run the course assignment utility."""
    try:
        assign_courses_to_departments()
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
