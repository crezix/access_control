from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep


class WebController:
    def __init__(self):
        # webdriver
        self.chrome_options = Options()
        self.chrome_options.add_argument("kiosk")
        self.chrome_options.add_argument("disable-infobars")
        self.chrome_options.add_experimental_option(
            "useAutomationExtension", False)
        self.chrome_options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        self.driver = webdriver.Chrome(options=self.chrome_options)

        self.idleLoc = "file:///home/pi/Desktop/Face-Mask-Detection/web/idle.html"
        self.indexLoc = "file:///home/pi/Desktop/Face-Mask-Detection/web/index.html"

    def loadIdlePage(self):
        self.driver.get(self.idleLoc)

    def loadMainPage(self):
        self.driver.get(self.indexLoc)

    def changeVideo(self, video):
        cmd = "document.getElementById('vidmp4').src='"+video+"'"
        self.driver.execute_script(cmd)
        self.driver.execute_script(
            "document.getElementsByTagName('video')[0].load()")

    def changeProgress(self, text):
        cmd = "document.getElementById('progress').innerText='"+text+"'"
        self.driver.execute_script(cmd)

    def measuringTemperature(self):
        self.loadMainPage()
        self.changeProgress('Measuring Temperature!')

    def preRecognizingMask(self, temperature):
        cmd = "document.getElementById('temp').innerText=%d" % (temperature)
        self.driver.execute_script(cmd)
        self.changeVideo('./face_id.mp4')
        self.changeProgress('Hold Still to capture !')

    def recognizingMask(self):
        cmd = "document.getElementsByTagName('video')[0].style.display='none'"
        self.driver.execute_script(cmd)
        cmd = "document.getElementById('face').style.display='block'"
        self.driver.execute_script(cmd)
        cmd = "document.getElementById('face').src ='./face.jpg'"
        self.driver.execute_script(cmd)
        self.changeProgress('Recognizing Mask!')

    def preSanitizing(self):
        self.changeVideo('./sanitize.mp4')
        self.changeProgress('Put your palms to the sanitizer!')

    def sanitizing(self):
        self.changeVideo('./sanitize.mp4')
        self.changeProgress('Sanitizing...!')

    def noMask(self):
        cmd = "document.getElementsByTagName('video')[0].style.display='block'"
        self.driver.execute_script(cmd)
        cmd = "document.getElementById('face').style.display='none'"
        self.driver.execute_script(cmd)
        self.changeVideo('./mask_not_detected.mp4')
        self.changeProgress('Mask is not detected!')

    def maskRecognized(self):
        cmd = "document.getElementsByTagName('video')[0].style.display='block'"
        self.driver.execute_script(cmd)
        cmd = "document.getElementById('face').style.display='none'"
        self.driver.execute_script(cmd)
        self.driver.execute_script(
            "document.getElementById('mask').src='./checked.png'")

    def sanitized(self):
        self.driver.execute_script(
            "document.getElementById('sanitize').src='checked.png'")
        self.changeProgress('You can go in!')

    def highTemperature(self):
        self.changeProgress('Temperature is over the limit!')

    def errorDetected(self, error):
        self.changeProgress('Err! - ' + error)

    def refresh(self):
        self.driver.refresh()
