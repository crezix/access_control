from gpiozero import DigitalOutputDevice, LED
from time import sleep


# outputs
rejectIndicator = DigitalOutputDevice(17, initial_value=True)
successIndicator = DigitalOutputDevice(22, initial_value=True)
captureLight = DigitalOutputDevice(27, initial_value=True)
sanitizerLight = LED(25, initial_value=False)
temperatureLight = LED(23, initial_value=True)
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
        sanitizerLight.off()
    else:
        sanitizerLight.on()


def temperatureL(state):
    if(state == 1):
        temperatureLight.off()
    elif (state == 2):
        temperatureLight.blink(on_time=0.5, off_time=0.5)
    else:
        temperatureLight.on()


def pump(pumpingTime, webController):
    try:
        webController.sanitizing()
        pumpRelay.off()
        sleep(pumpingTime)
        pumpRelay.on()
        webController.sanitized()
    except:
        webController.errorDetected('code:PM01')


def successI(doorTime, webController):
    try:
        # webController.sanitizing()
        successIndicator.off()
        sleep(doorTime)
        successIndicator.on()
        # webController.sanitized()
    except:
        webController.errorDetected('code:D01')
