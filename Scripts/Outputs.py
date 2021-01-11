from gpiozero import DigitalOutputDevice
from time import sleep


#outputs
rejectIndicator = DigitalOutputDevice(17)
successIndicator = DigitalOutputDevice(22)
captureLight = DigitalOutputDevice(15)
sanitizerLight = DigitalOutputDevice(18)
temperatureLight = DigitalOutputDevice(23)
pumpRelay = DigitalOutputDevice(24)

def rejectI(state):
    if(state):
        rejectIndicator.on()
    else:
        rejectIndicator.off()

def successI(state):
    if(state):
        successIndicator.on()
    else:
        successIndicator.off()

def captureL(state):
    if(state):
        captureLight.on()
    else:
        captureLight.off()

def sanitizeL(state):
    if(state):
        sanitizerLight.on()
    else:
        sanitizerLight.off()

def temperatureL(state):
    if(state):
        temperatureLight.on()
    else:
        temperatureLight.off()

def pump(pumpingTime,sleepingTime,webController):
    webController.sanitizing()
    pumpRelay.on()
    sleep(pumpingTime)
    pumpRelay.off()
    webController.sanitized()
    sleep(sleepingTime)
    
    

