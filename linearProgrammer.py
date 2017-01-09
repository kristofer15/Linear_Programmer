from dateutil import rrule
from datetime import datetime, timedelta

import workout          # Entity
import term_io as io    # Interface class
import xlsx_io as file  # Storage

# Initalize which exercises to track, their current weights and planned increments
def initWorkout(wo):
    # Give the new program a name
    wo.workoutName = io.reqInput("Enter program name: ")
    setExercises(wo)
    setWeights(wo)
    setIncrements(wo)

def modifyWorkout(wo):
    choice = ''
    while(choice != '4'):
        io.printStatus(wo)
        options = {}
        options['1'] = "Set exercises"
        if(len(wo.ex) > 0):
            options['2'] = "Set weights"
            options['3'] = "Set increments"
        options['4'] = "Continue"
        choice = io.chooseAction(options)

        if(choice == '1'):
            setExercises(wo)
        elif(choice == '2'):
            setWeights(wo)
        elif(choice == '3'):
            setIncrements(wo)

# Name exercises that you want to track
def setExercises(wo):
    choice = ''
    while(choice != '3'):
        if(len(wo.ex) > 0):
            io.ssprint("Exercises:")
            io.printList(wo.ex)
        else:
            io.ssprint("No exercises set")
        options = {}
        options['1'] = "Add an exercise"
        options['2'] = "Remove an exercise"
        options['3'] = "Done"
        choice = io.chooseAction(options)
        
        if(choice == '1'):
            ex = io.reqInput("Exercise name: ")
            if(ex != ""):               # If anything was returned
               wo.ex.append(ex)
        elif(choice == '2'):
            i = 0
            exerciseOptions = {}
            for ex in wo.ex:
                i = i+1
                exerciseOptions[str(i)] = ex
            io.ssprint("Enter the number of the exercise you want to remove:")
            exerciseChoice = io.chooseAction(exerciseOptions)
            
            removee = exerciseOptions[exerciseChoice]
            if(io.confirmRemoval(removee)):
               wo.ex.remove(removee)

# Set the current weight of each exercise
def setWeights(wo):
    if(len(wo.ex) > 0):
        choice = ''
        while(choice != '-1'):       #Arbritrary number. Loop should exit on return command
            if(len(wo.weights) > 0):
                io.ssprint("Weights:")
                io.printDict(wo.weights)
            else:
                io.ssprint("No weights set")
                    
            io.ssprint("Choose an exercise to set your working weight:")
            options = {}
            options['1'] = "All"
            i = 2                    # Start i as next available option
            for ex in wo.ex:
                options[str(i)] = ex # Add option
                i = i+1              # Increment i for next option

            doneOpNum = i            # The done option comes after the dynamic middle, so make sure we remember it's number
            options[str(doneOpNum)] = "Done"
            
            choice = io.chooseAction(options)

            if(choice == '1'):
                io.ssprint("Enter your current weight for each exercise: ")
                wo.weights = io.getDict(wo.ex)
            elif(choice == str(doneOpNum)):
                return
            else:
                exercise = options[choice]                  # Get the name of the exercise chosen
                newWeight = io.reqInput(exercise + ": ")    # Request the new weight
                wo.weights[exercise] = newWeight            # Set the new weight

# Set the planned increment of each exercise
def setIncrements(wo):
    if(len(wo.ex) > 0):
        choice = ''
        while(choice != '-1'):  #Arbritrary number. Loop should exit on return command
            if(len(wo.increments) > 0):
                io.ssprint("Increments:")
                io.printDict(wo.increments)
            else:
                io.ssprint("No increments set")
            io.ssprint("Choose an exercise to set your planned weight increments per workout:")
            options = {}
            options['1'] = "All"
            i = 2                    # Start i as next available option
            for ex in wo.ex:
                options[str(i)] = ex # Add option
                i = i+1              # Increment i for next option

            doneOpNum = i            # The done option comes after the dynamic middle, so make sure we remember it's number
            options[str(doneOpNum)] = "Done"
            
            choice = io.chooseAction(options)

            if(choice == '1'):
                io.ssprint("Enter your current per workout weight increment for each exercise: ")
                wo.increments = io.getDict(wo.ex)
            elif(choice == str(doneOpNum)):
                return
            else:
                exercise = options[choice]                  # Get the name of the exercise chosen
                newWeight = io.reqInput(exercise + ": ")    # Request the new increment
                wo.weights[exercise] = newWeight            # Set the new increment

def export_xlsx(wo):
    f = file.xlsx_io(wo.workoutName) # Create an instance of our file class
    
    columns = wo.ex[:]               # Copy wo.ex by value
    columns.insert(0, "Day")
    columns.insert(0, "Date")
    f.setColumns(columns)

    weights = wo.weights
    now = datetime.now()
    for d in rrule.rrule(rrule.DAILY, dtstart=now, until=now+timedelta(days=90)):   # Iterate through 30 days
        if(d.strftime('%a') in ["Mon", "Wed", "Fri"]):                              # If the day is in the list
            row = {}
            row["Day"] = d.strftime('%a')
            row["Date"] = d.strftime('%b %d')
            for ex in wo.ex:
                row[ex] = float(weights[ex])
                weights[ex] = float(weights[ex]) + float(wo.increments[ex])

            f.writeRow(row)

    f.generateXLSX()                # Write the file (Overwrites existing)
    
    
def main():
    wo = workout.Workout()
    # TODO: Attempt to load workout
    if(len(wo.ex) <= 0):
        initWorkout(wo)
    modifyWorkout(wo)

    export_xlsx(wo)

main()
