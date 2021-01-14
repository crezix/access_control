from Inputs import measureTemp, detectHand, sanitizeTime, doorTime
from Outputs import rejectI, successI, captureL, sanitizeL, temperatureL, pump
from DetectMask import detectMask
from LoadModels import loadModels
from osCommands import emergShutdown, emergReboot, create
import WebController
from time import sleep

errorCount = 0

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
            sanitizingDuration = sanitizeTime(webController)
            doorDuration = doorTime(webController)
            #sanitizingDuration = 5
            #sleepingDuration = 5
            sanitizeL(True)
            handDetected = detectHand(5, webController)
            sanitizeL(False)
            if (handDetected == -1):
                errorCount += 1
                sleep(5)
                continue
            elif(handDetected):
                pump(sanitizingDuration, webController)
                successI(doorDuration, webController)
            continue
        else:
            rejectI(True)
            sleep(2)
            rejectI(False)
            continue
    else:
        rejectI(True)
        sleep(2)
        rejectI(False)
        continue
