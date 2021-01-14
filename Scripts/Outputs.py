from gpiozero import DigitalOutputDevice
from time import sleep


# outputs
rejectIndicator = DigitalOutputDevice(17, initial_value=True)
successIndicator = DigitalOutputDevice(22, initial_value=True)
captureLight = DigitalOutputDevice(27, initial_value=True)
sanitizerLight = DigitalOutputDevice(25)
temperatureLight = DigitalOutputDevice(23)
pumpRelay = DigitalOutputDevice(24, initial_value=True)


def rejectI(state):
    if(state):
        rejectIndicator.off()
    else:
        rejectIndicator.on()


def captureL(state):
    if(state):
        captureLight.off()
    else:
        captureLight.on()


def sanitizeL(state):
    if(state):
        sanitizerLight.blink(on_time=0.5, off_time=0.5)
    else:
        sanitizerLight.off()


def temperatureL(state):
    if(state == 1):
        temperatureLight.on()
    elif (state == 2):
        temperatureLight.blink(on_time=0.5, off_time=0.5)
    else:
        temperatureLight.off()


def pump(pumpingTime, webController):
    webController.sanitizing()
    pumpRelay.off()
    sleep(pumpingTime)
    pumpRelay.on()
    webController.sanitized()


def successI(doorTime, webController):
    # webController.sanitizing()
    successIndicator.off()
    sleep(doorTime)
    successIndicator.on()
    # webController.sanitized()
