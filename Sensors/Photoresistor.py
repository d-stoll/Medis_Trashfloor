from multiprocessing import Process, ProcessError, Queue
from Models.PhotoresistorDto import PSignal
import RPi.GPIO as GPIO
from time import sleep


class Photoresistor(Process):

    def __init__(self, photo_pin, photo_bouncetime, queue: Queue):
        Process.__init__(self)
        self.photo_pin = photo_pin
        self.photo_bouncetime = photo_bouncetime
        self.queue = queue

    # Initialisierung GPIOs
    def setup_gpios(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.photo_pin, GPIO.IN)
        GPIO.add_event_detect(self.photo_pin, GPIO.RISING, callback=self.share_event, bouncetime=self.photo_bouncetime)

    # Reagiert auf Events von der Lichtschranke
    def share_event(self):
        self.queue.put(PSignal.ACTIVE)

    def run(self) -> None:
        self.setup_gpios()
        while True:
            sleep(1)



