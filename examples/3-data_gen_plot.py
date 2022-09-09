import time

import numpy as np
import pyview as pv

# Create a model
class Model:
    def __init__(self):
        self.want_to_abort = False
        self.count = 0
        self.ind = []
        self.result = []


    def start(self):
        self.want_to_abort = False

        while True:
            self.count += 1
            self.ind.append( self.count )
            self.result.append( np.random.randn(1) )

            pv.update()

            time.sleep(0.1)
            if self.want_to_abort: break


    def stop(self):
        self.want_to_abort = True



# Create a view
axes_params = dict(ylabel='Magnitude',
				   xlabel='Data Point #',
				   title='Data Generator')
plot = pv.Plot(x='ind', y='result', plot_type='plot', axes_params=axes_params)

button_start = pv.Button('start', label='Start!')
button_stop = pv.Button('stop', label='Stop', single_threaded=False)

view = pv.View([[plot],
                [button_start, button_stop]], title='Random Data!')

model = Model()

# Run the program
pv.run(model, view)


