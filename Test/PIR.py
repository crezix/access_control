from gpiozero import DigitalInputDevice
sanitizer_pir = DigitalInputDevice(27)

while True:
    sanitizer_pir.wait_for_active()
    print('detected')