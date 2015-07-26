# import core functions
from widgets import *
from mvc import *

# remove external access to internal modules
del widgets, mvc
del Figure, FigCanvas, NavigationToolbar, WorkerThread, Thread, matplotlib, np, pub, pylab, wx

