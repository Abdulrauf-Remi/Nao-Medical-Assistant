import main

# this file defines the robot's reaction when a certain keyword is recognised by speech recognition

class Dialog(object):

    def __init__(self, movemodule):
        self._movemodule = movemodule
        
    def answer(self, question):
        if "stand up" in question:
            self._movemodule.standUp()
            return
        elif "sit down" in question:
            self._movemodule.sitDown()
            return 
        elif "dance" in question:
            self._movemodule.hulaHoop()
            return 
