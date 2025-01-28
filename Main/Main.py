# This Work done by group: 4th Group
# Delfin B. Simbulan, 2024-02727-MN-0, 
# James Pol Quimen
# Christanne Tedd Revidad
# Jeru Antonio

import csv
import datetime
import os
import time

def startFeature():
    def validate_student_id(student_id, valid_ids):
        """Validate the student ID."""
        while student_id not in valid_ids:
            student_id = input("Invalid ID. Please enter a valid student ID: ")
        return student_id

    def get_student_level_selection():
        """Get the level selection from the user."""
        level = input("Select student level: Undergraduate (U), Graduate (G), or Both (B): ").upper()
        while level not in ['U', 'G', 'B']:
            level = input("Invalid selection. Please select U, G, or B: ").upper()

        if level == 'G' or level == 'B':
            degree = input("Select degree: Master (M), Doctorate (D), or Both (B): ").upper()
            while degree not in ['M', 'D', 'B']:
                degree = input("Invalid selection. Please select M, D, or B: ").upper()

            if level == 'G':
                if degree == 'M':
                    return ['GM']
                elif degree == 'D':
                    return ['GD']
                elif degree == 'B':
                    return ['GM', 'GD']

            if level == 'B':
                levels = ['U']
                if degree == 'M':
                    levels.append('GM')
                elif degree == 'D':
                    levels.append('GD')
                elif degree == 'B':
                    levels.extend(['GM', 'GD'])
                return levels

        return [level]

    def load_student_details(file_path):
        """Load student details from a specific student ID file."""
        student_details = []
        if not os.path.exists(file_path):
            print(f"Error: File {file_path} does not exist.")
            return student_details

        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                student_details.append(row)
        return student_details

    def main():
        # Load the data from the main CSV file
        student_details_file = 'studentDetails.csv'
        student_details = load_student_details(student_details_file)

        # Extract valid student IDs
        valid_ids = {row['stdID'] for row in student_details}

        # Get user inputs
        level = get_student_level_selection()
        print(f"Selected level: {level}")  # Debugging: Print selected level

        student_id = input("Enter the student ID: ").strip()
        student_id = validate_student_id(student_id, valid_ids)

        # Load the specific student file
        student_file = f"{student_id}.csv"
        student_data = load_student_details(student_file)

        if not student_data:
            print(f"No enrollment data found for student {student_id}.")
            return

        # Validate level and degree
        is_enrolled = False

        if 'U' in level:
            if any(row['Level'].strip().upper() == 'U' for row in student_data):
                print(f"Student {student_id} is enrolled in Undergraduate level.")
                is_enrolled = True
            else:
                print(f"Student {student_id} is not enrolled in Undergraduate level.")
                is_enrolled = False
                time.sleep(3)
                os.system('cls')
                startFeature()

        if 'GM' in level or 'GD' in level:
            # Filter student data for Graduate level
            graduate_data = [row for row in student_data if row['Level'].strip().upper() == 'G']
            valid_degrees = {row['Degree'].strip().upper() for row in graduate_data}

            # Adjusted checks for GM and GD based on actual degree names
            gm_enrolled = 'GM' in level and any(degree.startswith('M') for degree in valid_degrees)
            gd_enrolled = 'GD' in level and any(degree.startswith('D') for degree in valid_degrees)

            if gm_enrolled:
                print(f"Student {student_id} is enrolled in a Master's program.")
                is_enrolled = True

            if gd_enrolled:
                print(f"Student {student_id} is enrolled in a Doctorate program.")
                is_enrolled = True

            if 'GM' in level and 'GD' in level:
                if gm_enrolled and gd_enrolled:
                    print(f"Student {student_id} is enrolled in both Master's and Doctorate programs.")
                    is_enrolled = True

            if not (gm_enrolled or gd_enrolled):
                print(f"Student {student_id} is not enrolled in the selected Graduate levels.")
                os.system('cls')
                startFeature()


        if is_enrolled:
            print("Validation successful. Redirecting to menu page...\n\n")
            time.sleep (3)
            menuFeature(level, student_id)
        else:
            print("The student is not enrolled in any selected levels or degrees.")

    if __name__ == "__main__":
        main()

