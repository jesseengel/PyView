import pyview as pv
import operator

# Create a model
class model:
    def __init__(self):
        self.first = 1.0
        self.second = 2.0
        self.result = 3.0
        self.op = 'add'

    def do_it(self):
        if self.op == 'add':
            self.result = operator.add(self.first, self.second)
        elif self.op == 'subtract':
            self.result = operator.sub(self.first, self.second)
        
        print('{0} {1} {2} = {3}'.format(self.first, self.op, self.second, self.result))
        pv.update()


# Create a view
textctrl_first = pv.TextCtrl('first', label='First', dtype=float)
textctrl_second = pv.TextCtrl('second', label='Second', dtype=float)
textctrl_result = pv.TextCtrl('result', label='Result', dtype=float)

button_do_it = pv.Button('do_it', label='Do it!')
combo_op = pv.ComboBox('op', item_list=['add', 'subtract'], label='Operation:')

view = pv.View([[textctrl_first, textctrl_second, textctrl_result],
                [combo_op],
                [button_do_it]], 
                title='Small Calculator')

# Run the program
pv.run(model, view)


