#!/bin/env python3

import dbus
import dbus.mainloop.glib
import os
import time
import subprocess
import gi
import signal
from gi.repository import GLib
import sys

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
    os.remove("/tmp/lock_before_sleep.pid")
    os.system("nohup i3-nagbar -t warning -m 'lock_before_sleep.py got terminated, that means your screen will not be locked automatically before sleep. This is bad! Do you want to restart it?' -B 'Damn yes, restart!' 'nohup ~/scripts/lock_before_sleep.py &; killall i3-nagbar'")
    os.system("notify-send -u critical -a \"lock_before_sleep.py\" -c warning \"Screenlocker killed\" \"python3 got killed, restart lock_before_sleep.py, otherwise the screen will not be locked automatically before sleep\"")
    # loop.quit()
    # GLib.idle_add(quit)

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
#signal.signal(signal.SIGKILL, sigterm_handler)

loop = GLib.MainLoop()

# quit if script is running already running
if os.path.isfile("/tmp/lock_before_sleep.pid"):
    log("script is already running, pidfile exists")
    sys.exit(1)

with open("/tmp/lock_before_sleep.pid", 'w') as f:
    f.write(str(os.getpid()))
    f.close()
# tell systemd to wait for us
lock = manager.Inhibit("sleep", "Screenlocker", "Locking screen...", "delay")
loop.run()