def menuFeature(degree, student_id):
    
    #stores the student ID and level
    stdID = int(student_id)
    level = degree

    # Lists to hold the request data
    request_history = []
    dates = []
    times = []

    # Get current time for timestamp
    now = datetime.datetime.now()

    # Format time in 12-hour format with AM/PM
    formatted_time = now.strftime("%I:%M %p")
    


    confirm = True
    while confirm:
        print("Student Transcript Generation System")
        print("======================================")
        print("1. Student Details")
        print("2. Statistics")
        print("3. Transcript based on Major Courses")
        print("4. Transcript based on Minor Courses")
        print("5. Full Transcript")
        print("6. Previous Transcript Requests")
        print("7. Select Another Student")
        print("8. Terminate the System")
        print("======================================")
        try:
            option = int(input("Enter Your Feature: "))
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 8.")
            continue

        if 1 <= option <= 8:
            if option == 1:
                detailsFeature(level, stdID)
            elif option == 2:
                statisticsFeature(level, stdID)
                request_history.append("Statistics")
                dates.append(str(now.date()))
                times.append(formatted_time)
            elif option == 3:
                MajorTranscript(level, stdID)
                request_history.append("Major")
                dates.append(str(now.date()))
                times.append(formatted_time) 
            elif option == 4:
                MinorTranscript(level, stdID)
                request_history.append("Minor")
                dates.append(str(now.date()))
                times.append(formatted_time) 
            elif option == 5:
                FullTranscript(level, stdID)
                request_history.append("Full")
                dates.append(str(now.date()))
                times.append(formatted_time)    
            elif option == 6:
                previousRequestsFeature(request_history, dates, times, stdID) 
            elif option == 7:
                newStudentFeature()
            elif option == 8:
                terminateFeature(request_history)
                confirm = False
        else:
            print("Invalid option. Please try again.")
            continue

def detailsFeature(level, student_id):
    # Open and read the CSV file
    with open('studentDetails.csv', mode='r') as file:
        reader = csv.DictReader(file)

        # Initialize a flag to check if student details are found
        details_found = False

        # Map levels to their full descriptions
        level_descriptions = {
            'U': "Undergraduate",
            'GM': "Graduate - Masters",
            'GD': "Graduate - Doctorate"
        }

        # Initialize containers for details
        terms_display = {}
        colleges_display = set()
        departments_display = set()

        # Collect all rows matching the student ID
        matching_rows = []
        for row in reader:
            if row['stdID'] == str(student_id):
                matching_rows.append(row)

        # Process the matching rows
        for row in matching_rows:
            details_found = True

            # Extract details for the corresponding levels
            for l in level:
                if l == 'U' and row['Level'] == 'U':
                    terms_display['Undergraduate'] = f"Undergraduate: {row['Terms']} term(s)"
                    colleges_display.add(row['College'])
                    departments_display.add(row['Department'])
                elif l == 'GM' and row['Degree'] == 'M1':
                    terms_display['Graduate - Masters'] = f"Graduate - Masters: {row['Terms']} term(s)"
                    colleges_display.add(row['College'])
                    departments_display.add(row['Department'])
                elif l == 'GD' and row['Degree'] == 'D1':
                    terms_display['Graduate - Doctorate'] = f"Graduate - Doctorate: {row['Terms']} term(s)"
                    colleges_display.add(row['College'])
                    departments_display.add(row['Department'])

        # If details are found, prepare the output
        if details_found:
            # Generate the description for the selected levels
            level_display = ", ".join([level_descriptions[l] for l in level if l in level_descriptions])

            # Prepare the details in the required format
            student_details = (
                f"Name: {matching_rows[0]['Name']}, "
                f"\nStudent ID: {matching_rows[0]['stdID']}, "
                f"\nLevels: {level_display}, "
                f"\nTerms: {', '.join(terms_display.values())}, "
                f"\nCollege(s): {', '.join(colleges_display)}, "
                f"\nDepartment(s): {', '.join(departments_display)}"
            )

            # Print to console
            print(student_details)

            # Create the file name based on student ID
            file_name = f"{student_id}_StudentDetails.txt"

            # Write the details to the text file
            with open(file_name, "w") as txt_file:
                txt_file.write(student_details)

            print(f"\nStudent details have been saved to {file_name}.")

            # Wait for a few seconds before clearing the screen
            time.sleep(10)

            # Clear the console (works differently depending on the OS)
            os.system('cls' if os.name == 'nt' else 'clear')

            # Redirect to the menu
            print("Redirecting to the menu...")
            time.sleep(2)  # Pause briefly before redirecting

        # If no details match the student ID or level
        else:
            print("Student ID not found or no matching level details.")
            time.sleep(2)

