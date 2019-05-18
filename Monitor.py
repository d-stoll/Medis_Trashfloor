from multiprocessing import Process
from TimeControl import TimeControl
import os

# TODO: Build Processes with Queues for IPC, start them and manage the Communication.
# TODO: Repair after Subprocess failes.
# TODO: Long-Term Testing


class Monitor(Process):

    def __init__(self):
        Process.__init__(self)
        self.state = 0


    def run(self) -> None:
        pass


if __name__ == '__main__':

    # Parameter Photodetektor
    PHOTO_PIN = 23
    PHOTO_BOUNCETIME = 150

    # Parameter LED-Strip
    LED_PIN = 21
    LED_COUNT = 60

    # Parameter Timer
    TIMER_DURATION = 2
    # NOCH HINZUFUEGEN: COUNTER_MAX

    # Parameter Musicplayer
    DIR_MUSIC = os.path.dirname(os.path.realpath(__file__)) + "/Music_Medis"

    # Programmstart
    run_endless(DIR_MUSIC, PHOTO_PIN, PHOTO_BOUNCETIME, LED_PIN, LED_COUNT, TIMER_DURATION)