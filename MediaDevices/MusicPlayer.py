from multiprocessing import Process, Queue, ProcessError
import os
import pygame
import random
from Models.MusicDto import MusicCmd


# Implementiert einen Musikplayer, welcher gezielt ausgeloest werden kann um einen zufaelligen Song zu spielen.
class MusicPlayer(Process):
    EXT_LIST = ['.mp3']  # Liste aller kompatiblen Dateiendungen

    # Constructor fuer die Klasse MusicPlayerThread
    def __init__(self, directory, queue: Queue):
        Process.__init__(self)
        self.queue = queue
        self.directory = directory
        file_list = os.listdir(directory)
        self.song_list = [x for x in file_list if self.has_extension(x, self.EXT_LIST)]
        pygame.init()
        self.mixer = pygame.mixer
        self.mixer.init()
        self.mixer.music.set_volume(1.0)
        self.paused = False
        self.play_count = 0

    def run(self) -> None:
        while True:
            cmd = self.queue.get()
            if isinstance(cmd, MusicCmd):
                if cmd is MusicCmd.PLAY:
                    self.unpause()
                else:
                    self.pause()
            else:
                raise ProcessError("Illegal IPC-Message. Restart MusicPlayer-Process....")

    # Pausiert die aktuelle Wiedergabe
    def pause(self):
        self.mixer.music.pause()
        self.paused = True

    # Unpausiert die aktuelle Wiedergabe
    def unpause(self):
        if self.play_count >= 12:
            self.mixer.music.queue(self.get_random_song())
            self.play_count = 0
        else:
            self.play_count += 1

        self.mixer.music.unpause()
        self.paused = False

    # Setzt die Wiedergabe fort oder Spielt einen neuen Song
    def init_player(self):
        for _ in range(0, 3):
            self.mixer.music.queue(self.get_random_song())
        self.mixer.music.play()
        self.mixer.music.pause()
        self.paused = True

    # Waehlt einen zufaelligen Song aus
    def get_random_song(self):
        return self.directory + "/" + random.choice(self.song_list)

    # Beendet alle Instanzen
    def __del__(self):
        self.mixer.music.stop()
        del self.mixer
        pygame.quit()

    # Prueft eine Datei auf die richtige Endung
    @staticmethod
    def has_extension(input_file, ext_list):
        if input_file is None:
            return False
        for ext in ext_list:
            if input_file.endswith(ext):
                return True
        return False