def statisticsFeature(levels, student_ID):
    """
    Generates a statistical summary for a student's academic performance.
    Combines major and minor details with overall, term, and specific statistics.
    Saves the output to a text file.
    """
    stdID = str(student_ID)  # Ensure student_ID is treated as a string

    def load_csv(filepath):
        """Load CSV file into a list of dictionaries."""
        data = []
        try:
            with open(filepath, 'r') as file:
                headers = file.readline().strip().split(',')
                for line in file:
                    values = line.strip().split(',')
                    data.append(dict(zip(headers, values)))
        except FileNotFoundError:
            print(f"Error: File {filepath} not found.")
        except Exception as e:
            print(f"Error while reading file {filepath}: {e}")
        return data

    def calculate_averages(courses):
        """Calculate total credits and weighted averages for a list of courses."""
        total_credits = sum(int(course['creditHours']) for course in courses)
        weighted_sum = sum(int(course['Grade']) * int(course['creditHours']) for course in courses)
        average = weighted_sum / total_credits if total_credits > 0 else 0
        return total_credits, average

    def generate_statistics(stdID, student_details_path, student_courses_path, levels):
        """Generates the statistics and saves it to a text file."""
        student_details = load_csv(student_details_path)
        student_courses = load_csv(student_courses_path)

        # Get student details
        student_info = next((student for student in student_details if student['stdID'] == stdID), None)
        if not student_info:
            print(f"No details found for student ID: {stdID}")
            return

        if isinstance(levels, str):
            levels = [levels]

        statistics_data = {}
        level_names = {'U': 'Undergraduate', 'GM': 'Graduate - Masters', 'GD': 'Graduate - Doctoral'}

        for level in levels:
            level_courses = []
            if level == 'GM':
                level_courses = [course for course in student_courses if course['Level'] == 'G' and course['Degree'] == 'M1']
            elif level == 'GD':
                level_courses = [course for course in student_courses if course['Level'] == 'G' and course['Degree'] == 'D1']
            elif level == 'U':
                level_courses = [course for course in student_courses if course['Level'] == 'U']

            all_terms = sorted(set(course['Term'] for course in level_courses))
            term_averages = []
            max_grades = []
            min_grades = []
            repeated_courses = set()
            all_grades = []

            for term in all_terms:
                term_courses = [course for course in level_courses if course['Term'] == term]
                major_courses = [course for course in term_courses if course['courseType'] == 'Major']
                minor_courses = [course for course in term_courses if course['courseType'] == 'Minor']

                _, term_avg_major = calculate_averages(major_courses)
                _, term_avg_minor = calculate_averages(minor_courses)

                total_credits = sum(int(course['creditHours']) for course in term_courses)
                weighted_sum = sum(int(course['Grade']) * int(course['creditHours']) for course in term_courses)
                term_avg = weighted_sum / total_credits if total_credits > 0 else 0
                term_averages.append((term, term_avg))

                max_grade = max(term_courses, key=lambda x: int(x['Grade']))
                min_grade = min(term_courses, key=lambda x: int(x['Grade']))

                max_grades.append((term, max_grade['courseID'], max_grade['Grade']))
                min_grades.append((term, min_grade['courseID'], min_grade['Grade']))

                all_grades.extend([int(course['Grade']) for course in term_courses])

                course_ids = [course['courseID'] for course in term_courses]
                repeated_courses.update([cid for cid in course_ids if course_ids.count(cid) > 1])

            overall_avg = sum(all_grades) / len(all_grades) if all_grades else 0

            statistics_data[level] = {
                "term_averages": term_averages,
                "max_grades": max_grades,
                "min_grades": min_grades,
                "repeated_courses": repeated_courses,
                "overall_avg": overall_avg
            }

        statistics_lines = []
        for level, data in statistics_data.items():
            statistics_lines.append(f"\n{'*' * 10} {level_names.get(level, level)} Level {'*' * 10}\n")
            statistics_lines.append(f"Overall average (major and minor) for all terms: {data['overall_avg']:.2f}\n")

            for term, avg in data['term_averages']:
                statistics_lines.append(f"Average (major and minor) of Term {term}: {avg:.2f}")

            for term, course_id, grade in data['max_grades']:
                statistics_lines.append(f"\nMaximum grade: {grade} in Term {term} (Course: {course_id})")

            for term, course_id, grade in data['min_grades']:
                statistics_lines.append(f"Minimum grade: {grade} in Term {term} (Course: {course_id})")

            if data['repeated_courses']:
                statistics_lines.append(f"\nRepeated courses: {', '.join(data['repeated_courses'])}")
            else:
                statistics_lines.append("No repeated courses.")

        output_filename = f"{stdID}_Statistics.txt"
        with open(output_filename, "w") as file:
            file.write("\n".join(statistics_lines))

        print("\n".join(statistics_lines))
        print(f"\n\nStatistics saved to {output_filename}")

    student_details_path = "studentDetails.csv"
    student_courses_path = f"{stdID}.csv"
    generate_statistics(stdID, student_details_path, student_courses_path, levels)

    #Pause for a few seconds
    time.sleep(10)

    #clears the screen and redirects to menu
    os.system('cls')
    print("Redirecting to main menu...")
    time.sleep(2) #waits a few seconds
    os.system('cls') #clears again before returning back to main menu

