import csv
import datetime
import os
import time

def statisticsFeature(student_id):
    file_name = f"{student_id}.csv"
    output_file_name = f"std{student_id}statistics.txt"

    if not os.path.exists(file_name):
        print(f"Error: File {file_name} not found.")
        return

    # Read the CSV file
    with open(file_name, mode='r') as file:
        reader = csv.DictReader(file)
        records = list(reader)

    # Separate undergraduate and graduate records
    undergraduate = [row for row in records if row['Level'] == 'U']
    graduate = [row for row in records if row['Level'] == 'G']

    def calculate_statistics(records, level_name):
        statistics = f"{level_name} Level\n"
        if not records:
            statistics += "No records found.\n"
            return statistics

        terms = {}
        repeated_courses = set()
        overall_sum = 0
        overall_count = 0
        max_grade = float('-inf')
        min_grade = float('inf')
        max_terms = []
        min_terms = []

        for record in records:
            term = record['Term']
            course = record['courseName']
            grade = float(record['Grade'])

            # Track per-term data
            if term not in terms:
                terms[term] = []
            terms[term].append(grade)

            # Overall data
            overall_sum += grade
            overall_count += 1

            # Max/Min grades
            if grade > max_grade:
                max_grade = grade
                max_terms = [term]
            elif grade == max_grade:
                max_terms.append(term)

            if grade < min_grade:
                min_grade = grade
                min_terms = [term]
            elif grade == min_grade:
                min_terms.append(term)

            # Check for repeated courses
            if sum(1 for rec in records if rec['courseName'] == course) > 1:
                repeated_courses.add(course)

        # Calculate averages
        overall_average = overall_sum / overall_count
        term_averages = {term: sum(grades) / len(grades) for term, grades in terms.items()}

        # Build statistics string
        statistics += f"Overall average (major and minor) for all terms: {overall_average:.2f}\n"
        statistics += "Average (major and minor) of each term:\n"
        for term, avg in term_averages.items():
            statistics += f"  Term {term}: {avg:.2f}\n"
        statistics += f"Maximum grade(s): {max_grade} in term(s): {', '.join(max_terms)}\n"
        statistics += f"Minimum grade(s): {min_grade} in term(s): {', '.join(min_terms)}\n"
        statistics += f"Do you have any repeated course(s)? {'Yes' if repeated_courses else 'No'}\n"
        if repeated_courses:
            statistics += f"Repeated courses: {', '.join(repeated_courses)}\n"

        return statistics

    # Compute and store statistics for each level
    undergraduate_stats = calculate_statistics(undergraduate, "Undergraduate")
    graduate_stats = calculate_statistics(graduate, "Graduate")

    # Combine all statistics
    all_statistics = undergraduate_stats + "\n" + graduate_stats

    # Display statistics on the screen
    print(all_statistics)

    # Save to file
    with open(output_file_name, mode='w') as output_file:
        output_file.write(all_statistics)

    # Clear the screen, wait, and redirect to the menu
    time.sleep(3)
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Returning to the menu...")
