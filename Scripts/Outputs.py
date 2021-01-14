from gpiozero import DigitalOutputDevice
from time import sleep


# outputs
rejectIndicator = DigitalOutputDevice(17)
successIndicator = DigitalOutputDevice(22)
captureLight = DigitalOutputDevice(27)
sanitizerLight = DigitalOutputDevice(18)
temperatureLight = DigitalOutputDevice(23)
pumpRelay = DigitalOutputDevice(24)
pumpRelay.on()


def rejectI(state):
    if(state):
        rejectIndicator.off()
    else:
        rejectIndicator.on()


def successI(state):
    if(state):
        successIndicator.off()
    else:
        successIndicator.on()


def captureL(state):
    if(state):
        captureLight.off()
    else:
        captureLight.on()


def sanitizeL(state):
    if(state):
        sanitizerLight.on()
    else:
        sanitizerLight.off()


def temperatureL(state):
    if(state == 1):
        temperatureLight.on()
    elif (state == 2):
        temperatureLight.blink(on_time=0.5, off_time=0.5)
    else:
        temperatureLight.off()


def pump(pumpingTime, sleepingTime, webController):
    webController.sanitizing()
    pumpRelay.off()
    sleep(pumpingTime)
    pumpRelay.on()
    webController.sanitized()
    sleep(sleepingTime)
