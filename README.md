# Student Record and Examination Results Management System

**Course** BICT
**Module:** PROG211 - Object-Oriented Programming Methods 1
**Institution:** Limkokwing University of Creative Technology, Sierra Leone
**Domain:** Education
**Language:** Python 3 (tested with Python 3.12.10)
**Student:** Daniel Michael Fofanah 
**ID** 905006072

---

## 1. Problem Statement

Many schools still keep student records and examination results on paper or in
scattered spreadsheets. This makes it slow to find a student, easy to make
mistakes when recording marks, and difficult to calculate averages correctly.

This project is a simple terminal program that stores student records and
examination marks in one place, checks that the data entered is valid, and
calculates each student's average mark.

## 2. Objectives

- Use Object-Oriented Programming (classes, objects, attributes and methods) to
  solve a real education problem.
- Store multiple student objects in **one primary data structure** (a list).
- Validate input so that wrong data (empty fields, duplicate IDs, marks outside
  0-100) is rejected.
- Follow Digital Public Goods (DPG) principles.

## 3. Features

1. Register a student with a unique student ID, name and course.
2. Record examination marks for Mathematics, English and Programming.
3. Update a student's marks.
4. Display all registered students.
5. Search for a student by ID.
6. Calculate and display a student's average mark (using recorded marks only).
7. Load fictional demonstration data.
8. Display information about the system.
9. Exit the program safely (including Ctrl+C).

## 4. OOP Concepts Used

### Classes and objects

| Class | Purpose |
|---|---|
| `Student` | Represents **one** student and their three marks. |
| `StudentRecordSystem` | Manages **many** `Student` objects stored in one list. |

Objects are created with `StudentRecordSystem()` and inside
`register_student()`, which creates a new `Student(...)` object.

### Attributes

- `Student`: `student_id`, `name`, `course`, `mathematics_mark`,
  `english_mark`, `programming_mark`.
  A mark that has not been recorded is stored as `None` (not `0`), so it is
  never counted in the average.
- `StudentRecordSystem`: `students` (the list), plus class-level information
  `SYSTEM_NAME`, `VERSION`, `SUBJECTS_TEXT` and `DATA_NOTICE`.

### Constructors

Both classes have an `__init__` method. The `Student` constructor also checks
that the ID, name and course are not empty.

### Instance methods (use `self`)

| Method | Class | What it does |
|---|---|---|
| `update_mark(subject, mark)` | Student | Validates and saves one mark. |
| `count_recorded_marks()` | Student | Counts how many marks are recorded. |
| `calculate_average()` | Student | Averages recorded marks only; returns `None` if none. |
| `display_info()` | Student | Prints the student's details and results. |
| `register_student(id, name, course)` | StudentRecordSystem | Adds a new student to the list (rejects duplicates). |
| `find_student(id)` | StudentRecordSystem | Searches the list by ID. |
| `display_all_students()` | StudentRecordSystem | Displays every student in the list. |
| `update_student_mark(id, subject, mark)` | StudentRecordSystem | Finds a student and updates a mark. |

### Class method (uses `cls`)

```python
@classmethod
def display_system_information(cls):
    print(f"System   : {cls.SYSTEM_NAME}")
    print(f"Version  : {cls.VERSION}")
    ...
```

- An **instance method** receives `self`, which is **one particular object**,
  and works with that object's own data (for example, one student's marks).
- A **class method** receives `cls`, which is **the class itself**, and works
  with information shared by the whole class. It can be called without creating
  an object: `StudentRecordSystem.display_system_information()`.

System information (name, version, subjects) belongs to the whole system, not
to one student list, so a class method is the right choice.

### Interaction between objects

- `StudentRecordSystem.register_student()` **creates** `Student` objects.
- `StudentRecordSystem.display_all_students()` asks **each** `Student` object to
  run its own `display_info()` method.
- `StudentRecordSystem.update_student_mark()` calls the `Student` object's
  `update_mark()` method.

### Data structure

The program uses **exactly one primary data structure**: the list
`self.students`, which holds all `Student` objects. Marks are stored as three
separate attributes, so no second list or dictionary is needed.

- **Add records:** `register_student()` uses `self.students.append(...)`.
- **Display records:** `display_all_students()` loops over `self.students`.
- **Search records:** `find_student()` loops over `self.students`.

## 5. Installation

1. Install Python 3.8 or newer from <https://www.python.org/downloads/>.
2. Download or clone this repository:
   ```
   git clone <repository-url>
   cd <repository-folder>
   ```
3. No extra packages are needed. The program uses only the Python standard
   library.

## 6. Usage

Run the program:

```
python main.py
```

Choose an option by typing its number and pressing **Enter**:

```
1. Register a new student
2. Record or update an exam mark
3. Display all students
4. Search for a student by ID
5. Show a student's average mark
6. Load fictional demo data
7. Display system information
0. Exit
```

Tip: choose **6** first to load fictional students for a quick demonstration.

