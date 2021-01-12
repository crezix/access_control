from Inputs import measureTemp, detectHand, sanitizeTime, doorTime
from Outputs import rejectI, successI, captureL, sanitizeL, temperatureL, pump
from DetectMask import detectMask
from LoadModels import loadModels
from osCommands import emergShutdown, emergReboot
import WebController
from time import sleep

net, model = loadModels()
webController = WebController.WebController()

while True:
    errorCount = 0
    if (errorCount > 5):
        emergShutdown()
        emergReboot()
    webController.loadIdlePage()
    temperature, tempStatus = measureTemp(36, webController)
    if (tempStatus == -1):
        errorCount += 1
        sleep(5)
        continue
    elif(tempStatus):
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
            handDetected = detectHand(5)
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
