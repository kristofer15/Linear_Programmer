class Workout:
    def __init__(self):
        self.workoutName = ""
        # List of all tracked exercises
        self.ex = []
        # Dictionary of the increment that an exercise should increase by for every workout
        self.increments = {}
        # Dictionary of the current working weight for each exercise
        self.weights = {}
