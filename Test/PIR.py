from gpiozero import DigitalInputDevice, DigitalOutputDevice
from time import sleep
sanitizer_pir = DigitalInputDevice(27)
pumpRelay = DigitalOutputDevice(24, initial_value=True)

while True:
    sanitizer_pir.wait_for_inactive()
    pumpRelay.off()
    sleep(5)
    pumpRelay.on()
