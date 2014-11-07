import pyview as pv

# Create a model
class model:
    def __init__(self):
        self.first = 1
        self.second = 2
        self.op = 'add'

        self.count = 0
        self.ind = []
        self.result = []



    def add(self):
        return float(self.first) + float(self.second)

    def subtract(self):
        return float(self.first) - float(self.second)

    def do_it(self):
        if self.op == 'add':
            res = self.add()
        elif self.op == 'subtract':
            res = self.subtract()

        print res

        self.count += 1
        self.ind = range(self.count)
        self.result.append(res)

        pv.update()


# Create a view
axes_params = dict(ylabel='Magnitude (V or A)',
				   xlabel='Pulse #',
				   title='Pulse Magnitudes')

plot = pv.Plot('ind', 'result', 'plot', axes_params=axes_params) 

textctrl_first = pv.TextCtrl('first', label='First')
textctrl_second = pv.TextCtrl('second', label='Second')

button_do_it = pv.Button('do_it', label='Do it!')
combo_op = pv.ComboBox('op', item_list=['add', 'subtract'], label='Operation:')

view = pv.View([[plot],
				[textctrl_first, textctrl_second],
                [combo_op],
                [button_do_it]], title='Small Graph Calculator')

# Run the program
pv.run(model, view)


