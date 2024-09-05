# ------------------------------------------------------------------------------------------ #
# Title: Assignment06_Starter
# Desc: This assignment demonstrates using functions
# with structured error handling
# Change Log: (Who, When, What)
#   Eder Martins,9/4/2024,Created Script
#
# ------------------------------------------------------------------------------------------ #
import json

# Define the Data Constants
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
'''
# Define the Data Constants
FILE_NAME: str = "Enrollments.json"

# Define the Data Variables
menu_choice: str = ''  # Hold the choice made by the user
students: list = []  # A table to hold student data (list of dictionary rows)
student_first_name: str = ''  # Holds the student's first name
student_last_name: str = ''  # Holds the student's last name
course_name: str = ''  # Holds the course name
file_name: str = FILE_NAME  # The file name for storing data


class FileProcessor:
    """
    Class to process data to and from a file.

    This class provides static methods to read from and write data to a file in JSON format.
    It handles file operations such as opening, reading, writing, and closing the file,
    while performing error handling to ensure proper file management.

    Methods:
        read_data_from_file(file_name: str, student_data: list):
            Reads data from a specified file and loads it into the provided list.

        write_data_to_file(file_name: str, student_data: list):
            Writes the provided list of data to a specified file in JSON format.
    """

    @staticmethod
    def read_data_from_file(file_name: str, student_data: list):
        """
        Reads data from a file into a list of dictionaries.

        Args:
            file_name (str): The name of the file to read from.
            student_data (list): The list where the data will be stored.

        Returns:
            None
        """
        try:
            file = open(file_name, "r")
            student_data.clear()
            student_data.extend(json.load(file))
            file.close()
        except Exception as e:
            IO.output_error_messages("Error: There was a problem with reading the file.", e)
        finally:
            if file.closed is False:
                file.close()

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        """
        Writes data from a list of dictionaries to a file.

        Args:
            file_name (str): The name of the file to write to.
            student_data (list): The list of data to be written.

        Returns:
            None
        """
        try:
            file = open(file_name, "w")
            json.dump(student_data, file)
            file.close()
        except Exception as e:
            message = "Error: There was a problem with writing to the file.\n"
            message += "Please check that the file is not open by another program."
            IO.output_error_messages(message, e)
        finally:
            if file.closed is False:
                file.close()


class IO:
    """
    Class to handle input and output operations.

    This class provides static methods for interacting with the user,
    including displaying messages, collecting user input, and printing student data.
    It also handles error messaging for improved user feedback.

    Methods:
        output_error_messages(message: str, error: Exception = None):
            Outputs error messages and optional technical error details.

        output_menu(menu: str):
            Displays the menu of available options.

        input_menu_choice():
            Gets the user's choice from the menu.

        input_student_data(student_data: list):
            Prompts the user for student data (first name, last name, course) and appends it to the list.

        output_student_courses(student_data: list):
            Displays all student data in a formatted list.
    """

    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """
        Outputs error messages and optional technical error details.

        Args:
            message (str): The error message to display.
            error (Exception, optional): The exception to display additional details for.

        Returns:
            None
        """
        print(message)
        if error:
            print("-- Technical Error Message -- ")
            print(error.__doc__)
            print(error.__str__())

    @staticmethod
    def output_menu(menu: str):
        """
        Displays the menu of choices to the user.

        Args:
            menu (str): The menu string to display.

        Returns:
            None
        """
        print(menu)

    @staticmethod
    def input_menu_choice():
        """
        Gets the user's menu choice.

        Returns:
            str: The user's choice as a string.
        """
        return input("What would you like to do: ")

    @staticmethod
    def input_student_data(student_data: list):
        """
        Prompts the user to enter student data and stores it in a list.

        Args:
            student_data (list): The list to append the new student's data to.

        Returns:
            None
        """
        try:
            student_first_name = input("Enter the student's first name: ")
            if not student_first_name.isalpha():
                raise ValueError("The first name should only contain alphabetic characters.")
            student_last_name = input("Enter the student's last name: ")
            if not student_last_name.isalpha():
                raise ValueError("The last name should only contain alphabetic characters.")
            course_name = input("Please enter the name of the course: ")
            student = {"FirstName": student_first_name, "LastName": student_last_name, "CourseName": course_name}
            student_data.append(student)
            print(f"You have registered {student_first_name} {student_last_name} for {course_name}.")
        except ValueError as e:
            IO.output_error_messages(e.__str__(), e)
        except Exception as e:
            IO.output_error_messages("Error: There was a problem with your entered data.", e)

    @staticmethod
    def output_student_courses(student_data: list):
        """
        Displays all student data in a formatted manner.

        Args:
            student_data (list): The list of students' data to display.

        Returns:
            None
        """
        print("-" * 50)
        for student in student_data:
            print(f'Student {student["FirstName"]} '
                  f'{student["LastName"]} is enrolled in {student["CourseName"]}')
        print("-" * 50)


# Main Body of the Program
FileProcessor = FileProcessor()  # Instantiate the FileProcessor class
IO = IO()  # Instantiate the IO class

# When the program starts, read the file data into a list of lists (table)
FileProcessor.read_data_from_file(file_name, students)

while True:
    IO.output_menu(MENU)
    menu_choice = IO.input_menu_choice()

    if menu_choice == "1":
        IO.input_student_data(students)
    elif menu_choice == "2":
        IO.output_student_courses(students)
    elif menu_choice == "3":
        FileProcessor.write_data_to_file(file_name, students)
        print("The data below has been saved to the file.")
        FileProcessor.read_data_from_file(file_name, students)  # Read the saved data back into memory
        IO.output_student_courses(students)  # Display the saved data
    elif menu_choice == "4":
        print("Program Ended")
        break
    else:
        print("Please choose a valid option from the menu (1-4).")
