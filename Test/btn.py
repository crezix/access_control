from gpiozero import Button
human_presence = Button(17)
hand = Button(27)

human_presence.wait_for_press()
print('pressed')