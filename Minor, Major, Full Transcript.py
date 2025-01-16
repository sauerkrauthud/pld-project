import csv
import datetime
import os
import time

# def startFeature():
#     stdLevel = str(input("Please enter your student level here (G for Graduate, U for Undergraduate, B for Both): "))
#     if stdLevel == "U":
#         stdDegree = "N/A - Undergraduate."
#         stdID = int(input("Please enter your student ID number here: (ie: 2020006000): "))
#     if stdLevel == "G" or stdLevel == "B":
#         stdDegree = str(input("Are you taking a Masters, a Doctorate, or Both? (M for Masters, D for Doctorate and B0 for Both): "))
#         stdID = int(input("Please enter your student ID number here: (ie: 2020006000): "))

#start feature
# def previousRequestsFeature(request_history, dates, times):
    # Ensure the input lists are not empty
    # if not request_history or not dates or not times:
    #     print("No request history available.")
    #     return

    # # Show the request history on the screen
    # print("\nPrevious Transcript Requests")
    # print("Request\tDate\tTime")
    # print("======================================")
    # for i in range(len(request_history)):
    #     print(f"{request_history[i]}\t{dates[i]}\t{times[i]}")

    # # Ask if the user wants to save the request history to a file
    # save_to_file = input("Would you like to save this request history to a file? (Y/N): ").strip().lower()
    # if save_to_file == 'y':
    #     student_id = input("Please enter your student ID: ").strip()
    #     file_name = f"{student_id}PreviousRequests.txt"

    #     # Prepare the content for the file
    #     content = "Request\tDate\tTime\n"
    #     content += "======================================\n"
    #     for i in range(len(request_history)):
    #         content += f"{request_history[i]}\t{dates[i]}\t{times[i]}\n"

    #     # Write the content to the file
    #     with open(file_name, "w") as file:
    #         file.write(content)

    #     print(f"Request history has been saved to {file_name}.")
    # else:
    #     print("Request history was not saved to a file.")

    # # Pause for a few seconds
    # input("Press Enter to return to the menu.")


def menuFeature():
    # Lists to hold the request data
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
    
    request_history = []
    dates = []
    times = []

    # Get current time for timestamp
    now = datetime.datetime.now()

    # Format time in 12-hour format with AM/PM
    formatted_time = now.strftime("%I:%M %p")
    


    confirm = True
    while confirm:
        try:
            option = int(input("Enter Your Feature: "))
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 8.")
            continue

        if 1 <= option <= 8:
            if option == 1:
                detailsFeature('201009000')
                # number is just an example, needs to be a variable in menufeature
            elif option == 2:
                print("kys")  # Replace this with actual functionality
            elif option == 3:
                MajorTranscript()
                request_history.append("Major")
                dates.append(str(now.date()))
                times.append(formatted_time)  
            elif option == 4:
                MinorTranscript()
                request_history.append("Minor")
                dates.append(str(now.date()))
                times.append(formatted_time)
            elif option == 5:
                FullTranscript()
                request_history.append("Full")
                dates.append(str(now.date()))
                times.append(formatted_time)
            elif option == 6:
                previousRequestsFeature(request_history, dates, times) 
            elif option == 8:
                terminateFeature(request_history)
                confirm = False
        else:
            print("Invalid option. Please try again.")
            continue

