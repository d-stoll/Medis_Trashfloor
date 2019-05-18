from multiprocessing import Process, Queue
from TimeControl import TimeControl
import threading
import os
from Sensors.Photoresistor import Photoresistor
from MediaDevices.MusicPlayer import MusicPlayer
from MediaDevices.Lightstrip import Lightstrip
from Models.PhotoresistorDto import PSignal
from Models.MusicDto import MusicCmd

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

        self.timer = None

    # Reagiert auf Events von der Lichtschranke
    def react_on_event(self):
        if self.state == 0:
            self.state += 1
            self.queue_mp.put(MusicCmd.PLAY)
            self.queue_ls.put(self.state)
            self.start_timer()
        elif self.state < 20:
            self.state += 1
            self.queue_ls.put(self.state)
        else:
            print(f"Counter: {self.state} -> Maximum erreicht")

        # Target-Funktion fuer den Timer
    def target_function(self):
        print("---------------------")
        print("Timer abgelaufen")
        if self.state == 1:
            self.state -= 1
            self.queue_mp.put(MusicCmd.STOP)
            self.queue_ls.put(self.state)
        elif self.state >= 1:
            self.state -= 1
            self.start_timer()
            self.queue_ls.put(self.state)
        print("Counter: ", self.state)
        print("---------------------")

    # Startet den Timer
    def start_timer(self):
        # TIMER STOPPEN
        if self.timer is not None:
            self.timer.cancel()
            self.timer = None
        self.timer = threading.Timer(TIMER_DURATION, self.target_function)
        self.timer.start()

    def run(self) -> None:
        self.photo_resistor.start()
        self.music_player.start()
        self.lightstrip.start()

        while True:
            try:
                motion = self.queue_pr.get()
                if not isinstance(motion, PSignal):
                    self.restart_photo_resistor()
                self.react_on_event()
            except Exception:
                self.restart_lightstrip()
                self.restart_music_player()
                self.restart_photo_resistor()

    def restart_photo_resistor(self):
        del self.queue_pr
        del self.photo_resistor
        self.queue_pr = Queue()
        self.photo_resistor = Photoresistor(PHOTO_PIN, PHOTO_BOUNCETIME, self.queue_pr)
        self.photo_resistor.start()

    def restart_music_player(self):
        del self.queue_mp
        del self.music_player
        self.queue_mp = Queue()
        self.music_player = MusicPlayer(DIR_MUSIC, self.queue_mp)
        self.music_player.start()

    def restart_lightstrip(self):
        del self.queue_ls
        del self.lightstrip
        self.queue_ls = Queue()
        self.lightstrip = Lightstrip(LED_COUNT, LED_PIN, self.queue_ls)
        self.lightstrip.start()


if __name__ == '__main__':
    Monitor().start()


