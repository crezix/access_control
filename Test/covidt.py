from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument("kiosk")
chrome_options.add_argument("disable-infobars")
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_experimental_option(
    "excludeSwitches", ["enable-automation"])
driver = webdriver.Chrome(options=chrome_options)
driver.get(
    "file:///home/pi/Desktop/covid/responsive-background-video/dist/index.html")
sleep(2)
driver.get(
    "file:///home/pi/Desktop/covid/responsive-background-video/dist/temperature.html")
sleep(2)
driver.execute_script(
    "document.getElementById('temp').innerText='Temperature : 30'")