## 7. Example Input / Output

The examples below were copied from a real run of the program.

**Option 7 - Display system information (class method):**

```
System   : Student Record and Examination Results Management System
Version  : 1.0
Class    : StudentRecordSystem
Subjects : Mathematics, English, Programming
Marks    : 0 to 100
Privacy  : Uses fictional demonstration data only. Nothing is saved to disk.
```

**Option 6 then Option 3 - Load demo data and display all students:**

```
3 fictional demo student(s) added.

Total students: 3
---------------------------------------------
Student ID  : LUCT001
Name        : Aminata Example
Course      : BSc Software Engineering
Mathematics : 78
English     : 65
Programming : 90
Average     : 77.67 (based on 3 of 3 subjects)
---------------------------------------------
Student ID  : LUCT002
Name        : Mohamed Sample
Course      : BSc Information Technology
Mathematics : 55
English     : 70
Programming : Not recorded
Average     : 62.50 (based on 2 of 3 subjects)
---------------------------------------------
Student ID  : LUCT003
Name        : Isatu Demo
Course      : Diploma in Business IT
Mathematics : Not recorded
English     : Not recorded
Programming : Not recorded
Average     : No marks recorded yet
---------------------------------------------
```

**Option 1 - Register a student (with an empty name rejected, then a duplicate ID rejected):**

```
Enter student ID: LUCT004
Enter student name:
Error: this field cannot be empty. Please try again.
Enter student name: Fatu Fictional
Enter course: BSc Computing
Success: student LUCT004 registered.

Enter student ID: luct004
Enter student name: Dup Name
Enter course: Course
Error: Student ID 'LUCT004' is already registered.
```

**Option 2 - Record a mark (invalid subject and invalid marks rejected):**

```
Enter student ID: LUCT004
Subjects: 1. Mathematics  2. English  3. Programming
Choose a subject (1-3): 5
Error: invalid subject. Please enter 1, 2 or 3.
Choose a subject (1-3): 3
Enter mark (0-100): abc
Error: please enter a number, for example 75.
Enter mark (0-100): 150
Error: mark must be between 0 and 100.
Enter mark (0-100): 82
Success: programming mark saved.
```

**Option 5 and Option 4 - Average and unknown ID:**

```
Enter student ID: LUCT004
Fatu Fictional's average mark is 82.00 (based on 1 of 3 subjects).

Enter student ID to search: NOPE
Error: no student found with ID 'NOPE'.
```

> All names above are **fictional** and do not represent real people.

## 8. Testing

Automated tests use Python's built-in `unittest` framework (no installation
needed). Run:

```
python -m unittest -v test_main
```

The 26 tests check:

- Creating students and registering them in the list.
- Rejecting empty ID, name or course, and duplicate student IDs (case-insensitive).
- Finding a student and returning `None` for an unknown ID.
- Accepting valid marks, including the boundary values 0 and 100.
- Rejecting invalid marks (-1, 101, 100.5, text, `None`, `True`) and invalid subjects.
- Keeping the old mark when an update is rejected.
- Averages with three marks, two marks (missing mark not counted as zero),
  a real mark of 0, and no marks.
- Calling the class method without an object, and proving it uses `cls`.
- Loading demo data without creating duplicates.

## 9. Digital Public Goods (DPG) Alignment

| DPG principle | How this project supports it |
|---|---|
| **Open source** | Released under the MIT Licence (see `LICENSE`). Anyone can use, study, change and share the code. The source is hosted on GitHub. |
| **Inclusive and accessible design** | Plain-text terminal menu that works on any computer with Python, no internet, mouse or colour needed. Uses simple numbered options and clear error messages that say what went wrong and how to fix it. Works with screen readers that read terminal text. |
| **Privacy protection** | Uses fictional demonstration data only. Collects only the minimum data needed (ID, name, course, marks). Nothing is saved to disk or sent over a network, so all data is cleared when the program closes. |
| **Modular and reusable code** | Logic is separated into classes (`Student`, `StudentRecordSystem`) and small functions with clear responsibilities. The classes can be imported into other programs (`from main import StudentRecordSystem`) without starting the menu. Uses only the standard library. |

## 10. Limitations

- Data is stored in memory only and is lost when the program closes.
- Only three fixed subjects are supported.
- Students cannot be deleted or renamed after registration.
- There is no login system (not required for this demonstration).
- Terminal interface only; there is no graphical interface.

## 11. Future Improvements

- Save and load records from a file (for example CSV).
- Allow deleting and editing student details.
- Add grade letters (A, B, C...) and class rankings.

## 12. Project Structure

```
OOP1/
├── main.py         # Student and StudentRecordSystem classes + menu
├── test_main.py    # unittest test suite
├── README.md       # This document
├── LICENSE         # MIT Licence
├── .gitignore      # Files Git should ignore
└── screenshots/    # Screenshots of program execution
```

## 13. Licence

This project is licensed under the MIT Licence. See [LICENSE](LICENSE).
