from gpiozero import DigitalInputDevice,DigitalOutputDevice
from time import sleep

button = DigitalOutputDevice(25)
button.on()
sleep(2)
button.off()
print('ok')