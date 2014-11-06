import pyview as pv

# Create a model
class model:
    def __init__(self):
        self.first = 1
        self.second = 2
        self.result = 3
        self.op = 'add'

    def add(self):
        self.result = float(self.first) + float(self.second)
        print self.result

    def subtract(self):
        self.result = float(self.first) - float(self.second)
        print self.result

    def do_it(self):
        if self.op == 'add':
            self.add()
        elif self.op == 'subtract':
            self.subtract()
        pv.update_view()


# Create a view
textctrl_first = pv.TextCtrl('first', label='First')
textctrl_second = pv.TextCtrl('second', label='Second')
textctrl_result = pv.TextCtrl('result', label='Result')
button_do_it = pv.Button('do_it', label='Do it!')
combo_op = pv.ComboBox('op', item_list=['add', 'subtract'], label='Operation:')

view = pv.View([[textctrl_first, textctrl_second, textctrl_result],
                [combo_op],
                [button_do_it]], title='Small Calculator')

# Run the program
pv.run(model, view)


