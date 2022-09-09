PyView
======

__Disclaimer: This code is not actively maintained, and will likely develop breaking dependencies. I hope you find it useful as a reference.__


The philosophy behind making PyView is that there should be a good LabView replacement for Python.
NumPy is a great replacement for Matlab, but too many industry and academic research labs are still stuck using LabView because it easily interfaces with hardware and creates GUIs that plot in realtime. 

Many good libraries exist for interfacing python with external hardware, including [PySerial](http://pyserial.sourceforge.net/), [pyFirmata (arduino)](https://github.com/tino/pyFirmata), [pyOSC](https://pypi.python.org/pypi/pyOSC), and [PyVisa](https://pyvisa.readthedocs.org/en/master/) for general communication with lab equipment.

What's lacking is thus an easy frontend to connect a bunch of GUI knobs and sliders and plots to the python backend controlling lab equipment. PyView gives a shot at that under the philosiphy that (similar to LabView), you really want direct 1-1 correspondence of your dials/graphs to the real hardware/measurements. 

PyView uses a Model-View-Controller (MVC) design to provide a wrapper around a GUI library (a "View") (wxPython is currently the only one supported), that binds ("Controller") values easily to python variable in your program ("Model"). I used a similar approach to control a probe station setup in my research at Stanford, and I think there should be a library to write programs where you can easily make GUIs focused on data aquisition. I've since taken a job in computer science, not experimental science, so I don't have a lot of excuse to actively develop this library, but please take a look and hopefully someone will be inspired to carry a similar idea forward and spread it to university labs, because paying thousands of dollars for a labview license it ridiculous and unnecessary in this day and age.

Installation
============

PyView uses wxPython as it's backend. While you can install it manually, it is easiest to install
with conda (anaconda package manager). I recommend getting anaconda from [here](https://store.continuum.io/cshop/anaconda/), and then installing wxpython.

```
	conda update conda
	conda install wxpython
```

From there, The preferred way to install is with [pip](http://www.pip-installer.org/en/latest/)

```
	pip install pyview
```

Obviously the Arduino examples will also require an arduino microcontroller :).

Usage
=====
There are serval examples in the `examples/` directory, including several interfacing to an Arduino.
