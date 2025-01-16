import os
import time

def newStudentFeature():

#clear termninal screen
    if os.name == 'nt': #for windows
        os.system('cls')
    else:
        os.system('clear') #for linux and mac daming arte

#notify the user
print("Preparing for a new student...")
time.sleep(2)

#redirect to the main menu or start feature
print("Redirecting to the main menu...")
time.sleep(1)
startFeature()