def MajorTranscript(levels, student_ID):
    """
    Generates the transcript for a student's major subjects based on specified levels.
    Levels can be a single value or a list of values (e.g., ['U', 'GM', 'GD']).
    """
    stdID = str(student_ID)  # Ensure student_ID is treated as a string

    def load_csv(filepath):
        """Load CSV file into a list of dictionaries."""
        data = []
        try:
            with open(filepath, 'r') as file:
                headers = file.readline().strip().split(',')
                for line in file:
                    values = line.strip().split(',')
                    data.append(dict(zip(headers, values)))
        except FileNotFoundError:
            print(f"Error: File {filepath} not found.")
        except Exception as e:
            print(f"Error while reading file {filepath}: {e}")
        return data

    def get_number_of_terms(student_details, level):
        """Retrieve the number of terms based on the level."""
        if level == 'U':
            student_info = next((row for row in student_details if row['Level'] == 'U'), None)
        elif level == 'GM':
            student_info = next((row for row in student_details if row['Degree'] == 'M1'), None)
        elif level == 'GD':
            student_info = next((row for row in student_details if row['Degree'] == 'D1'), None)
        else:
            student_info = None

        return int(student_info['Terms']) if student_info and 'Terms' in student_info else 0

    def generate_transcript(stdID, student_details_path, student_courses_path, levels, course_type):
        """Generates the transcript for a student's subjects and saves it to a text file."""
        student_details = load_csv(student_details_path)
        student_courses = load_csv(student_courses_path)

        # Get student details
        student_info = next((student for student in student_details if student['stdID'] == stdID), None)
        if not student_info:
            print(f"No details found for student ID: {stdID}")
            return

        if isinstance(levels, str):
            levels = [levels]

        transcript_data = {}
        for level in levels:
            level_courses = []
            if level == 'GM':
                level_courses = [course for course in student_courses if course['courseType'] == course_type and course['Level'] == 'G' and course.get('Degree') == 'M1']
            elif level == 'GD':
                level_courses = [course for course in student_courses if course['courseType'] == course_type and course['Level'] == 'G' and course.get('Degree') == 'D1']
            elif level == 'U':
                level_courses = [course for course in student_courses if course['courseType'] == course_type and course['Level'] == 'U']

            all_terms = sorted(set(course['Term'] for course in level_courses))

            level_data = {}
            for term in all_terms:
                term_courses = [course for course in level_courses if course['Term'] == term]
                if term_courses:
                    total_credits = sum(int(course['creditHours']) for course in term_courses)
                    term_avg = sum(int(course['Grade']) * int(course['creditHours']) for course in term_courses) / total_credits
                else:
                    term_avg = None
                level_data[term] = {"courses": term_courses, "term_avg": term_avg}

            total_credit_hours = sum(int(course['creditHours']) for course in level_courses)
            overall_avg = sum(int(course['Grade']) * int(course['creditHours']) for course in level_courses) / total_credit_hours if total_credit_hours > 0 else 0

            number_of_terms = get_number_of_terms(student_details, level)

            transcript_data[level] = {
                "terms": level_data,
                "overall_avg": overall_avg,
                "student_info": {
                    "Name": student_info['Name'],
                    "stdID": student_info['stdID'],
                    "College": student_info['College'],
                    "Department": student_info['Department'],
                    "Major": student_info['Major'],
                    "Minor": student_info.get('Minor', 'N/A'),
                    "Number of terms": number_of_terms
                }
            }

        level_names = {'U': 'Undergraduate', 'GM': 'Graduate - Masters', 'GD': 'Graduate - Doctoral'}
        transcript_lines = []

        for level, data in transcript_data.items():
            student_info = data['student_info']
            transcript_lines.append(f"\nName: {student_info['Name']}\tstdID: {student_info['stdID']}")
            transcript_lines.append(f"College: {student_info['College']}\t\tDepartment: {student_info['Department']}")
            transcript_lines.append(f"Major: {student_info['Major']}\t\tMinor: {student_info['Minor']}")
            transcript_lines.append(f"Number of terms: {student_info['Number of terms']}")
            transcript_lines.append(f"\n{'=' * 40}\nLevel: {level_names.get(level, level)}\n{'=' * 40}")

            for term in data['terms']:
                term_data = data['terms'][term]
                transcript_lines.append(f"\n{'*' * 10} Term {term} {'*' * 10}")
                if term_data.get('courses'):
                    transcript_lines.append(f"{'course ID':<10} {'course name':<15} {'credit hours':<15} {'grade':<10}")
                    transcript_lines.append("-" * 40)
                    for course in term_data['courses']:
                        transcript_lines.append(
                            f"{course['courseID']:<10} {course['courseName']:<15} {course['creditHours']:<15} {course['Grade']:<10}"
                        )
                    transcript_lines.append(f"{course_type} Average = {term_data['term_avg']:.2f}")
                else:
                    transcript_lines.append(f"No {course_type.lower()} subjects for this term.")

            transcript_lines.append(f"Overall {course_type} Average = {data['overall_avg']:.2f}")
            transcript_lines.append(f"\n{'*' * 10} End of Transcript ({level_names.get(level, level)}) {'*' * 10}\n\n")

        output_filename = f"{stdID}_{course_type}Transcript.txt"
        with open(output_filename, "w") as file:
            file.write("\n".join(transcript_lines))

        print("\n".join(transcript_lines))
        print(f"Transcript saved to {output_filename}")

    student_details_path = "studentDetails.csv"
    student_courses_path = f"{stdID}.csv"
    generate_transcript(stdID, student_details_path, student_courses_path, levels, "Major")

    #Pause for a few seconds
    time.sleep(10)

    #clears the screen and redirects to menu
    os.system('cls')
    print("Redirecting to main menu...")
    time.sleep(2) #waits a few seconds
    os.system('cls') #clears again before returning back to main menu

