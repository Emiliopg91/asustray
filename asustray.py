#!/usr/bin/env python3

import gi
import time
import dbus

from py_modules.services.platform_service import PlatformService
from py_modules.models.platform_models import ThrottleThermalPolicy
from py_modules.dbus.servers.implementation import DbusImplementation
from py_modules.utils.constants import LAST_PROFILE
from py_modules.utils.di import inject
from py_modules.utils.logger import Logger
from py_modules.utils.tray_icon import TrayIcon
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib

gi.require_version("Gtk", "3.0")
gi.require_version("AppIndicator3", "0.1")


@inject
class AsusTray:
    inj_logger: Logger
    inj_platform_service: PlatformService
    inj_tray_icon: TrayIcon

    def __init__(self):
        # Configura el bucle principal de D-Bus y lo establece como predeterminado
        DBusGMainLoop(set_as_default=True)
    
    def main(self):
        self.inj_logger.info("#############################################################")
        self.inj_logger.info("Initializing AsusTray")
        self.inj_logger.add_tab()

        main_loop = GLib.MainLoop()
        self.inj_tray_icon.start(main_loop)

        self.inj_platform_service.set_throttle_thermal_policy(ThrottleThermalPolicy.PERFORMANCE, True)
        time.sleep(5)
        self.inj_platform_service.restore_throttle_thermal_policy()

        self.inj_logger.info("Starting service on dbus")
        self.session_bus = dbus.SessionBus()
        bus_name = dbus.service.BusName('es.emiliopg91.asustray', bus=self.session_bus)
        DbusImplementation(bus_name)

        self.inj_logger.rem_tab()
        self.inj_logger.info("Initialization finished")
        self.inj_logger.info("#############################################################")

        # Ejecuta el bucle principal
        main_loop.run()


if __name__ == "__main__":
    AsusTray().main()
