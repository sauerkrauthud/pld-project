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

    # Function to generate the statistics for an undergraduate.
    def generate_undergrad_statistics(stdID, student_details_path, student_courses_path):
    
    # Function to generate the statistics for a graduate.
    def generate_graduate_statistics(stdID, student_details_path, student_courses_path):
        
        
    
    
statisticsFeature()
