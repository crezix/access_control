from Inputs import measureTemp, detectHand, sanitizeTime, doorTime
from Outputs import rejectI, successI, captureL, sanitizeL, temperatureL, pump
from DetectMask import detectMask
from LoadModels import loadModels
from osCommands import emergShutdown, emergReboot, create
import WebController
from time import sleep
import faulthandler
import threading


webController = WebController.WebController()
webController.loadIdlePage()
net, model = loadModels()

faulthandler.enable()


def main(targ):
    errorCount = 0
    while True:
        if (errorCount > 2):
            break
        temperatureL(2)
        temperature, tempStatus = measureTemp(36, webController)
        temperatureL(3)
        if (tempStatus == -1):
            errorCount += 1
            sleep(5)
            webController.loadIdlePage()
            continue
        elif (tempStatus):
            maskStatus = detectMask(net, model, webController, temperature)
            if (maskStatus == -1):
                errorCount += 1
                sleep(5)
                webController.loadIdlePage()
                continue
            elif(maskStatus):
                # sanitizingDuration = 5
                # sleepingDuration = 5
                # sanitizeL(True)
                handDetected = detectHand(5, webController)
                # sanitizeL(False)
                if (handDetected == -1):
                    errorCount += 1
                    sleep(5)
                    webController.loadIdlePage()
                    continue
                elif (handDetected):
                    sanitizingDuration = sanitizeTime(webController)
                    doorDuration = doorTime(webController)
                    if (sanitizingDuration == -1):
                        sanitizingDuration = 2.5
                    if (doorDuration == -1):
                        doorDuration = 5
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


main(0)
