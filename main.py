"""
Student Record and Examination Results Management System
PROG211 - Object-Oriented Programming 1 (Education domain)

A simple terminal program that stores student records and examination
marks using Object-Oriented Programming.

All data used by this program is FICTIONAL demonstration data.
Nothing is saved to disk, so no personal information is stored.
"""


def format_mark(mark):
    """Return a mark as readable text, or 'Not recorded' if it is missing."""
    if mark is None:
        return "Not recorded"
    if mark == int(mark):
        return str(int(mark))
    return f"{mark:.2f}"


class Student:
    """Represents ONE student and their three examination marks."""

    # Class-level constants shared by every Student object.
    MIN_MARK = 0
    MAX_MARK = 100

    def __init__(self, student_id, name, course):
        """Constructor: runs automatically when a new Student object is created."""
        student_id = str(student_id).strip()
        name = str(name).strip()
        course = str(course).strip()

        if student_id == "":
            raise ValueError("Student ID cannot be empty.")
        if name == "":
            raise ValueError("Student name cannot be empty.")
        if course == "":
            raise ValueError("Course cannot be empty.")

        # Instance attributes: every Student object has its own copy.
        self.student_id = student_id.upper()
        self.name = name
        self.course = course

        # None means "no mark recorded yet" (this is NOT the same as 0).
        self.mathematics_mark = None
        self.english_mark = None
        self.programming_mark = None

    def update_mark(self, subject, mark):
        """Instance method: record or change the mark for one subject.

        subject must be 'mathematics', 'english' or 'programming'.
        mark must be a number from 0 to 100 (inclusive).
        """
        # Check the mark is a real number (True/False are not accepted).
        if isinstance(mark, bool) or not isinstance(mark, (int, float)):
            raise ValueError("Mark must be a number.")
        if not (Student.MIN_MARK <= mark <= Student.MAX_MARK):
            raise ValueError(
                f"Mark must be between {Student.MIN_MARK} and {Student.MAX_MARK}."
            )

        subject = str(subject).strip().lower()
        if subject == "mathematics":
            self.mathematics_mark = mark
        elif subject == "english":
            self.english_mark = mark
        elif subject == "programming":
            self.programming_mark = mark
        else:
            raise ValueError(
                "Invalid subject. Choose mathematics, english or programming."
            )

    def count_recorded_marks(self):
        """Instance method: return how many of the three marks are recorded."""
        count = 0
        if self.mathematics_mark is not None:
            count += 1
        if self.english_mark is not None:
            count += 1
        if self.programming_mark is not None:
            count += 1
        return count

    def calculate_average(self):
        """Instance method: return the average of the RECORDED marks only.

        Returns None if no marks have been recorded yet.
        Missing marks are skipped, never counted as zero.
        """
        count = self.count_recorded_marks()
        if count == 0:
            return None

        total = 0
        if self.mathematics_mark is not None:
            total += self.mathematics_mark
        if self.english_mark is not None:
            total += self.english_mark
        if self.programming_mark is not None:
            total += self.programming_mark
        return total / count

    def display_info(self):
        """Instance method: print this student's details and results."""
        print(f"Student ID  : {self.student_id}")
        print(f"Name        : {self.name}")
        print(f"Course      : {self.course}")
        print(f"Mathematics : {format_mark(self.mathematics_mark)}")
        print(f"English     : {format_mark(self.english_mark)}")
        print(f"Programming : {format_mark(self.programming_mark)}")

        average = self.calculate_average()
        if average is None:
            print("Average     : No marks recorded yet")
        else:
            print(
                f"Average     : {average:.2f} "
                f"(based on {self.count_recorded_marks()} of 3 subjects)"
            )


class StudentRecordSystem:
    """Manages MANY Student objects stored in one list."""

    # Class-level information shared by the whole system.
    SYSTEM_NAME = "Student Record and Examination Results Management System"
    VERSION = "1.0"
    SUBJECTS_TEXT = "Mathematics, English, Programming"
    DATA_NOTICE = "Uses fictional demonstration data only. Nothing is saved to disk."

    def __init__(self):
        """Constructor: create an empty record system."""
        # The ONE primary data structure: a list of Student objects.
        self.students = []

    def register_student(self, student_id, name, course):
        """Add a new student record to the list.

        Raises ValueError for empty fields or a duplicate student ID.
        Returns the new Student object.
        """
        # Creating the Student object also validates empty fields.
        new_student = Student(student_id, name, course)

        if self.find_student(new_student.student_id) is not None:
            raise ValueError(
                f"Student ID '{new_student.student_id}' is already registered."
            )

        self.students.append(new_student)
        return new_student

    def find_student(self, student_id):
        """Search the list for a student ID. Returns the Student or None."""
        search_id = str(student_id).strip().upper()
        for student in self.students:
            if student.student_id == search_id:
                return student
        return None

    def display_all_students(self):
        """Display every student record in the list."""
        if len(self.students) == 0:
            print("No students registered yet.")
            return

        print(f"Total students: {len(self.students)}")
        for student in self.students:
            print("-" * 45)
            # Interaction between objects: the system asks each
            # Student object to display its own information.
            student.display_info()
        print("-" * 45)

    def update_student_mark(self, student_id, subject, mark):
        """Find a student and update one of their marks.

        Raises ValueError if the student ID is unknown, or if the
        subject or mark is invalid.
        """
        student = self.find_student(student_id)
        if student is None:
            raise ValueError(f"No student found with ID '{student_id}'.")
        # Interaction between objects: the system calls a Student method.
        student.update_mark(subject, mark)
        return student

    @classmethod
    def display_system_information(cls):
        """Class method: show information about the system itself.

        It receives 'cls' (the class), not 'self' (one object), because
        this information belongs to the whole system and does not depend
        on any particular student list. It can be called without
        creating an object: StudentRecordSystem.display_system_information()
        """
        print(f"System   : {cls.SYSTEM_NAME}")
        print(f"Version  : {cls.VERSION}")
        print(f"Class    : {cls.__name__}")
        print(f"Subjects : {cls.SUBJECTS_TEXT}")
        print(f"Marks    : {Student.MIN_MARK} to {Student.MAX_MARK}")
        print(f"Privacy  : {cls.DATA_NOTICE}")


