"""
COMMENTS FOR A GOOD PROGRAM!!
"""
#import important modules

import pickle
import datetime

#Define important variables


reviewListObject = {} #main thing that will hold all the user data. Format is index#: [thingToRemember, timesReviewed, month, day, year, absolute day count]
archivedObject = {} #secondary main thing that will hold all the user archived data


#Define minor (for specific function) variables


userChoice = '' #to make the while loop starts
currentDT = datetime.datetime.now() #get the current date & time
currentDate = [currentDT.month, currentDT.day, currentDT.year] #get the current date and format into an array

#Define various important functions

def establishMonths(currentDate): #establishes various month variables
    global months
    global theMonthNumber
    global amountOfDaysInMonths
    
    months = {'January': 31, #initialize the months variable
          'February': 28,
          'March': 31,
          'April': 30,
          'May': 31,
          'June': 30,
          'July': 31,
          'August': 31,
          'September': 30,
          'October': 31,
          'November': 30,
          'December': 31}
    theMonthNumber = {'January': 0, #index of the month
                  'February': 1,
                  'March': 2,
                  'April': 3,
                  'May': 4,
                  'June': 5,
                  'July': 6,
                  'August': 7,
                  'September': 8,
                  'October': 9,
                  'November': 10,
                  'December': 11}
    amountOfDaysInMonths = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    if (currentDate[2] % 100 != 0 and currentDate[2] % 4 == 0) or currentDate[2] % 400 == 0: #change amount of days in February to 29 if its a leap year
        months['February'] = 29
    amountOfDaysInMonths[1] = months['February'] #make the array leap year friendly
    
def printMenu(): #Prints the menu of options, asks for an input from the user
    print('MENU')
    print('M - Reprint this menu')
    print('A - Add a new thing to study')
    print('D - Delete a thing to study')
    print('R - Studied a thing to study')
    print('C - List the things you currently have to study')
    print('U - List current and upcoming things to study')
    print('LA - List the archive of things you had to study')
    print('Q - Save and quit the program')
    print('Q! - Quit the program without saving')

def iterateDate(amountOfDays, currentMonth, currentDay, currentYear):
    #initalization of various variables
    currentMonthAsIndex = currentMonth - 1
    absoluteDaysCurrent = 0
    absoluteDaysFuture = 0

    futureYear = 0
    futureMonth = 0
    futureDay = 0

    for index in range(0, currentMonthAsIndex): #correctly defines absoluteDaysCurrent variable
        absoluteDaysCurrent += amountOfDaysInMonths[index]
        
    absoluteDaysCurrent += currentDay
    absoluteDaysFuture += absoluteDaysCurrent + amountOfDays #base absoluteDaysFuture variable on absoluteDaysCurrent
    
    if absoluteDaysFuture > sum(amountOfDaysInMonths): #if absoluteDaysFuture is in the next year
        futureYear = currentYear + 1
        futureMonth = 'January'
        futureDay = absoluteDaysFuture - sum(amountOfDaysInMonths)
        absoluteDaysFuture -= sum(amountOfDaysInMonths)
        
    else: #if absoluteDaysFuture isn't in the next year
        futureYear = currentYear
        absoluteDaysFutureReduced = absoluteDaysFuture
        monthIndex = 0
        while absoluteDaysFutureReduced > amountOfDaysInMonths[monthIndex]: #figure out the correct month
            absoluteDaysFutureReduced -= amountOfDaysInMonths[monthIndex]
            monthIndex += 1
        for correctMonth in theMonthNumber: #match the month index to the month's name (the key value)
            if theMonthNumber[correctMonth] == monthIndex:
                futureMonth = correctMonth
        futureDay = absoluteDaysFutureReduced
    return [absoluteDaysFuture, futureMonth, futureDay, futureYear]
""" returns an array with absoluteDaysFuture,
this is used to determine easily if the date of something to review has been passed already"""


def setReview(thingToRemember, timesReviewed, currentMonth, currentDay, currentYear): #function that sets the next review date for a specific thing to review
    reviewIntervals = [1,2,4,7,14]
    amountOfDays = reviewIntervals[timesReviewed]
    futureDate = iterateDate(amountOfDays, currentMonth, currentDay, currentYear)
    
    return [thingToRemember, timesReviewed, futureDate[1], futureDate[2], futureDate[3],futureDate[0]]

def printListObject(Object): #prints either reviewListObject or archivedObject in a nice format
    for thing in Object:
        print(str(thing) + ' --- ' + Object[thing][0] + ' --- Next review date: ' + Object[thing][2] + '-' + str(Object[thing][3]) + '-' + str(Object[thing][4]), end = ' ')
        print('--- Reviewed', str(Object[thing][1]), 'times')
    """POSSIBLE IMPROVEMENT:
    ORDER THE LIST BY CLOSEST TO PRESENT DAY TO FARTHEST FROM PRESENT DAY
    """