def MinorTranscript(levels, student_ID):
    """
    Generates the transcript for a student's minor subjects based on specified levels.
    """
    stdID = str(student_ID)  # Ensure student_ID is treated as a string

    def load_csv(filepath):
        """Load CSV file into a list of dictionaries."""
        data = []
        try:
            with open(filepath, 'r') as file:
                headers = file.readline().strip().split(',')
                for line in file:
                    values = line.strip().split(',')
                    data.append(dict(zip(headers, values)))
        except FileNotFoundError:
            print(f"Error: File {filepath} not found.")
        except Exception as e:
            print(f"Error while reading file {filepath}: {e}")
        return data

    def get_number_of_terms(student_details, level):
        """Retrieve the number of terms based on the level."""
        if level == 'U':
            student_info = next((row for row in student_details if row['Level'] == 'U'), None)
        elif level == 'GM':
            student_info = next((row for row in student_details if row['Degree'] == 'M1'), None)
        elif level == 'GD':
            student_info = next((row for row in student_details if row['Degree'] == 'D1'), None)
        else:
            student_info = None

        return int(student_info['Terms']) if student_info and 'Terms' in student_info else 0

    def generate_transcript(stdID, student_details_path, student_courses_path, levels, course_type):
        """Generates the transcript for a student's subjects and saves it to a text file."""
        student_details = load_csv(student_details_path)
        student_courses = load_csv(student_courses_path)

        # Get student details
        student_info = next((student for student in student_details if student['stdID'] == stdID), None)
        if not student_info:
            print(f"No details found for student ID: {stdID}")
            return

        if isinstance(levels, str):
            levels = [levels]

        transcript_data = {}
        for level in levels:
            level_courses = []
            if level == 'GM':
                level_courses = [course for course in student_courses if course['courseType'] == course_type and course['Level'] == 'G' and course.get('Degree') == 'M1']
            elif level == 'GD':
                level_courses = [course for course in student_courses if course['courseType'] == course_type and course['Level'] == 'G' and course.get('Degree') == 'D1']
            elif level == 'U':
                level_courses = [course for course in student_courses if course['courseType'] == course_type and course['Level'] == 'U']

            all_terms = sorted(set(course['Term'] for course in level_courses))

            level_data = {}
            for term in all_terms:
                term_courses = [course for course in level_courses if course['Term'] == term]
                if term_courses:
                    total_credits = sum(int(course['creditHours']) for course in term_courses)
                    term_avg = sum(int(course['Grade']) * int(course['creditHours']) for course in term_courses) / total_credits
                else:
                    term_avg = None
                level_data[term] = {"courses": term_courses, "term_avg": term_avg}

            total_credit_hours = sum(int(course['creditHours']) for course in level_courses)
            overall_avg = sum(int(course['Grade']) * int(course['creditHours']) for course in level_courses) / total_credit_hours if total_credit_hours > 0 else 0

            number_of_terms = get_number_of_terms(student_details, level)

            transcript_data[level] = {
                "terms": level_data,
                "overall_avg": overall_avg,
                "student_info": {
                    "Name": student_info['Name'],
                    "stdID": student_info['stdID'],
                    "College": student_info['College'],
                    "Department": student_info['Department'],
                    "Major": student_info['Major'],
                    "Minor": student_info.get('Minor', 'N/A'),
                    "Number of terms": number_of_terms
                }
            }

        level_names = {'U': 'Undergraduate', 'GM': 'Graduate - Masters', 'GD': 'Graduate - Doctoral'}
        transcript_lines = []

        for level, data in transcript_data.items():
            student_info = data['student_info']
            transcript_lines.append(f"\nName: {student_info['Name']}\tstdID: {student_info['stdID']}")
            transcript_lines.append(f"College: {student_info['College']}\t\tDepartment: {student_info['Department']}")
            transcript_lines.append(f"Major: {student_info['Major']}\t\tMinor: {student_info['Minor']}")
            transcript_lines.append(f"Number of terms: {student_info['Number of terms']}")
            transcript_lines.append(f"\n{'=' * 40}\nLevel: {level_names.get(level, level)}\n{'=' * 40}")

            for term in data['terms']:
                term_data = data['terms'][term]
                transcript_lines.append(f"\n{'*' * 10} Term {term} {'*' * 10}")
                if term_data.get('courses'):
                    transcript_lines.append(f"{'course ID':<10} {'course name':<15} {'credit hours':<15} {'grade':<10}")
                    transcript_lines.append("-" * 40)
                    for course in term_data['courses']:
                        transcript_lines.append(
                            f"{course['courseID']:<10} {course['courseName']:<15} {course['creditHours']:<15} {course['Grade']:<10}"
                        )
                    transcript_lines.append(f"{course_type} Average = {term_data['term_avg']:.2f}")
                else:
                    transcript_lines.append(f"No {course_type.lower()} subjects for this term.")

            transcript_lines.append(f"Overall {course_type} Average = {data['overall_avg']:.2f}")
            transcript_lines.append(f"\n{'*' * 10} End of Transcript ({level_names.get(level, level)}) {'*' * 10}\n\n")

        output_filename = f"{stdID}_{course_type}Transcript.txt"
        with open(output_filename, "w") as file:
            file.write("\n".join(transcript_lines))

        print("\n".join(transcript_lines))
        print(f"Transcript saved to {output_filename}")

    student_details_path = "studentDetails.csv"
    student_courses_path = f"{stdID}.csv"
    generate_transcript(stdID, student_details_path, student_courses_path, levels, "Minor")

    #Pause for a few seconds
    time.sleep(10)

    #clears the screen and redirects to menu
    os.system('cls')
    print("Redirecting to main menu...")
    time.sleep(2) #waits a few seconds
    os.system('cls') #clears again before returning back to main menu

