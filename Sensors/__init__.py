from threading import *


class Photoresistor(Thread):

    def __init__(self, pin, bouncetime):
        Thread.__init__(self)
        self.pin = pin
        self.bounce_time = bouncetime



    def run(self) -> None:
        pass


