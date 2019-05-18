from multiprocessing import Process, Queue
from TimeControl import TimeControl
import os
from Sensors.Photoresistor import Photoresistor
from MediaDevices.MusicPlayer import MusicPlayer
from MediaDevices.Lightstrip import Lightstrip

# TODO: Build Processes with Queues for IPC, start them and manage the Communication.
# TODO: Repair after Subprocess failes.
# TODO: Long-Term Testing

# Parameter Photodetektor
PHOTO_PIN = 23
PHOTO_BOUNCETIME = 150

# Parameter LED-Strip
LED_PIN = 21
LED_COUNT = 60

# Parameter Timer
TIMER_DURATION = 2

# Parameter Musicplayer
DIR_MUSIC = os.path.dirname(os.path.realpath(__file__)) + "/Music_Medis"


class Monitor(Process):

    def __init__(self):
        Process.__init__(self)
        self.state = 0

        self.queue_pr = Queue()
        self.photo_resistor = Photoresistor(PHOTO_PIN, PHOTO_BOUNCETIME, self.queue_pr)

        self.queue_mp = Queue()
        self.music_player = MusicPlayer(DIR_MUSIC, self.queue_mp)

        self.queue_ls = Queue()
        self.lightstrip = Lightstrip(LED_COUNT, LED_PIN, self.queue_ls)

    def run(self) -> None:
        self.photo_resistor.start()
        self.music_player.start()
        self.lightstrip.start()


if __name__ == '__main__':
    Monitor().start()