def FullTranscript(levels, student_ID):
    """
    Generates the full transcript for a student, combining major and minor subjects.
    Includes term averages and overall averages for both major and minor subjects.
    """
    stdID = str(student_ID)  # Ensure student_ID is treated as a string

    def load_csv(filepath):
        """Load CSV file into a list of dictionaries."""
        data = []
        try:
            with open(filepath, 'r') as file:
                headers = file.readline().strip().split(',')
                for line in file:
                    values = line.strip().split(',')
                    data.append(dict(zip(headers, values)))
        except FileNotFoundError:
            print(f"Error: File {filepath} not found.")
        except Exception as e:
            print(f"Error while reading file {filepath}: {e}")
        return data

    def calculate_averages(courses):
        """Calculate total credits and weighted averages for a list of courses."""
        total_credits = sum(int(course['creditHours']) for course in courses)
        weighted_sum = sum(int(course['Grade']) * int(course['creditHours']) for course in courses)
        average = weighted_sum / total_credits if total_credits > 0 else 0
        return total_credits, average

    def generate_full_transcript(stdID, student_details_path, student_courses_path, levels):
        """Generates the full transcript and saves it to a text file."""
        student_details = load_csv(student_details_path)
        student_courses = load_csv(student_courses_path)

        # Get student details
        student_info = next((student for student in student_details if student['stdID'] == stdID), None)
        if not student_info:
            print(f"No details found for student ID: {stdID}")
            return

        if isinstance(levels, str):
            levels = [levels]

        transcript_data = {}
        level_names = {'U': 'Undergraduate', 'GM': 'Graduate - Masters', 'GD': 'Graduate - Doctoral'}

        for level in levels:
            level_courses = []
            if level == 'GM':
                level_courses = [course for course in student_courses if course['Level'] == 'G' and course['Degree'] == 'M1']
            elif level == 'GD':
                level_courses = [course for course in student_courses if course['Level'] == 'G' and course['Degree'] == 'D1']
            elif level == 'U':
                level_courses = [course for course in student_courses if course['Level'] == 'U']

            all_terms = sorted(set(course['Term'] for course in level_courses))
            level_data = {}

            for term in all_terms:
                term_courses = [course for course in level_courses if course['Term'] == term]
                major_courses = [course for course in term_courses if course['courseType'] == 'Major']
                minor_courses = [course for course in term_courses if course['courseType'] == 'Minor']

                total_credits_major, term_avg_major = calculate_averages(major_courses)
                total_credits_minor, term_avg_minor = calculate_averages(minor_courses)

                total_credits = total_credits_major + total_credits_minor
                weighted_sum = (term_avg_major * total_credits_major) + (term_avg_minor * total_credits_minor)
                term_avg = weighted_sum / total_credits if total_credits > 0 else 0

                level_data[term] = {
                    "major_courses": major_courses,
                    "minor_courses": minor_courses,
                    "term_avg_major": term_avg_major,
                    "term_avg_minor": term_avg_minor,
                    "term_avg": term_avg
                }

            total_credit_hours, overall_avg = calculate_averages(level_courses)

            # Retrieve the number of terms for GM and GD levels
            num_terms = 0
            if level == 'U':
                num_terms = int(student_info['Terms'])
            elif level == 'GM':
                num_terms = int(next((row['Terms'] for row in student_details if row['stdID'] == stdID and row['Degree'] == 'M1'), 0))
            elif level == 'GD':
                num_terms = int(next((row['Terms'] for row in student_details if row['stdID'] == stdID and row['Degree'] == 'D1'), 0))

            transcript_data[level] = {
                "terms": level_data,
                "overall_avg": overall_avg,
                "student_info": {
                    "Name": student_info['Name'],
                    "stdID": student_info['stdID'],
                    "College": student_info['College'],
                    "Department": student_info['Department'],
                    "Major": student_info['Major'],
                    "Minor": student_info.get('Minor', 'N/A'),
                    "Number of terms": num_terms
                }
            }

        transcript_lines = []
        for level, data in transcript_data.items():
            student_info = data['student_info']
            transcript_lines.append(f"\nName: {student_info['Name']}\tstdID: {student_info['stdID']}")
            transcript_lines.append(f"College: {student_info['College']}\t\tDepartment: {student_info['Department']}")
            transcript_lines.append(f"Major: {student_info['Major']}\t\tMinor: {student_info['Minor']}")
            transcript_lines.append(f"Number of terms: {student_info['Number of terms']}")
            transcript_lines.append(f"\n{'=' * 40}\nLevel: {level_names.get(level, level)}\n{'=' * 40}")

            for term, term_data in data['terms'].items():
                transcript_lines.append(f"\n{'*' * 10} Term {term} {'*' * 10}")
                transcript_lines.append(f"{'course ID':<10} {'course name':<15} {'credit hours':<15} {'grade':<10}")
                transcript_lines.append("-" * 40)

                for course in term_data['major_courses']:
                    transcript_lines.append(
                        f"{course['courseID']:<10} {course['courseName']:<15} {course['creditHours']:<15} {course['Grade']:<10}"
                    )

                for course in term_data['minor_courses']:
                    transcript_lines.append(
                        f"{course['courseID']:<10} {course['courseName']:<15} {course['creditHours']:<15} {course['Grade']:<10}"
                    )

                transcript_lines.append(f"\nMajor Average = {term_data['term_avg_major']:.2f}")
                transcript_lines.append(f"Minor Average = {term_data['term_avg_minor']:.2f}")
                transcript_lines.append(f"Term Average = {term_data['term_avg']:.2f}")

            transcript_lines.append(f"Overall Average = {data['overall_avg']:.2f}\n\n")

        output_filename = f"{stdID}_FullTranscript.txt"
        with open(output_filename, "w") as file:
            file.write("\n".join(transcript_lines))

        print("\n".join(transcript_lines))
        print(f"\nTranscript saved to {output_filename}")

    student_details_path = "studentDetails.csv"
    student_courses_path = f"{stdID}.csv"
    generate_full_transcript(stdID, student_details_path, student_courses_path, levels)

    #Pause for a few seconds
    time.sleep(10)

    #clears the screen and redirects to menu
    os.system('cls')
    print("Redirecting to main menu...")
    time.sleep(2) #waits a few seconds
    os.system('cls') #clears again before returning back to main menu

