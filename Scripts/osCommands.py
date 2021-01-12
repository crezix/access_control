import os


def emergShutdown():
    try:
        reboot_log = open("reboot.log", 'r')
        reboot_count = int(reboot_log.read())
        reboot_log.close()
        if (reboot_count > 3):
            reboot_log = open("reboot.log", 'w')
            reboot_log.write('0')
            reboot_log.close()
            os.system("sudo shutdown now")
    except:
        None


def emergReboot():
    try:
        reboot_log = open("reboot.log", 'r')
        reboot_count = int(reboot_log.read())
        reboot_log.close()
        reboot_log = open("reboot.log", 'w')
        reboot_log.write(str(reboot_count+1))
        reboot_log.close()
        os.system("sudo reboot")
    except:
        None
