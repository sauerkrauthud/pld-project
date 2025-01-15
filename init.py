def startFeature():
    stdLevel = str(input("Please enter your student level here (G for Graduate, U for Undergraduate, B for Both): "))
    if stdLevel == "U":
        stdDegree = "N/A - Undergraduate."
        stdID = int(input("Please enter your student ID number here: (ie: 2020006000): "))
    if stdLevel == "G" or stdLevel == "B":
        stdDegree = str(input("Are you taking a Masters, a Doctorate, or Both? (M for Masters, D for Doctorate and B0 for Both): "))
        stdID = int(input("Please enter your student ID number here: (ie: 2020006000): "))

def terminateFeature():
    print("Virus installed, have fun!")
    exit()

def detailsFeature():
    print("Name: ")
    print("Student ID: ")
    print("Levels: ")
    print("Number of terms: ")
    print("College(s): ")
    print("Department(s): ")

def menuFeature():
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
    
    # Try Again
    while True:
        option = int(input("Enter Your Feature: "))
        if option >= 1 or option <= 8:
            if option == 1:
                detailsFeature()
            if option == 2:
                print("kys")
            if option == 8:
                terminateFeature()
        if option < 1 or option > 8:
            print("Invalid option. Please try again.")
            continue

# startFeature()
# menuFeature()