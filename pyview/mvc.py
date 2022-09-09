import wx

try:
    from wx.lib.pubsub import Publisher as pub
except ImportError:
    from wx.lib.pubsub import pub

import numpy as np
from threading import Thread

from pyview import widgets

###### PYVIEW CLASSES ######

class View(wx.Frame):
    """An object to quickly construct a GUI view from a list of pyview objects"""
    def __init__(self, obj_list, title='Awesome Program'):
        self.app = wx.App(False)
        wx.Frame.__init__(self, None, -1, title)
        self.obj_list = np.array(obj_list)
        self.__create_main_panel()

    def __create_main_panel(self):
        self.panel = wx.Panel(self)

 
        ### Create the elements ###
        for row in self.obj_list:
            for obj in row:
                obj._inherit(self.panel)
                setattr(self, obj.name, obj)

                # Add a label for TextCtrl and ComboBox objects
                if isinstance(obj, (widgets.TextCtrl, widgets.ComboBox)):
                    setattr(self, obj.label_name, wx.StaticText(self.panel, label=obj.label))

        
        ### Arrange the elements ###
        
        #Add(parent, porportion, flags=...) 
        std_flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT | wx.EXPAND

        self.vbox = wx.BoxSizer(wx.VERTICAL)
        
        for i, row in enumerate(self.obj_list):
            row_name = 'hbox_%d' % i
            setattr(self, row_name, wx.BoxSizer(wx.HORIZONTAL))

            for obj in row:
                if isinstance(obj, widgets.TextCtrl):
                    getattr(self, row_name).Add(getattr(self, obj.label_name), border=5, flag=std_flag)
                    getattr(self, row_name).Add(getattr(self, obj.name), border=5, flag=std_flag)

                if isinstance(obj, widgets.ComboBox):
                    getattr(self, row_name).Add(getattr(self, obj.label_name), border=5, flag=std_flag)
                    getattr(self, row_name).Add(getattr(self, obj.name), border=5, flag=std_flag)

                if isinstance(obj, widgets.Button):
                    getattr(self, row_name).Add(getattr(self, obj.name), border=5, flag=std_flag)

                if isinstance(obj, widgets.Plot):
                    # hbox_name = 'hbox_'+obj.name
                    # vbox_name = 'vbox_'+obj.name
                    # setattr(self, hbox_name, wx.BoxSizer(wx.HORIZONTAL))
                    # setattr(self, vbox_name, wx.BoxSizer(wx.VERTICAL))

                    getattr(self, row_name).Add(getattr(self, obj.name).canvas, 1, flag=wx.LEFT | wx.TOP | wx.GROW)
                    # getattr(self, vbox_name).Add(getattr(self, obj.name).toolbar, 1, flag=wx.CENTER | wx.EXPAND)
                    # getattr(self, hbox_name).Add(getattr(self, vbox_name))
                    # getattr(self, row_name).Add(getattr(self, hbox_name))


            self.vbox.Add(getattr(self, row_name), 0, flag=wx.ALIGN_LEFT | wx.TOP | wx.EXPAND)

        # Make it Fit
        self.panel.SetSizer(self.vbox)
        self.vbox.Fit(self)
    


    
class Controller(object):
    """An object made by run() that links the view to the methods and attributes 
    of the model"""
    def __init__(self, model, view, single_threaded=True):

        self.model = model
        self.view = view

        self.worker = None
        self.single_threaded = single_threaded

        ### PUB SUBSCRIBE ###
        pub.subscribe(self.update_view, 'update_view')
        pub.subscribe(self.thread_finished, 'thread_finished')
        pub.sendMessage('update_view')

        ### BINDINGS ###
        for row in self.view.obj_list:
            for obj in row:
                obj._bind(self)

        ### RUN ###
        self.view.Show()
        print('Program Finished Loading!')

    ### BINDING FUNCS ###
    def bind_method(self, event, obj):
        # Only one thread at a time
        if self.worker and obj.single_threaded:
            pass
        else:
	        program_name = obj.func_name
	        self.run_program(program_name)

    def run_program(self, program_name=''):
        #Create and run thread
        self.worker = WorkerThread(self.model, program_name)
        self.worker.start()      

    def bind_value(self, event, obj):
        setattr(self.model, obj.var_name, obj.dtype(obj.GetValue()))

    ### PUB FUNCS ###
    def update_view(self):
        """Update all view elements upon receiving "update_view" pub message.
        """
        for row in self.view.obj_list:
            for obj in row:
                obj._update(self.model)

    def thread_finished(self):
        """Kill the active thread upon receiving "thread_finished" pub message.
        BUG: Doesn't currently join (Kill) the thread, not a fatal bug, but accumulates...
        """
        # self.worker.join()
        self.worker = None
        self.want_to_abort = False


class WorkerThread(Thread):
    '''
    WorkerThread:
        Runs the model methods in a multithreaded manner.
    '''
    def __init__(self, model, program_name):
        Thread.__init__(self)
        self.model = model
        self.program_name = program_name
            
    def run(self):
        if hasattr(self.model, self.program_name):
            getattr(self.model, self.program_name)()
        #Terminate when done        
        pub.sendMessage('thread_finished')



###### PYVIEW FUNCTIONS ######

def run(model, view):
    '''Run the pyview program'''

    #Check if model is an instantiation of the class
    try:
        if not isinstance(model, model):
            model = model()
    except TypeError:
        print('\nModel must be a class, not module\n')
        raise

    controller = Controller(model, view)
    view.app.MainLoop()


def update():
    pub.sendMessage('update_view')

def abort():
    pub.sendMessage('thread_finished')
