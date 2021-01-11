import cv2
from tensorflow.keras.models import load_model

#modules
prototxtPath = "/home/pi/Desktop/Face-Mask-Detection/face_detector/deploy.prototxt"
weightsPath = "/home/pi/Desktop/Face-Mask-Detection/face_detector/res10_300x300_ssd_iter_140000.caffemodel"
net = cv2.dnn.readNet(prototxtPath, weightsPath)
model = load_model('/home/pi/Desktop/Face-Mask-Detection/mask_detector.model')

def loadModels():
    return net,model