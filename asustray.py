#!/usr/bin/env python3

import gi
import os
import dbus

from py_modules.services.asus_service import AsusService
from py_modules.models.throttle_thermal_policy import ThrottleThermalPolicy
from py_modules.dbus.implementation import DbusImplementation
from py_modules.utils.tray_icon import TrayIcon
from dbus.mainloop.glib import DBusGMainLoop

gi.require_version("Gtk", "3.0")
gi.require_version("AppIndicator3", "0.1")

from gi.repository import GLib

if __name__ == "__main__":
    DBusGMainLoop(set_as_default=True)
    session_bus = dbus.SessionBus()
    bus_name = dbus.service.BusName('es.emiliopg91.asustray', bus=session_bus)
    dbus_service = DbusImplementation(bus_name)
    loop = GLib.MainLoop()
    TrayIcon(loop)
    try:
        asustray_file_path = os.path.expanduser("~/.asustray")
        with open(asustray_file_path, "r") as f:
            policy_name = f.readline().strip()
            print(f"Restoring profile {policy_name}")
            policy = ThrottleThermalPolicy.map_to_throttle_policy(policy_name)                
            AsusService().set_throttle_thermal_policy(policy)
    except Exception as e:
        print(f"Error while restoring profile: {e}")
    loop.run()
    