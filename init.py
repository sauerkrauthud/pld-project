def startFeature():
    stdLevel = str(input("Please enter your student level here (G for Graduate, U for Undergraduate, B for Both): "))
    while stdLevel != "U" or stdLevel != "G" or stdLevel != "B":
        stdLevel = str(input("Please enter your student level here (G for Graduate, U for Undergraduate, B for Both): "))
    if stdLevel == "U":
        stdDegree = "N/A - Undergraduate."
        stdID = int(input("Please enter your student ID number here: (ie: 2020006000): "))
    if stdLevel == "G" or stdLevel == "B":
        stdDegree = str(input("Are you taking a Masters, a Doctorate, or Both? (M for Masters, D for Doctorate and B0 for Both): "))
        stdID = int(input("Please enter your student ID number here: (ie: 2020006000): "))

def menuFeature():
    print("\nStudent Transcript Generation System")
    print("======================================")
    print("1. Student Details")
    print("2. Statistics")
    print("3. Transcript based on Major Courses")
    print("4. Transcript based on Minor Courses")
    print("5. Full Transcript")
    print("6. Previous Transcript Requests")
    print("7. Select Another Student")
    print("8. Terminate the System")
    option = int(input("Enter Your Feature: "))

startFeature()
menuFeature()
