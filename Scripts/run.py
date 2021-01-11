from Inputs import measureTemp,detectHand,sanitizeTime,doorTime
from Outputs import rejectI,successI,captureL,sanitizeL,temperatureL,pump
from DetectMask import detectMask
from LoadModels import loadModels
import WebController
from time import sleep

errorCount = 0


net,model = loadModels()
webController = WebController.WebController()

while True:
    webController.loadIdlePage()
    temperature,tempStatus = measureTemp(36,webController)
    if(tempStatus==-1):
        sleep(5)
        continue
    elif(tempStatus):
        maskStatus = detectMask(net,model,webController,temperature)
        if(maskStatus==-1):
            sleep(5)
            continue
        elif(maskStatus):
            #sanitizingDuration = sanitizeTime()
            #sleepingDuration = doorTime()
            sanitizingDuration =5
            sleepingDuration = 5
            handDetected = detectHand(5)
            if(handDetected==-1):
                sleep(5)
                continue
            elif(handDetected):
                pump(sanitizingDuration,sleepingDuration,webController)
            continue
        else:
            sleep(2)
            continue
    else:
        sleep(2)
        continue

