from Inputs import measureTemp, detectHand, sanitizeTime, doorTime
from Outputs import rejectI, successI, captureL, sanitizeL, temperatureL, pump
from DetectMask import detectMask
from LoadModels import loadModels
from osCommands import emergShutdown, emergReboot, create
import WebController
from time import sleep
import faulthandler
import threading
import queue

errorCount = 0

webController = WebController.WebController()
webController.loadIdlePage()
net, model = loadModels()

faulthandler.enable()


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
            sanitizeL(True)
            handDetected = detectHand(5, webController)
            sanitizeL(False)
            if (handDetected == -1):
                errorCount += 1
                sleep(5)
                webController.loadIdlePage()
                continue
            elif (handDetected):
                t1 = threading.Thread(
                    target=sanitizeTime, args=(webController))
                t2 = threading.Thread(
                    target=doorTime, args=(webController))
                t1.start()
                t2.start()
                t1.join()
                t2.join()
            webController.loadIdlePage()
            continue
        else:
            rejectI(True)
            sleep(2)
            rejectI(False)
            webController.loadIdlePage()
            continue
    else:
        rejectI(True)
        sleep(2)
        rejectI(False)
        webController.loadIdlePage()
        continue