# ----------------------------------------------------------------------
# Terminal menu helper functions
# ----------------------------------------------------------------------

def get_non_empty_input(prompt):
    """Keep asking until the user types something that is not empty."""
    while True:
        value = input(prompt).strip()
        if value != "":
            return value
        print("Error: this field cannot be empty. Please try again.")


def get_mark_input(prompt):
    """Keep asking until the user types a number from 0 to 100."""
    while True:
        text = input(prompt).strip()
        try:
            mark = float(text)
        except ValueError:
            print("Error: please enter a number, for example 75.")
            continue
        if Student.MIN_MARK <= mark <= Student.MAX_MARK:
            return mark
        print(f"Error: mark must be between {Student.MIN_MARK} and {Student.MAX_MARK}.")


def get_subject_input():
    """Ask the user to choose a subject. Returns the subject name."""
    while True:
        print("Subjects: 1. Mathematics  2. English  3. Programming")
        choice = input("Choose a subject (1-3): ").strip()
        if choice == "1":
            return "mathematics"
        elif choice == "2":
            return "english"
        elif choice == "3":
            return "programming"
        print("Error: invalid subject. Please enter 1, 2 or 3.")


def add_demo_student(system, student_id, name, course,
                     maths=None, english=None, programming=None):
    """Register one fictional student and record any marks given.

    Returns True if added, or False if the ID already exists.
    """
    try:
        system.register_student(student_id, name, course)
    except ValueError:
        return False  # Already loaded, skip duplicates.
    if maths is not None:
        system.update_student_mark(student_id, "mathematics", maths)
    if english is not None:
        system.update_student_mark(student_id, "english", english)
    if programming is not None:
        system.update_student_mark(student_id, "programming", programming)
    return True


def load_demo_data(system):
    """Add FICTIONAL demonstration students (not real people).

    Returns how many students were newly added.
    """
    added = 0
    if add_demo_student(system, "LUCT001", "Aminata Example",
                        "BSc Software Engineering", 78, 65, 90):
        added += 1
    if add_demo_student(system, "LUCT002", "Mohamed Sample",
                        "BSc Information Technology", 55, 70):
        added += 1
    if add_demo_student(system, "LUCT003", "Isatu Demo",
                        "Diploma in Business IT"):
        added += 1
    return added


def show_menu():
    """Print the main menu."""
    print()
    print("=" * 45)
    print(" STUDENT RECORD AND EXAM RESULTS SYSTEM")
    print("=" * 45)
    print("1. Register a new student")
    print("2. Record or update an exam mark")
    print("3. Display all students")
    print("4. Search for a student by ID")
    print("5. Show a student's average mark")
    print("6. Load fictional demo data")
    print("7. Display system information")
    print("0. Exit")


def run_menu(system):
    """Main menu loop. Runs until the user chooses 0 (Exit)."""
    while True:
        show_menu()
        choice = input("Enter your choice (0-7): ").strip()
        print()

        if choice == "1":
            student_id = get_non_empty_input("Enter student ID: ")
            name = get_non_empty_input("Enter student name: ")
            course = get_non_empty_input("Enter course: ")
            try:
                student = system.register_student(student_id, name, course)
                print(f"Success: student {student.student_id} registered.")
            except ValueError as error:
                print(f"Error: {error}")

        elif choice == "2":
            student_id = get_non_empty_input("Enter student ID: ")
            if system.find_student(student_id) is None:
                print(f"Error: no student found with ID '{student_id}'.")
                continue
            subject = get_subject_input()
            mark = get_mark_input("Enter mark (0-100): ")
            try:
                system.update_student_mark(student_id, subject, mark)
                print(f"Success: {subject} mark saved.")
            except ValueError as error:
                print(f"Error: {error}")

        elif choice == "3":
            system.display_all_students()

        elif choice == "4":
            student_id = get_non_empty_input("Enter student ID to search: ")
            student = system.find_student(student_id)
            if student is None:
                print(f"Error: no student found with ID '{student_id}'.")
            else:
                student.display_info()

        elif choice == "5":
            student_id = get_non_empty_input("Enter student ID: ")
            student = system.find_student(student_id)
            if student is None:
                print(f"Error: no student found with ID '{student_id}'.")
            else:
                average = student.calculate_average()
                if average is None:
                    print(f"{student.name} has no marks recorded yet.")
                else:
                    print(
                        f"{student.name}'s average mark is {average:.2f} "
                        f"(based on {student.count_recorded_marks()} of 3 subjects)."
                    )

        elif choice == "6":
            added = load_demo_data(system)
            print(f"{added} fictional demo student(s) added.")

        elif choice == "7":
            # Calling the class method using the class name.
            StudentRecordSystem.display_system_information()

        elif choice == "0":
            print("Thank you for using the system. Goodbye!")
            break

        else:
            print("Error: invalid choice. Please enter a number from 0 to 7.")


def main():
    """Program entry point."""
    system = StudentRecordSystem()  # Object creation
    try:
        run_menu(system)
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C or end of input: exit safely instead of crashing.
        print("\nProgram closed. Goodbye!")


# This check means the menu only starts when main.py is run directly,
# not when test_main.py imports it.
if __name__ == "__main__":
    main()