def MajorTranscript():
    def load_csv(filepath):
        """Load CSV file into a list of dictionaries."""
        data = []
        with open(filepath, 'r') as file:
            headers = file.readline().strip().split(',')
            for line in file:
                values = line.strip().split(',')
                data.append(dict(zip(headers, values)))
        return data

    def generate_transcript(stdID, student_details_path, student_courses_path):
        """
        Generates the transcript for a student and saves it to text files.

        Args:
            stdID (int): Student ID.
            student_details_path (str): Path to the student details CSV file.
            student_courses_path (str): Path to the student courses CSV file.
        """
        # Load data
        student_details = load_csv(student_details_path)
        student_courses = load_csv(student_courses_path)

        # Filter student details for the given stdID
        student_info_list = [student for student in student_details if int(student['stdID']) == stdID]

        # Separate courses and transcript data for Undergraduate (U) and Graduate (G) levels
        levels = {"U": [], "G_M": [], "G_D": []}

        for student_info_row in student_info_list:
            level = student_info_row['Level']
            degree = student_info_row.get('Degree', '')  # Assume Degree column distinguishes M and D within G
            if level == "U":
                levels["U"].append(student_info_row)
            elif level == "G" and degree == "M1":
                levels["G_M"].append(student_info_row)
            elif level == "G" and degree == "D1":
                levels["G_D"].append(student_info_row)

        consolidated_transcript = []

        for level, students in levels.items():
            if not students:
                continue

            major_courses = []
            for student_info_row in students:
                major_courses += [
                    course for course in student_courses
                    if course['courseType'] == 'Major' and course['Level'] == student_info_row['Level']
                ]

            # Group courses by term to calculate averages and organize data
            terms = sorted(set(course['Term'] for course in major_courses))
            transcript_data = {}

            for term in terms:
                term_courses = [course for course in major_courses if course['Term'] == term]
                total_credits = sum(int(course['creditHours']) for course in term_courses)
                term_avg = sum(
                    int(course['Grade']) * int(course['creditHours']) for course in term_courses
                ) / total_credits
                transcript_data[term] = {
                    "courses": term_courses,
                    "term_avg": term_avg
                }

            # Calculate the overall average across all terms
            if major_courses:
                total_credit_hours = sum(int(course['creditHours']) for course in major_courses)
                overall_avg = sum(
                    int(course['Grade']) * int(course['creditHours']) for course in major_courses
                ) / total_credit_hours
            else:
                overall_avg = 0

            # Prepare transcript data for the current level
            student_info = students[0]
            transcript_lines = [
                f"\nName: {student_info['Name']}\tstdID: {student_info['stdID']}",
                f"College: {student_info['College']}\t\tDepartment: {student_info['Department']}",
                f"Major: {student_info['Major']}\t\tMinor: {student_info['Minor']}",
                f"Level: {student_info['Level']}\t\t\tDegree: {student_info.get('Degree', '')}",
                f"Number of terms: {len(terms)}",
                "=" * 40
            ]

            # Add term-wise data
            for term, data in transcript_data.items():
                transcript_lines.append(f"\n{'*' * 10} Term {term} {'*' * 10}")
                transcript_lines.append(f"{'course ID':<10} {'course name':<15} {'credit hours':<15} {'grade':<10}")
                transcript_lines.append("-" * 40)
                for course in data['courses']:
                    transcript_lines.append(
                        f"{course['courseID']:<10} {course['courseName']:<15} {course['creditHours']:<15} {course['Grade']:<10}"
                    )
                transcript_lines.append(f"Major Average = {data['term_avg']:.2f}")

            # Add overall average
            transcript_lines.append("=" * 40)
            transcript_lines.append(f"Overall Major Average = {overall_avg:.2f}")
            transcript_lines.append(f"{'*' * 10} End of Transcript for Level ({level}) {'*' * 10}\n\n")

            # Combine transcript lines for this level
            consolidated_transcript.append("\n".join(transcript_lines))

        # Display the consolidated transcript
        print("\n\n".join(consolidated_transcript))

        # Save the consolidated transcript to a single file
        output_filename = f"{stdID}MajorTranscript.txt"
        with open(output_filename, "w") as file:
            file.write("\n\n".join(consolidated_transcript))

    # Execute
    if __name__ == "__main__":
        # File paths (replace with actual paths if necessary)
        student_details_path = "studentDetails.csv"
        student_courses_path = "201006000.csv"

        # Student ID (example)
        stdID = 201006000

        # Generate transcript
        generate_transcript(stdID, student_details_path, student_courses_path)

