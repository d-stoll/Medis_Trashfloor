from rpi_ws281x import *
from multiprocessing import Process, Queue, ProcessError


# Implementiert einen Lightstrip.
class Lightstrip(Process):

    # Constructor fuer die Klasse Lightstrip
    def __init__(self, led_count, led_pin, queue: Queue):
        Process.__init__(self)
        self.queue = queue
        self.strip = Adafruit_NeoPixel(led_count, led_pin)
        self.strip.begin()
        self.clear()

    def run(self) -> None:
        while True:
            state = self.queue.get()
            if not isinstance(state, int):
                raise ProcessError("Illegal IPC-Message. Restart Lightstrip-Process....")
            else:
                self.loading(state)

    # Laedt Ladebalkenmuster auf
    def loading(self, counter):
        for i in range(self.strip.numPixels()):
            if i < (3 * counter):
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
    def __del__(self):
        self.clear()
        del self.strip

