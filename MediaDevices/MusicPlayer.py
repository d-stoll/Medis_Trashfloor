import threading
import os
import time
import pygame
import random


# Implementiert einen Musikplayer, welcher gezielt ausgeloest werden kann um einen zufaelligen Song zu spielen.
class MusicPlayerThread(threading.Thread):
    playing = False  # statisches Attribut fuer den aktuellen Abspielstatus
    paused = False  # statisches Attribut fuer den Pausierungsstatus
    isRunning = True  # statisches Attribut fuer den Threadstatus
    EXT_LIST = ['.mp3']  # Liste aller kompatiblen Dateiendungen

    # Constructor fuer die Klasse MusicPlayerThread
    def __init__(self, directory):
        threading.Thread.__init__(self)
        self.isRunning = True
        self.directory = directory
        file_list = os.listdir(directory)
        self.song_list = [x for x in file_list if self.has_extension(x, self.EXT_LIST)]
        self.mixer = pygame.mixer
        self.mixer.init()
        self.mixer.music.set_volume(1.0)

    # run Funktion fuer den Thread
    def run(self):
        while self.isRunning:
            if not self.mixer.music.get_busy():
                if self.playing and (not self.paused):
                    self.play()
            time.sleep(0.5)

    # Spielt einen Song
    def play_song(self, song):
        self.mixer.music.load(song)
        self.mixer.music.play()
        self.playing = True
        self.paused = False

    # Pausiert die aktuelle Wiedergabe
    def pause(self):
        if self.playing:
            self.mixer.music.pause()
            self.paused = True

    # Unpausiert die aktuelle Wiedergabe
    def unpause(self):
        if self.playing:
            self.mixer.music.unpause()
            self.paused = False

    # Beendet die aktuelle Wiedergabe
    def stop_song(self):
        self.mixer.music.stop()
        self.playing = False
        self.paused = False

    # Setzt die Wiedergabe fort oder Spielt einen neuen Song
    def play(self):
        if self.paused:
            self.unpause()
        else:
            self.stop_song()
            self.play_song(self.get_random_song())

    # Waehlt einen zufaelligen Song aus
    def get_random_song(self):
        return self.directory + "/" + random.choice(self.song_list)

    # Prueft eine Datei auf die richtige Endung
    def has_extension(self, input_file, ext_list):
        if input_file is None:
            return False
        for ext in ext_list:
            if input_file.endswith(ext):
                return True
        return False

    # Beendet alle Instanzen
    def delete(self):
        self.isRunning = False
        self.stop_song()
        del self.mixer
        pygame.quit()
        playing = False
        paused = False
