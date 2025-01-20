import csv
import datetime
import os
import time

def statisticsFeature(student_id, level):
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
    def generate_statistics(stdID, student_details_path, student_courses_path):
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
        
    
    
statisticsFeature()