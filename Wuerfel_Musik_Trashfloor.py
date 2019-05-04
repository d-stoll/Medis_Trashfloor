# Kopfkommentar, noch zu schreiben

import RPi.GPIO as GPIO
from MediaDevices.Lightstrip import *
from MediaDevices.MusicPlayer import *


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
