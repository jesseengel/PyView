import wx

import matplotlib
matplotlib.use('WXAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas, \
    NavigationToolbar2WxAgg as NavigationToolbar

import numpy as np
import pylab


###### WXPYTHON WIDGET CLASSES ######

class Button(wx.Button):
    """Extension of the Button Widget.
    Bind to function 'func' and run every time the button is pushed."""
    def __init__(self, func_name, label='', single_threaded=True):
        self.func_name = func_name
        self.single_threaded = single_threaded

        self.label = label
        self.name = ('button_'+self.label).replace(' ', '_')
        self.label_name = ('label_'+self.label).replace(' ', '_')

    def _inherit(self, parent):
        wx.Button.__init__(self, parent, label=self.label)

    def _bind(self, controller):
        self.Bind( wx.EVT_BUTTON, lambda event, obj=self: controller.bind_method(event, self) )

    def _update(self, model):
        pass

class ComboBox(wx.ComboBox):
    """Extension of the ComboBox Widget.
    Bind to 'var' and update every time new option selected."""
    def __init__(self, var_name, item_list, label='', dtype=str):
        self.var_name = var_name
        self.item_list = item_list

        self.label = label
        self.name = ('combo_'+self.label).replace(' ', '_')
        self.label_name = ('label_'+self.label).replace(' ', '_')
        self.dtype = dtype

    def _inherit(self, parent):
        wx.ComboBox.__init__(self, parent, style=wx.CB_READONLY)
        str_list = []
        for item in self.item_list:
            str_list.append(str(item))
        self.AppendItems(str_list)

    def _bind(self, controller):
        self.Bind( wx.EVT_COMBOBOX, lambda event, obj=self: controller.bind_value(event, self) )

    def _update(self, model):
        self.SetValue( str( getattr(model, self.var_name) ) )


class TextCtrl(wx.TextCtrl):
    """Extension of the TextCtrl.
    Bind to variable 'var' and update every time new value entered."""
    def __init__(self, var_name, label='', dtype=str):
        self.var_name = var_name

        self.label = label
        self.name = ('textctrl_'+self.label).replace(' ', '_')
        self.label_name = ('label_'+self.label).replace(' ', '_')
        self.dtype = dtype
       
    def _inherit(self, parent):
        wx.TextCtrl.__init__(self, parent, value='', style=wx.TE_PROCESS_ENTER)

    def _bind(self, controller):
        self.Bind( wx.EVT_TEXT, lambda event, obj=self: controller.bind_value(event, self) )
        self.Bind( wx.EVT_TEXT_ENTER, lambda event, obj=self: controller.bind_value(event, self) )

    def _update(self, model):
        self.SetValue( str( getattr(model, self.var_name) ) )



class Plot(object):
    def __init__(self, x='', y='', plot_type='plot', axes_params=None, dimensions=(6.0,5.0), dpi=100 ):
        """ Self updating plot """
        self.plot_type = plot_type
        self.name = 'plot_'+x+'_'+y
        self.x = x
        self.y = y

        self.fig = Figure(dimensions, dpi=dpi)
        self.axes = self.fig.add_subplot(111)

        if axes_params is None:
            axes_params = dict(title='Awesome graph',
                               xlabel='X',
                               ylabel='Y')

        # self.canvas.mpl_connect('pick_event', self.on_pick)
        
        # Create the navigation toolbar, tied to the canvas
        # pylab.setp(self.axes.get_xticklabels(), fontsize=8)
        # pylab.setp(self.axes.get_yticklabels(), fontsize=8)

        # plot the data as a line series, and save the reference 
        # to the plotted line series
        
        self.plot_data = getattr(self.axes, plot_type)(np.array([]), 'yo-')[0]

        # anecdote: axes.grid assumes b=True if any other flag is
        # given even if b is set to False.
        # so just passing the flag into the first statement won't
        # work.
        
        if 'log' in self.plot_type:
            self.axes.yaxis.grid(b=True, which='minor', color=(.2,.2,.2), linestyle=':')
            self.axes.grid(b=True, which='major', color='gray', linestyle=':')
            self.axes.minorticks_on()
        else:
            self.axes.grid(b=True, which='major', color='gray')
        pylab.setp(self.axes, facecolor=[.05,.05,.05])

        # self.axes.grid(True, color='gray')
        # Using setp here is convenient, because get_xticklabels
        # returns a list over which one needs to explicitly 
        # iterate, and setp already handles this.
         
        pylab.setp(self.axes.get_xticklabels(), visible=True)
        pylab.setp(self.axes, **axes_params)
        # pylab.tight_layout()

    def _inherit(self, parent):
        self.parent = parent
        self.canvas = FigCanvas(self.parent, -1, self.fig)
        # self.toolbar = NavigationToolbar(self.canvas)

    def _bind(self, controller):
        pass

    def _update(self, model):
        self.draw( getattr(model, self.x), getattr(model, self.y))

    def draw(self, x, y):
        """ Redraws the plot
        """
        x = np.array(x)
        y = np.array(y)

        if x.size and y.size:
            if 'log' in self.plot_type:
                try:
                    ymin = round(np.min(y[y>0]), 0) - 1
                except ValueError:
                    ymin = 1
            else:
                ymin = round(np.min(y), 0) - 1

            ymax = round(np.max(y), 0) + 1
            xmin = round(np.min(x), 0) - 1
            xmax = round(np.max(x), 0) + 1


            self.axes.set_xbound(lower=xmin, upper=xmax)
            self.axes.set_ybound(lower=ymin, upper=ymax)
            
            self.plot_data.set_xdata(x)
            self.plot_data.set_ydata(y)
            
            try:
                self.canvas.draw()
            except ValueError:
                print('Woops!\nSome drawing SNAFU happened.\n')


