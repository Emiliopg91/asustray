#!/usr/bin/env python3

import gi
import os
import dbus

from py_modules.services.asus_service import AsusService
from py_modules.models.throttle_thermal_policy import ThrottleThermalPolicy
from py_modules.dbus.servers.implementation import DbusImplementation
from py_modules.utils.constants import LAST_PROFILE
from py_modules.utils.di import inject
from py_modules.utils.logger import Logger
from py_modules.utils.tray_icon import TrayIcon
from dbus.mainloop.glib import DBusGMainLoop

gi.require_version("Gtk", "3.0")
gi.require_version("AppIndicator3", "0.1")

from gi.repository import GLib

@inject
class AsusTray:
    logger:Logger
    
    def main(self):
        self.logger.info("#############################################################")
        self.logger.info("Initializing AsusTray")
        DBusGMainLoop(set_as_default=True)
        session_bus = dbus.SessionBus()
        bus_name = dbus.service.BusName('es.emiliopg91.asustray', bus=session_bus)
        DbusImplementation(bus_name)
        self.logger.info("Running service on dbus")
        loop = GLib.MainLoop()
        TrayIcon(loop)
        try:
            with open(LAST_PROFILE, "r") as f:
                policy_name = f.readline().strip()
                self.logger.info(f"Restoring profile {policy_name}")
                policy = ThrottleThermalPolicy.map_to_throttle_policy(policy_name)                
                AsusService().set_throttle_thermal_policy(policy)
        except Exception as e:
            self.logger.error(f"Error while restoring profile: {e}")
        loop.run()

if __name__ == "__main__":
    AsusTray().main()