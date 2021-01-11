from gpiozero import DigitalInputDevice
from signal import pause
from smbus2 import SMBus
from mlx90614 import MLX90614
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn



def measureTemp(limit,webController):
    webController.measuringTemperature()
    try:
        i2c = busio.I2C(board.SCL, board.SDA)# Create the I2C bus
        ads = ADS.ADS1015(i2c)# Create the ADC object using the I2C bus
        bus = SMBus(1)#SMBus for Temperature Sensor
        sharpIR = AnalogIn(ads, ADS.P0)# Create single-ended input on channel 0 - Sharp IR
        tempSensor = MLX90614(bus, address=0x5A)#Temperature Sensor - I2c
        while True:
            if(sharpIR.value>18000):
                temperature = tempSensor.get_object_1()
                bus.stop()
                if(temperature>limit):
                    webController.highTemperature()
                    return (temperature,False)
                    break
                else:
                    return (temperature,True)
                    break
    except:
        webController.errorDetected('code:T01')
        return (-1,-1)
            
def detectHand(timeout,webController):
    try:
        sanitizerPIR = DigitalInputDevice(27)
        if(sanitizerPIR.wait_for_active(timeout=timeout)):
            return True
        else:
            return False
    except:
        webController.errorDetected('code: P01')
        return -1

def sanitizeTime():
    try:
        i2c = busio.I2C(board.SCL, board.SDA)# Create the I2C bus
        ads = ADS.ADS1015(i2c)# Create the ADC object using the I2C bus
        sanitizeTimer = AnalogIn(ads, ADS.P1)# Create single-ended input on channel 0 - Pot 01
        value = sanitizeTimer.value
        timeInSeconds = value
        return timeInSeconds
    except:
        return -1
    
def doorTime():
    try:
        i2c = busio.I2C(board.SCL, board.SDA)# Create the I2C bus
        ads = ADS.ADS1015(i2c)# Create the ADC object using the I2C bus
        doorTimer = AnalogIn(ads, ADS.P2)# Create single-ended input on channel 0 - pot 02
        value = doorTimer.value
        timeInSeconds = value
        return timeInSeconds
    except:
        return -1