def archiver(): #archives things that have been reviewed more than 4 times
    for thing in reviewListObject:
        if reviewListObject[thing][1] >= 5:
            archivedObject[thing] = reviewListObject[thing]
            del reviewListObject[thing]
            
def checkIsItTimeToReview(array): #returns true/false on whether or not the review day for a study topic has been passed. Specific to the array format set by setReview().
    absoluteDaysCurrent = 0
    currentMonthAsIndex = currentDT.month - 1
    for index in range(0, currentMonthAsIndex): #correctly defines absoluteDaysCurrent variable
        absoluteDaysCurrent += amountOfDaysInMonths[index]
        
    absoluteDaysCurrent += currentDT.day
    if absoluteDaysCurrent >=array[5]:
        return True
    else:
        return False

def printOnlyCurrentStudyThings():
    
    testIfAnyCurrent = 0
    for thing in reviewListObject:
            if checkIsItTimeToReview(reviewListObject[thing]):
                testIfAnyCurrent += 1
                print(str(thing) + ' --- ' + reviewListObject[thing][0] + ' Next review date: ' + reviewListObject[thing][2] + '-' + str(reviewListObject[thing][3]) + '-' + str(reviewListObject[thing][4]), end = ' ')
                print('Reviewed', str(reviewListObject[thing][1]), 'times')
    if testIfAnyCurrent == 0:
        print('There\'s nothing for you to study currently.')
        
#check if the user has used the program before:
haveUsedProgram = input('Have you used this program before? (Y/N)')
if haveUsedProgram == 'Y': #could be improved by using a try catch
    with open('fighting_the_forgetting_curve.pkl', 'rb') as saveFile: #loads the save file
        reviewListObject, archivedObject, indexPerEntry = pickle.load(saveFile)

printMenu() #prints the menu of options
archiver()

if reviewListObject == {} and archivedObject == {}: #initializes the indexPerEntry variable ONLY IF the user selects N for 'Have you used this program before? (Y/N)'
    indexPerEntry = 0
while(userChoice != 'Q' and userChoice != 'Q!'): #start of the operations that the user sees
   
    

    establishMonths(currentDate) #sets the month-related variables
    
          
    userChoice = input('Choose an option:\n').upper() #allows the user to choose an option
    
    if userChoice == 'A': #user option of adding something to study
        thingToRemember = input('What do you need to remember?\n')
        indexPerEntry += 1
        
        reviewListObject[indexPerEntry] = setReview(thingToRemember, 0, currentDate[0], currentDate[1], currentDate[2])
        print(reviewListObject[indexPerEntry][0], 'has been added to your database!')

    elif userChoice == 'D': #user option of deleting
        printListObject(reviewListObject)
        thingToDelete = int(input('Which number would you like to delete?\n'))
        if thingToDelete in reviewListObject:
            del reviewListObject[thingToDelete]
            print(thingToDelete, 'has been deleted!')
        else:
            print('Sorry, couldn\'t find that in the list!')
    elif userChoice == 'C': #user option of displaying things currently need to study/review
        printOnlyCurrentStudyThings()
    elif userChoice == 'U': #user option displaying all things that need to be reviewed at some point
        printListObject(reviewListObject)
    elif userChoice == 'M': #user option that prints the menu
        printMenu()
    elif userChoice == 'R': #user option that updates an entry in reviewListObject
        printOnlyCurrentStudyThings()
        thingReviewed = input('What number did you review? Type \'back\' if there\'s nothing to study currently.\n')
        try: #reject non-integer inputs
            thingReviewed = int(thingReviewed)
            if thingReviewed in reviewListObject: #check if number is in reviewListObject
                if checkIsItTimeToReview(reviewListObject[thingReviewed]): #check if number should be reviewed yet
                    reviewListObject[thingReviewed][1] += 1
                    reviewListObject[thingReviewed] = setReview(reviewListObject[thingReviewed][0], reviewListObject[thingReviewed][1], currentDate[0], currentDate[1], currentDate[2])
                    print(reviewListObject[thingReviewed][0], 'has been updated!')
                else:
                    print('You aren\'t supposed to review that yet!')
            else:
                print('That\'s not on the list, but you can add it !')
            
        except ValueError: #rejects non-integer inputs
            if thingReviewed == 'back':
                print('')
            else:
                print('That\'s not a number!')
                
    elif userChoice == 'LA': #user option to list archived things to study
        printListObject(archivedObject)
    elif userChoice == 'Q': #user option to quit and save the program
        print('bye bye !')
        with open('fighting_the_forgetting_curve.pkl', 'wb') as saveFile:
            pickle.dump([reviewListObject, archivedObject, indexPerEntry], saveFile)
    elif userChoice == 'Q!': #user option to quit without saving
        print('bye bye!')
    else:
        print('Didn\'t recognize that, try again.')

                                             
