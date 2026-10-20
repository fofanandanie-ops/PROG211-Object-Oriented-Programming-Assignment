"""
Unit tests for the Student Record and Examination Results Management System.
Run with:  python -m unittest -v
"""

import io
import unittest
from contextlib import redirect_stdout

from main import Student, StudentRecordSystem, format_mark, load_demo_data


class TestStudent(unittest.TestCase):
    """Tests for the Student class."""

    def setUp(self):
        self.student = Student("luct100", "Test Student", "BSc Testing")

    def test_object_creation(self):
        self.assertEqual(self.student.student_id, "LUCT100")
        self.assertEqual(self.student.name, "Test Student")
        self.assertEqual(self.student.course, "BSc Testing")
        self.assertIsNone(self.student.mathematics_mark)
        self.assertIsNone(self.student.english_mark)
        self.assertIsNone(self.student.programming_mark)

    def test_empty_fields_rejected(self):
        with self.assertRaises(ValueError):
            Student("", "Name", "Course")
        with self.assertRaises(ValueError):
            Student("ID1", "   ", "Course")
        with self.assertRaises(ValueError):
            Student("ID1", "Name", "")

    def test_update_valid_marks(self):
        self.student.update_mark("mathematics", 80)
        self.student.update_mark("English", 65.5)
        self.student.update_mark(" programming ", 90)
        self.assertEqual(self.student.mathematics_mark, 80)
        self.assertEqual(self.student.english_mark, 65.5)
        self.assertEqual(self.student.programming_mark, 90)

    def test_boundary_marks_accepted(self):
        self.student.update_mark("mathematics", 0)
        self.student.update_mark("english", 100)
        self.assertEqual(self.student.mathematics_mark, 0)
        self.assertEqual(self.student.english_mark, 100)

    def test_invalid_marks_rejected(self):
        for bad_mark in (-1, 101, 100.5, "abc", "75", None, True):
            with self.assertRaises(ValueError):
                self.student.update_mark("mathematics", bad_mark)
        self.assertIsNone(self.student.mathematics_mark)

    def test_invalid_subject_rejected(self):
        with self.assertRaises(ValueError):
            self.student.update_mark("history", 50)

    def test_rejected_update_keeps_old_mark(self):
        self.student.update_mark("english", 70)
        with self.assertRaises(ValueError):
            self.student.update_mark("english", 150)
        self.assertEqual(self.student.english_mark, 70)

    def test_average_all_three_marks(self):
        self.student.update_mark("mathematics", 60)
        self.student.update_mark("english", 70)
        self.student.update_mark("programming", 80)
        self.assertAlmostEqual(self.student.calculate_average(), 70.0)

    def test_average_ignores_missing_marks(self):
        self.student.update_mark("mathematics", 60)
        self.student.update_mark("english", 80)
        # Missing programming mark must NOT be counted as zero.
        self.assertAlmostEqual(self.student.calculate_average(), 70.0)
        self.assertEqual(self.student.count_recorded_marks(), 2)

    def test_average_with_no_marks(self):
        self.assertIsNone(self.student.calculate_average())
        self.assertEqual(self.student.count_recorded_marks(), 0)

    def test_average_with_zero_mark(self):
        # A real mark of 0 IS counted, unlike a missing mark.
        self.student.update_mark("mathematics", 0)
        self.student.update_mark("english", 100)
        self.assertAlmostEqual(self.student.calculate_average(), 50.0)

    def test_display_info_output(self):
        output = io.StringIO()
        with redirect_stdout(output):
            self.student.display_info()
        text = output.getvalue()
        self.assertIn("LUCT100", text)
        self.assertIn("Not recorded", text)
        self.assertIn("No marks recorded yet", text)


