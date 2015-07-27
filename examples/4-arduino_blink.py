''' 
Blink an LED on a digital pin on an arduino. 
Relies on the python library pyFirmata.

installation:
1) open Arduino app and load 'firmata' sketch to your arduino
2) pip install pyFirmata
3) make sure the port in the gui is correct for your device
'''

import pyview as pv

import pyfirmata
import numpy as np
import time

# Create a model
class model:
    def __init__(self):
        self.want_to_abort = False
        self.count = 0
        self.ind = []
        self.result = []
        self.arduino = None
        self.port = '/dev/tty.usbmodemfd121'

        self.pin = 13
        self.rate = 0.5

    def load_arduino(self):
        self.arduino = pyfirmata.Arduino(self.port)


    def start(self):
        self.want_to_abort = False

        while True:
            self.arduino.digital[self.pin].write(1)
            time.sleep(self.rate)
            self.arduino.digital[self.pin].write(0)
            time.sleep(self.rate)
     
            if self.want_to_abort: break

    def stop(self):
        self.want_to_abort = True



# Create a view
textctrl_port = pv.TextCtrl('port', label='Port:')
textctrl_rate = pv.TextCtrl('rate', label='Rate (s):', dtype=float)

combo_pin = pv.ComboBox('pin', 
                        [0, 1, 2, 3, 4,
                         5, 6, 7, 8, 9,
                         10, 11, 12, 13], 
                        label='Pin:',
                        dtype=int)

button_start = pv.Button('start', label='Start!')
button_stop = pv.Button('stop', label='Stop', single_threaded=False)
button_load_arduino = pv.Button('load_arduino', label='Load', single_threaded=False)


view = pv.View([[textctrl_port, button_load_arduino],
                [button_start, button_stop],
                [combo_pin, textctrl_rate]],
                title='Arduino Blinker')

# Run the program
pv.run(model, view)


