# Choose between displayed options.
# Utilizes Bastardized Dependency Injection Attempt tm
# - Good for flow control
def chooseAction(options):
    print("Select an option:")
    printDict(options)
    choice = input("Choice: ")
    if(choice not in options):
        print("Invalid choice. Please choose one of the numbered options")
        return chooseAction(options)
    return choice

def printStatus(workout):
    print("Workout program name: " + workout.workoutName)
    
    print("Registered exercises:")
    printList(workout.ex)

    print("Registered weights:")
    printDict(workout.weights)

    print("Registered increments:")
    printDict(workout.increments)

def printList(myList):
    for item in myList:
        print(" - " + item)
    print("")

def printDict(d):
    myList = []
    for item in d:
        myList.append(str(item) + ": " + d[item])
    printList(myList)

# Request user input with a provided request string
# - Seperates IO from logic
def reqInput(req):
    return input(req)

# Currently redundant but can improve modularity
def ssprint(msg):
    print(msg)

# Notify user of the item that is about to be removed
# Return true for final approval
def confirmRemoval(item):
    print("About to remove " + item)
    if(reqInput("Are you sure? (y/n): ").lower() == 'y'):
        return True
    return False

def getDict(myList):
    d = {}
    for item in myList:
        d[item] = reqInput(str(item) + ": ")

    return d