def MinorTranscript():

    # Function to load a CSV file into a list of dictionaries
    def load_csv(filepath):
        """Load CSV file into a list of dictionaries."""
        data = []
        with open(filepath, 'r') as file:
            headers = file.readline().strip().split(',')  # Read the headers from the first line
            for line in file:
                values = line.strip().split(',')  # Split each line by commas
                data.append(dict(zip(headers, values)))  # Create a dictionary for each row
        return data

    # Function to generate the minor transcript for a student
    def generate_minor_transcript(stdID, student_details_path, student_courses_path):
        """
        Generates the minor transcript for a student and saves it to text files.

        Args:
            stdID (int): Student ID.
            student_details_path (str): Path to the student details CSV file.
            student_courses_path (str): Path to the student courses CSV file.
        """
        # Load data from the provided CSV files
        student_details = load_csv(student_details_path)
        student_courses = load_csv(student_courses_path)

        # Filter student details for the given stdID
        student_info_list = [student for student in student_details if int(student['stdID']) == stdID]

        # Separate courses and transcript data for Undergraduate (U) and Graduate (G) levels
        levels = {"U": [], "G_M": [], "G_D": []}  # Create categories for levels and degrees

        for student_info_row in student_info_list:
            level = student_info_row['Level']  # Determine the student's level
            degree = student_info_row.get('Degree', '')  # Check the degree (if applicable)
            if level == "U":
                levels["U"].append(student_info_row)
            elif level == "G" and degree == "M1":
                levels["G_M"].append(student_info_row)
            elif level == "G" and degree == "D1":
                levels["G_D"].append(student_info_row)

        consolidated_transcript = []  # To hold the complete transcript for all levels

        for level, students in levels.items():
            if not students:  # Skip if no students for this level
                continue

            minor_courses = []  # List to hold minor courses for the level
            for student_info_row in students:
                minor_courses += [
                    course for course in student_courses
                    if course['courseType'] == 'Minor' and course['Level'] == student_info_row['Level']
                ]

            # Group courses by term to calculate averages and organize data
            terms = sorted(set(course['Term'] for course in minor_courses))
            transcript_data = {}  # Dictionary to store courses and term averages

            for term in terms:
                term_courses = [course for course in minor_courses if course['Term'] == term]
                total_credits = sum(int(course['creditHours']) for course in term_courses)
                term_avg = sum(
                    int(course['Grade']) * int(course['creditHours']) for course in term_courses
                ) / total_credits  # Calculate weighted average for the term
                transcript_data[term] = {
                    "courses": term_courses,
                    "term_avg": term_avg
                }

            # Calculate the overall average across all terms
            if minor_courses:
                total_credit_hours = sum(int(course['creditHours']) for course in minor_courses)
                overall_avg = sum(
                    int(course['Grade']) * int(course['creditHours']) for course in minor_courses
                ) / total_credit_hours  # Calculate weighted overall average
            else:
                overall_avg = 0

            # Prepare transcript data for the current level
            student_info = students[0]  # Take the first student's info for headers
            transcript_lines = [
                f"\nName: {student_info['Name']}\tstdID: {student_info['stdID']}",
                f"College: {student_info['College']}\t\tDepartment: {student_info['Department']}",
                f"Major: {student_info['Major']}\t\tMinor: {student_info['Minor']}",
                f"Level: {student_info['Level']}\t\t\tDegree: {student_info.get('Degree', '')}",
                f"Number of terms: {len(terms)}",
                "=" * 40
            ]

            # Add term-wise data to the transcript
            for term, data in transcript_data.items():
                transcript_lines.append(f"\n{'*' * 10} Term {term} {'*' * 10}")
                transcript_lines.append(f"{'course ID':<10} {'course name':<15} {'credit hours':<15} {'grade':<10}")
                transcript_lines.append("-" * 40)
                for course in data['courses']:
                    transcript_lines.append(
                        f"{course['courseID']:<10} {course['courseName']:<15} {course['creditHours']:<15} {course['Grade']:<10}"
                    )
                transcript_lines.append(f"Minor Average = {data['term_avg']:.2f}")

            # Add overall average to the transcript
            transcript_lines.append("=" * 40)
            transcript_lines.append(f"Overall Minor Average = {overall_avg:.2f}")
            transcript_lines.append(f"{'*' * 10} End of Transcript for Level ({level}) {'*' * 10}")

            # Combine transcript lines for this level
            consolidated_transcript.append("\n".join(transcript_lines))

        # Display the consolidated transcript
        print("\n\n".join(consolidated_transcript))

        # Save the consolidated transcript to a single file
        output_filename = f"{stdID}MinorTranscript.txt"
        with open(output_filename, "w") as file:
            file.write("\n\n".join(consolidated_transcript))

    # Example usage
    if __name__ == "__main__":
        # File paths (replace with actual paths if necessary)
        student_details_path = "studentDetails.csv"
        student_courses_path = "201006000.csv"

        # Student ID (example)
        stdID = 201006000

        # Generate transcript
        generate_minor_transcript(stdID, student_details_path, student_courses_path)