def previousRequestsFeature(request_history, dates, times, stdID):
    # Ensure the input lists are not empty
    if not request_history or not dates or not times:
        print("No request history available.")
        time.sleep(2)
        return

    # Show the request history on the screen
    print("\nPrevious Transcript Requests")
    print("Request\tDate\tTime")
    print("======================================")
    for i in range(len(request_history)):
        print(f"{request_history[i]}\t{dates[i]}\t{times[i]}")

    # Ask if the user wants to save the request history to a file
    save_to_file = input("Would you like to save this request history to a file? (Y/N): ").strip().lower()
    
    if save_to_file == 'y':
        file_name = f"{stdID}_PreviousRequests.txt"

        # Check if the file already exists
        file_exists = os.path.exists(file_name)

        # Prepare the content for the file
        content = ""
        if not file_exists:
            content += "Request\tDate\tTime\n"
            content += "======================================\n"

        for i in range(len(request_history)):
            content += f"{request_history[i]}\t{dates[i]}\t{times[i]}\n"

        # Append the content to the file
        with open(file_name, "a") as file:
            file.write(content)

        print(f"Request history has been {'updated' if file_exists else 'saved'} to {file_name}.")
    else:
        print("Request history was not saved to a file.")

    # Pause for a few seconds, clear the screen, and redirect to the menu
    input("Press Enter to return to the menu.")
    time.sleep(3)
    os.system('cls' if os.name == 'nt' else 'clear')

def terminateFeature(request_history):
    print("======================================")
    print(f"Number of requests: {len(request_history)}")

def newStudentFeature():
    #clear termninal screen
    if os.name == 'nt': #for windows
        os.system('cls')
    else:
        os.system('clear') #for linux and mac

    #notify the user
    print("Preparing for a new student...")
    time.sleep(2)

        #redirect to the main menu or start feature
    print("Redirecting to the main menu...")
    time.sleep(1)
    startFeature()

startFeature()
