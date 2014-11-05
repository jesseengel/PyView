import wx

class Button(wx.Button):
	"""Extension of the Button Widget.
	Bind to function 'func' and run every time the button is pushed."""
	def __init__(self, function):
		super(Button, self).__init__()
		self.func = func

class ComboBox(wx.ComboBox):
	"""Extension of the ComboBox Widget.
	Bind to 'var' and update every time new option selected."""
	def __init__(self, variable):
		super(ComboBox, self).__init__()
		self.var = var

class TextCtrl(wx.TextCtrl):
	"""Extension of the TextCtrl.
	Bind to variable 'var' and update every time new val entered."""
	def __init__(self, var):
		super(TextCtrl, self).__init__()
		self.var = var

class Graph(wx.Graph):
	"""An embedded matplotlib graph"""
	def __init__(self, arg):
		super(Graph, self).__init__()
		self.arg = arg

class View(object):
	"""An object to quickly construct a GUI view from a list of pyview objects"""
	def __init__(self, arg):
		self.arg = arg


def run():
	'''Run the pyview program'''
	pass