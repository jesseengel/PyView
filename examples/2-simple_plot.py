import pyview as pv
import operator

# Create a model
class model:
    def __init__(self):
        self.first = 1
        self.second = 2
        self.op = 'add'

        self.count = 0
        self.ind = []
        self.result = []

    def do_it(self):
        if self.op == 'add':
            res = operator.add(self.first, self.second)
        elif self.op == 'subtract':
            res = operator.sub(self.first, self.second)

        self.count += 1
        self.ind.append(self.count)
        self.result.append(res)

        print('{0} {1} {2} = {3}'.format(self.first, self.op, self.second, res))
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


