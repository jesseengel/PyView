'''
Plots measurments from an analog pin on an arduino.
Relies on the python library pyFirmata.

installation:
1) open Arduino app and load 'firmata' sketch to your arduino
2) pip install pyFirmata
3) make sure the port in the gui is correct for your device
'''

import time

import numpy as np
import pyfirmata

import pyview as pv

# Create a model
class Model:
    def __init__(self):
        self.want_to_abort = False
        self.count = 0
        self.ind = []
        self.result = []
        self.arduino = None
        self.port = '/dev/tty.usbmodemfd121'

        self.pin = 0
        self.rate = 0.1

    def load_arduino(self):
        self.arduino = pyfirmata.Arduino(self.port)

    def start(self):
        # If there's no board, load one
        if not self.arduino:
            self.load_arduino()

        # Initialize iterator and pin (board communication)
        self.want_to_abort = False
        it = pyfirmata.util.Iterator(self.arduino)
        it.start()
        a_pin = self.arduino.analog[self.pin]
        a_pin.enable_reporting()
        # Allow board time to settle
        time.sleep(0.1)

        while True:
            value = a_pin.read()

            self.count += 1
            self.ind.append( self.count )
            self.result.append(value)

            pv.update()
            time.sleep(self.rate)

            if self.want_to_abort:
                # Shutdown pin and board
                a_pin.disable_reporting()
                self.arduino.exit()
                self.arduino = None
                break

    def stop(self):
        self.want_to_abort = True



# Create a view
axes_params = dict(ylabel='Magnitude',
                   xlabel='Data Point #',
                   title='Analog Pin Value')
plot = pv.Plot(x='ind', y='result', plot_type='plot', axes_params=axes_params)

textctrl_port = pv.TextCtrl('port', label='Port:')
textctrl_rate = pv.TextCtrl('rate', label='Rate (s):', dtype=float)

combo_pin = pv.ComboBox('pin', [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], dtype=int)

button_start = pv.Button('start', label='Start!')
button_stop = pv.Button('stop', label='Stop', single_threaded=False)
button_load_arduino = pv.Button('load_arduino', label='Load')


view = pv.View([[textctrl_port, button_load_arduino],
                [plot],
                [button_start, button_stop],
                [combo_pin, textctrl_rate]],
               title='Arduino Analog-in')

model = Model()

# Run the program
pv.run(model, view)


