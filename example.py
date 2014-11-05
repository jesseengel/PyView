import pyview as pv

def test(text):
	print text

text = ''

textctrl_text = pv.TextCtrl(text)
button_test = pv.Button(test)

view = pv.View([[textctrl_text], button_test])

pv.run()