def FullTranscript():

    # Function to load a CSV file into a list of dictionaries
    def load_csv(filepath):
        """Load CSV file into a list of dictionaries."""
        data = []
        with open(filepath, 'r') as file:
            headers = file.readline().strip().split(',')  # Read the headers from the first line
            for line in file:
                values = line.strip().split(',')  # Split each line by commas
                data.append(dict(zip(headers, values)))  # Create a dictionary for each row
        return data

    # Function to generate the full transcript for a student
    def generate_full_transcript(stdID, student_details_path, student_courses_path):
        """
        Generates the full transcript for a student (both major and minor) and saves it to text files.

        Args:
            stdID (int): Student ID.
            student_details_path (str): Path to the student details CSV file.
            student_courses_path (str): Path to the student courses CSV file.
        """
        # Load data from the provided CSV files
        student_details = load_csv(student_details_path)
        student_courses = load_csv(student_courses_path)

        # Filter student details for the given stdID
        student_info_list = [student for student in student_details if int(student['stdID']) == stdID]

        # Separate courses and transcript data for Undergraduate (U) and Graduate (G) levels
        levels = {"U": [], "G_M": [], "G_D": []}  # Create categories for levels and degrees

        for student_info_row in student_info_list:
            level = student_info_row['Level']  # Determine the student's level
            degree = student_info_row.get('Degree', '')  # Check the degree (if applicable)
            if level == "U":
                levels["U"].append(student_info_row)
            elif level == "G" and degree == "M1":
                levels["G_M"].append(student_info_row)
            elif level == "G" and degree == "D1":
                levels["G_D"].append(student_info_row)

        consolidated_transcript = []  # To hold the complete transcript for all levels

        for level, students in levels.items():
            if not students:  # Skip if no students for this level
                continue

            major_courses = []  # List to hold major courses for the level
            minor_courses = []  # List to hold minor courses for the level

            for student_info_row in students:
                major_courses += [
                    course for course in student_courses
                    if course['courseType'] == 'Major' and course['Level'] == student_info_row['Level']
                ]
                minor_courses += [
                    course for course in student_courses
                    if course['courseType'] == 'Minor' and course['Level'] == student_info_row['Level']
                ]

            # Group courses by term to calculate averages and organize data
            terms = sorted(set(course['Term'] for course in major_courses + minor_courses))
            transcript_data = {}  # Dictionary to store courses and term averages

            for term in terms:
                term_major_courses = [course for course in major_courses if course['Term'] == term]
                term_minor_courses = [course for course in minor_courses if course['Term'] == term]

                total_major_credits = sum(int(course['creditHours']) for course in term_major_courses)
                total_minor_credits = sum(int(course['creditHours']) for course in term_minor_courses)

                term_major_avg = sum(
                    int(course['Grade']) * int(course['creditHours']) for course in term_major_courses
                ) / total_major_credits if total_major_credits else 0

                term_minor_avg = sum(
                    int(course['Grade']) * int(course['creditHours']) for course in term_minor_courses
                ) / total_minor_credits if total_minor_credits else 0

                term_avg = (term_major_avg + term_minor_avg) / 2 if (term_major_avg and term_minor_avg) else 0

                transcript_data[term] = {
                    "major_courses": term_major_courses,
                    "minor_courses": term_minor_courses,
                    "term_major_avg": term_major_avg,
                    "term_minor_avg": term_minor_avg,
                    "term_avg": term_avg
                }

            # Calculate the overall average across all terms
            if major_courses or minor_courses:
                total_major_credits = sum(int(course['creditHours']) for course in major_courses)
                total_minor_credits = sum(int(course['creditHours']) for course in minor_courses)

                overall_major_avg = sum(
                    int(course['Grade']) * int(course['creditHours']) for course in major_courses
                ) / total_major_credits if total_major_credits else 0

                overall_minor_avg = sum(
                    int(course['Grade']) * int(course['creditHours']) for course in minor_courses
                ) / total_minor_credits if total_minor_credits else 0

                overall_avg = (overall_major_avg + overall_minor_avg) / 2 if (overall_major_avg and overall_minor_avg) else 0
            else:
                overall_major_avg = overall_minor_avg = overall_avg = 0

            # Prepare transcript data for the current level
            student_info = students[0]  # Take the first student's info for headers
            transcript_lines = [
                f"\nName: {student_info['Name']}\tstdID: {student_info['stdID']}",
                f"College: {student_info['College']}\t\tDepartment: {student_info['Department']}",
                f"Major: {student_info['Major']}\t\tMinor: {student_info['Minor']}",
                f"Level: {student_info['Level']}\t\t\tDegree: {student_info.get('Degree', '')}",
                f"Number of terms: {len(terms)}",
                "=" * 40
            ]

            # Add term-wise data to the transcript
            for term, data in transcript_data.items():
                transcript_lines.append(f"\n{'*' * 10} Term {term} {'*' * 10}")
                transcript_lines.append(f"{'course ID':<10} {'course name':<15} {'credit hours':<15} {'grade':<10}")
                transcript_lines.append("-" * 40)

                for course in data['major_courses']:
                    transcript_lines.append(
                        f"{course['courseID']:<10} {course['courseName']:<15} {course['creditHours']:<15} {course['Grade']:<10}"
                    )
                transcript_lines.append(f"\nMajor Average = {data['term_major_avg']:.2f}\n\n")

                for course in data['minor_courses']:
                    transcript_lines.append(
                        f"{course['courseID']:<10} {course['courseName']:<15} {course['creditHours']:<15} {course['Grade']:<10}"
                    )
                transcript_lines.append(f"\nMinor Average = {data['term_minor_avg']:.2f}\n")

                transcript_lines.append(f"Term Average = {data['term_avg']:.2f}")

            # Add overall averages to the transcript
            transcript_lines.append("=" * 40)
            transcript_lines.append(f"Overall Major Average = {overall_major_avg:.2f}")
            transcript_lines.append(f"Overall Minor Average = {overall_minor_avg:.2f}")
            transcript_lines.append(f"Overall Average = {overall_avg:.2f}")
            transcript_lines.append(f"{'*' * 10} End of Transcript for Level ({level}) {'*' * 10}")

            # Combine transcript lines for this level
            consolidated_transcript.append("\n".join(transcript_lines))

        # Display the consolidated transcript
        print("\n\n".join(consolidated_transcript))

        # Save the consolidated transcript to a single file
        output_filename = f"{stdID}FullTranscript.txt"
        with open(output_filename, "w") as file:
            file.write("\n\n".join(consolidated_transcript))

    # Example usage
    if __name__ == "__main__":
        # File paths (replace with actual paths if necessary)
        student_details_path = "studentDetails.csv"
        student_courses_path = "201006000.csv"

        # Student ID (example)
        stdID = 201006000

        # Generate transcript
        generate_full_transcript(stdID, student_details_path, student_courses_path)









# def detailsFeature(student_id):
#     # Open and read the CSV file
#     with open('studentDetails.csv', mode='r') as file:
#         reader = csv.DictReader(file)
        
#         # Iterate through each row in the CSV
#         for row in reader:
#             # Check if the student ID matches the given ID
#             if row['stdID'] == student_id:
#                 # Prepare the details to be printed and written
#                 student_details = (
#                     f"Name: {row['Name']}\n"
#                     f"Student ID: {row['stdID']}\n"
#                     f"Levels: {row['Level']}\n"
#                     f"Number of terms: {row['Terms']}\n"
#                     f"College(s): {row['College']}\n"
#                     f"Department(s): {row['Department']}\n"
#                 )
                
#                 # Print to console
#                 print(student_details)
                
#                 # Create the file name based on student ID
#                 file_name = f"{row['stdID']}details.txt"
                
#                 # Write the details to the text file
#                 with open(file_name, "w") as txt_file:
#                     txt_file.write(student_details)
                
#                 print(f"Student details have been saved to {file_name}.")
#                 return  # Exit the function once the student is found
        
#         # If student ID is not found
#         print("Student ID not found.")


# def terminateFeature(request_history):
#     print("======================================")
#     print(f"Number of requests: {len(request_history)}")


menuFeature()