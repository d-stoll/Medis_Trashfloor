# Kopfkommentar, noch zu schreiben

import os, sys, time, random, threading, pygame
import RPi.GPIO as GPIO
from rpi_ws281x import *


# Implementiert einen Lightstrip.
class Lightstrip:
    
    # Constructor fuer die Klasse Lightstrip
    def __init__(self, led_count, led_pin):
        self.strip = Adafruit_NeoPixel(led_count, led_pin)
        self.strip.begin()
        self.clear()
    
    # Laedt Ladebalkenmuster auf
    def loading(self, counter):
        for i in range(self.strip.numPixels()):
            if i < (3*counter):
                if i < 9:
                    self.strip.setPixelColorRGB(i, 255, 0, 0)
                elif i < 30:
                    self.strip.setPixelColorRGB(i, 255, 70, 0)
                elif i < 51:
                    self.strip.setPixelColorRGB(i, 255, 200, 0)
                else:
                    self.strip.setPixelColorRGB(i, 50, 255, 0)
            else:
                self.strip.setPixelColorRGB(i, 0, 0, 0)
        self.strip.show()
    
    # Stellt alle LEDs aus
    def clear(self):
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColorRGB(i, 0, 0, 0)
        self.strip.show()
    
    # Beendet alle Instanzen
    def delete(self):
        self.clear()
        del self.strip


# Implementiert einen Musikplayer, welcher gezielt ausgeloest werden kann um einen zufaelligen Song zu spielen.
class MusicPlayerThread(threading.Thread):
    playing = False  # statisches Attribut fuer den aktuellen Abspielstatus
    paused = False  # statisches Attribut fuer den Pausierungsstatus
    isRunning = True # statisches Attribut fuer den Threadstatus
    EXT_LIST = ['.mp3'] # Liste aller kompatiblen Dateiendungen

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


# Implementiert eine Manager-Klasse, welcher auf Events der Lichtschranke
# reagiert und die daraus resultierenden Ablaeufe managed.        
class Manager:
    timer = None

    # Constructor fuer die Klasse Manager
    def __init__(self, directory, led_count, led_pin, timer_duration):
        self.counter = 0
        self.timer_duration = timer_duration
        self.musicplayer = MusicPlayerThread(directory)
        self.musicplayer.start()
        self.lightstrip = Lightstrip(led_count, led_pin)
    
    # Reagiert auf Events von der Lichtschranke
    def react_on_event(self, channel):
        print("---------------------")
        print("Event detected")
        if self.counter == 0:
            self.counter += 1
            print("Counter: ", self.counter)
            self.musicplayer.play()
            self.lightstrip.loading(self.counter)
            self.start_timer()
        elif self.counter < 20:
            self.counter += 1
            self.lightstrip.loading(self.counter)
            print("Counter: ", self.counter)
        else:
            print("Counter: ", self.counter, " -> Maximum erreicht")
        print("---------------------")
    
    # Target-Funktion fuer den Timer
    def target_function(self):
        print("---------------------")
        print("Timer abgelaufen")
        if self.counter == 1:
            self.counter -= 1
            self.musicplayer.stop_song()
            self.lightstrip.loading(self.counter)
        elif self.counter >= 1:
            self.counter -= 1
            self.start_timer()
            self.lightstrip.loading(self.counter)
        print("Counter: ", self.counter)
        print("---------------------")
    
    # Startet den Timer
    def start_timer(self):
        #TIMER STOPPEN
        if self.timer is not None:
            self.timer.cancel()
            self.timer = None
        self.timer = threading.Timer(self.timer_duration, self.target_function)
        self.timer.start()
    
    # Beendet alle Instanzen
    def close(self):
        if self.timer is not None:
            self.timer.cancel()
            self.timer = None
        self.musicplayer.delete()
        del self.musicplayer
        self.lightstrip.delete()
        del self.lightstrip
    
        
def run_endless(path_music, photo_pin, photo_bouncetime, led_pin, led_count, timer_duration):
    manager = Manager(path_music, led_count, led_pin, timer_duration)

    # Initialisierung GPIOs
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(photo_pin, GPIO.IN)
    GPIO.add_event_detect(photo_pin, GPIO.RISING, callback=manager.react_on_event, bouncetime=photo_bouncetime)

    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        manager.close()
        del manager
        GPIO.remove_event_detect(photo_pin)
        print("System finished")
        return
    except:
        print("System crash, system restarting...")
        manager.close()
        del manager
        GPIO.remove_event_detect(photo_pin)
        run_endless()


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