class TestStudentRecordSystem(unittest.TestCase):
    """Tests for the StudentRecordSystem class."""

    def setUp(self):
        self.system = StudentRecordSystem()

    def test_one_list_of_student_objects(self):
        self.assertIsInstance(self.system.students, list)
        self.assertEqual(len(self.system.students), 0)
        self.system.register_student("S1", "Alpha Test", "Course A")
        self.assertIsInstance(self.system.students[0], Student)

    def test_register_student(self):
        student = self.system.register_student("  s1 ", " Alpha Test ", "Course A")
        self.assertEqual(len(self.system.students), 1)
        self.assertEqual(student.student_id, "S1")
        self.assertEqual(student.name, "Alpha Test")

    def test_duplicate_id_rejected(self):
        self.system.register_student("S1", "Alpha Test", "Course A")
        with self.assertRaises(ValueError):
            self.system.register_student("s1", "Beta Test", "Course B")
        self.assertEqual(len(self.system.students), 1)

    def test_register_empty_fields_rejected(self):
        with self.assertRaises(ValueError):
            self.system.register_student("", "Name", "Course")
        with self.assertRaises(ValueError):
            self.system.register_student("S2", "", "Course")
        with self.assertRaises(ValueError):
            self.system.register_student("S2", "Name", " ")
        self.assertEqual(len(self.system.students), 0)

    def test_find_student(self):
        self.system.register_student("S1", "Alpha Test", "Course A")
        self.assertIsNotNone(self.system.find_student("s1"))
        self.assertIsNone(self.system.find_student("UNKNOWN"))

    def test_update_student_mark(self):
        self.system.register_student("S1", "Alpha Test", "Course A")
        self.system.update_student_mark("S1", "programming", 88)
        self.assertEqual(self.system.find_student("S1").programming_mark, 88)

    def test_update_unknown_student_rejected(self):
        with self.assertRaises(ValueError):
            self.system.update_student_mark("NOPE", "english", 50)

    def test_update_student_invalid_mark_rejected(self):
        self.system.register_student("S1", "Alpha Test", "Course A")
        with self.assertRaises(ValueError):
            self.system.update_student_mark("S1", "english", 101)

    def test_display_all_students_empty(self):
        output = io.StringIO()
        with redirect_stdout(output):
            self.system.display_all_students()
        self.assertIn("No students registered yet", output.getvalue())

    def test_display_all_students(self):
        self.system.register_student("S1", "Alpha Test", "Course A")
        self.system.register_student("S2", "Beta Test", "Course B")
        output = io.StringIO()
        with redirect_stdout(output):
            self.system.display_all_students()
        text = output.getvalue()
        self.assertIn("Total students: 2", text)
        self.assertIn("Alpha Test", text)
        self.assertIn("Beta Test", text)

    def test_class_method_without_instance(self):
        output = io.StringIO()
        with redirect_stdout(output):
            StudentRecordSystem.display_system_information()
        text = output.getvalue()
        self.assertIn(StudentRecordSystem.SYSTEM_NAME, text)
        self.assertIn(StudentRecordSystem.VERSION, text)
        self.assertIn("StudentRecordSystem", text)

    def test_class_method_uses_cls(self):
        # A subclass changes the class data; the class method must use it.
        class CustomSystem(StudentRecordSystem):
            SYSTEM_NAME = "Custom Results System"

        output = io.StringIO()
        with redirect_stdout(output):
            CustomSystem.display_system_information()
        text = output.getvalue()
        self.assertIn("Custom Results System", text)
        self.assertIn("CustomSystem", text)

    def test_load_demo_data_no_duplicates(self):
        self.assertEqual(load_demo_data(self.system), 3)
        self.assertEqual(load_demo_data(self.system), 0)
        self.assertEqual(len(self.system.students), 3)


class TestHelpers(unittest.TestCase):
    """Tests for small helper functions."""

    def test_format_mark(self):
        self.assertEqual(format_mark(None), "Not recorded")
        self.assertEqual(format_mark(75.0), "75")
        self.assertEqual(format_mark(65.5), "65.50")


if __name__ == "__main__":
    unittest.main()
