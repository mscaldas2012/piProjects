import cwiid
import time

class WiiRemote:
    button_A = 8
    button_B = 4
    button_ONE = 2
    button_TWO = 1

    button_minus = 16
    button_plus = 4096
    button_home = 128

    button_up = 2048
    button_right = 512
    button_down = 1024
    button_left = 256

    wm = None

    def __init__(self):
        print 'Press button 1 + 2 on your Wii Remote...'
        time.sleep(1)

       
        self.wm = cwiid.Wiimote()
        print 'Wii Remote connected...'
        #print '\nPress the PLUS button to disconnect the Wii and end the application'
        time.sleep(1)

        #    Rumble = False
        self.wm.rpt_mode = cwiid.RPT_BTN


    def getButtonState(self):
        return self.wm.state['buttons']
    
    def buttonAPressed(self):
        return self.wm.state['buttons'] == WiiRemote.button_A

    def buttonBPressed(self):
        return self.wm.state['buttons'] == WiiRemote.button_B
            
