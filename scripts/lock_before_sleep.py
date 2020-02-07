#!/bin/env python3

import dbus
import dbus.mainloop.glib
import os
import time
import subprocess
import gi
import signal
from gi.repository import GLib

# make sure there is just one instance of screenlocker running
# in this case, its handled by the script called
def lock_screen():
    os.system("~/.config/i3/i3lock_customized.sh")  # lock screen

dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)     # integrate into gobject main loop
bus = dbus.SystemBus()
proxy = bus.get_object("org.freedesktop.login1", "/org/freedesktop/login1")
manager = dbus.Interface(proxy, "org.freedesktop.login1.Manager")

def log(txt):
    print("%s -- %s" % (time.time(), txt))

def sigterm_handler(_signo, _stack_frame):
    log("Exit")
    loop.quit()
    GLib.idle_add(quit)

def handle_sleep(mode):
    global lock
    global manager

    if mode:
        log("Lock...")
        lock_screen()
        #os.close(lock.take())                           # tell system we are finished
    else:
        #lock = manager.Inhibit("sleep", "Screenlocker", "Locking screen...", "delay")   # tell system to wait for us next time
        log("Resume")


bus.add_signal_receiver(               # define the signal to listen to
    handle_sleep,                      # callback function
    'PrepareForSleep',                 # signal name
    'org.freedesktop.login1.Manager',  # interface
    'org.freedesktop.login1'           # bus name
)

signal.signal(signal.SIGINT, sigterm_handler)
signal.signal(signal.SIGTERM, sigterm_handler)

loop = GLib.MainLoop()

# tell systemd to wait for us
lock = manager.Inhibit("sleep", "Screenlocker", "Locking screen...", "delay")
loop.run()

