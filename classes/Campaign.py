class Campaign:
    """Controls the ordered adventure and detects the final ending."""

    LEVEL_NAMES = [
        "Level1-1",
        "Level1-2",
        "Level1-3",
        "Level1-4",
        "Level2-1",
        "Level2-2",
        "Level2-3",
        "Level3-1",
    ]

    def __init__(self):
        self.levelNames = list(self.LEVEL_NAMES)
        self.currentIndex = 0

    def getCurrentLevel(self):
        return self.levelNames[self.currentIndex]

    def hasNextLevel(self):
        return self.currentIndex < len(self.levelNames) - 1

    def goToNextLevel(self):
        if self.hasNextLevel() == False:
            return False

        self.currentIndex += 1
        return True

    def getProgressText(self):
        return str(self.currentIndex + 1) + " / " + str(len(self.levelNames))
