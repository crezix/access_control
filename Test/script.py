from gpiozero import Button, DigitalOutputDevice, DigitalInputDevice
from signal import pause
import time
import cv2
from tensorflow.keras.models import load_model
from detect_mask_image import mask_image
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from smbus2 import SMBus
from mlx90614 import MLX90614
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

#Sharp IR sensor
# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1015(i2c)

# Create single-ended input on channel 0
chan = AnalogIn(ads, ADS.P0)

#webdriver
chrome_options = Options()
chrome_options.add_argument("kiosk")
chrome_options.add_argument("disable-infobars")
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_experimental_option(
    "excludeSwitches", ["enable-automation"])
driver = webdriver.Chrome(options=chrome_options)

#modules
print("Loading Modules...")
prototxtPath = "/home/pi/Desktop/Face-Mask-Detection/face_detector/deploy.prototxt"
weightsPath = "/home/pi/Desktop/Face-Mask-Detection/face_detector/res10_300x300_ssd_iter_140000.caffemodel"
net = cv2.dnn.readNet(prototxtPath, weightsPath)
model = load_model('/home/pi/Desktop/Face-Mask-Detection/mask_detector.model')
print("Modules Loaded!")

#inputs
bus = SMBus(1)
sensor = MLX90614(bus, address=0x5A)
human_presence = Button(17)
sanitizer_pir = DigitalInputDevice(27)
relay = DigitalOutputDevice(14)
sanitizing_time = 5


def measure_temp():
    while True:
        st = time.time()
        if(chan.value>18000):
            print('Measure Temp')
            driver.execute_script("document.getElementById('progress').innerText='Measuring Temperature'")
            temp = (sensor.get_object_1())
            temp_script ="document.getElementById('temp').innerText=%d"%(temp)
            et = time.time()
            if(temp < 38.0):
                driver.execute_script(temp_script)
                print('Temperature Measuring Time :', et-st, 's')
                return True
                break
            else:
                driver.execute_script(temp_script)
                print('Temperature Measuring Time :', et-st, 's')
                return False
                break


def mask_recognition(net, model):
    print('Recognizing mask')
    driver.execute_script(
        "document.getElementById('progress').innerText='Recognizing Mask'")
    driver.execute_script(
        "document.getElementById('vidmp4').src='./face_id.mp4'")
    driver.execute_script("document.getElementsByTagName('video')[0].load()")
    st = time.time()
    masked = mask_image(net, model)
    et = time.time()
    if(masked):
        print('Mask Recognizing Time :', et-st, 's')
        driver.execute_script(
            "document.getElementById('mask').src='./face.jpg'")
        return True
    else:
        print('Mask Recognizing Time :', et-st, 's')
        driver.execute_script(
            "document.getElementById('mask').src='./face.jpg'")
        driver.execute_script("document.getElementById('progress').innerText='Recognizing Mask'")
        driver.execute_script("document.getElementById('vidmp4').src='./mask_not_detected.mp4'")
        driver.execute_script("document.getElementsByTagName('video')[0].load()")
        return False


def sanitize():
    print('Sanitizing')
    driver.execute_script(
        "document.getElementById('progress').innerText='Sanitizing'")
    relay.on()
    time.sleep(sanitizing_time)
    relay.off()
    driver.execute_script(
        "document.getElementById('sanitize').src='./checked.png'")


while True:
    driver.get(
        "file:///home/pi/Desktop/Face-Mask-Detection/web/idle.html")
    human_presence.wait_for_press()
    driver.get(
        "file:///home/pi/Desktop/Face-Mask-Detection/web/index.html")
    driver.execute_script(
        "document.getElementById('vidmp4').src='./welcome.mp4'")
    driver.execute_script("document.getElementsByTagName('video')[0].load()")
    time.sleep(2)
    driver.execute_script("document.getElementById('progress').innerText='Put Your wrist to temperature Sensor'")
    driver.execute_script(
        "document.getElementById('vidmp4').src='./temperature.mp4'")
    driver.execute_script("document.getElementsByTagName('video')[0].load()")
    
    try:
        if(measure_temp()):
            if(mask_recognition(net, model)):
                driver.execute_script("document.getElementById('vidmp4').src='./sanitize.mp4'")
                driver.execute_script("document.getElementsByTagName('video')[0].load()")
                sanitizer_pir.wait_for_active()
                sanitize()
                print('You can go in!')
                time.sleep(2)
                continue
            else:
                print('Access Denied!')
                time.sleep(4)
                continue
        else:
            continue
    except:
        driver.execute_script( "document.getElementById('progress').innerText='Something went wrong! Try Again'")
        time.sleep(2)
        continue
