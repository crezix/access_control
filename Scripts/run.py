from Inputs import measureTemp, detectHand, sanitizeTime, doorTime
from Outputs import rejectI, successI, captureL, sanitizeL, temperatureL, pump, pumpOff
from DetectMask import detectMask
from LoadModels import loadModels
from osCommands import emergShutdown, emergReboot, create
import WebController
from time import sleep

errorCount = 0
rejectI(False)
successI(False)
captureL(False)
pumpOff()

webController = WebController.WebController()
webController.loadIdlePage()
net, model = loadModels()


while True:
    webController.loadIdlePage()
    if (errorCount > 3):
        break
    temperatureL(2)
    temperature, tempStatus = measureTemp(36, webController)
    temperatureL(3)
    if (tempStatus == -1):
        errorCount += 1
        sleep(5)
        continue
    elif (tempStatus):
        maskStatus = detectMask(net, model, webController, temperature)
        if (maskStatus == -1):
            errorCount += 1
            sleep(5)
            continue
        elif(maskStatus):
            #sanitizingDuration = sanitizeTime()
            #sleepingDuration = doorTime()
            sanitizingDuration = 5
            sleepingDuration = 5
            handDetected = detectHand(5, webController)
            if (handDetected == -1):
                errorCount += 1
                sleep(5)
                continue
            elif(handDetected):
                pump(sanitizingDuration, sleepingDuration, webController)
            continue
        else:
            sleep(2)
            continue
    else:
        sleep(2)
        continue
