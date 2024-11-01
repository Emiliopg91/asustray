#!/usr/bin/env python3

import gi
import time
import dbus

from py_modules.services.asus_service import AsusService
from py_modules.models.throttle_thermal_policy import ThrottleThermalPolicy
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
    logger: Logger
    asus_service: AsusService

    def __init__(self):
        # Configura el bucle principal de D-Bus y lo establece como predeterminado
        DBusGMainLoop(set_as_default=True)
    
    def main(self):
        self.logger.info("#############################################################")
        self.logger.info("Initializing AsusTray")
        self.logger.add_tab()

        # Inicializa el icono de la bandeja y el bucle principal de GLib
        main_loop = GLib.MainLoop()
        TrayIcon(main_loop)

        # Inicializa el bus de sesión después del main_loop
        self.session_bus = dbus.SessionBus()

        # Establece el nombre del bus para el servicio
        bus_name = dbus.service.BusName('es.emiliopg91.asustray', bus=self.session_bus)

        # Mensajes de log
        self.logger.info("Running service on dbus")

        # Ajusta el perfil térmico y restaura el perfil anterior
        self.asus_service.set_throttle_thermal_policy(ThrottleThermalPolicy.PERFORMANCE, True)
        time.sleep(5)
        try:
            with open(LAST_PROFILE, "r") as f:
                policy_name = f.readline().strip()
                self.logger.info(f"Restoring profile {policy_name}")
                policy = ThrottleThermalPolicy.map_to_throttle_policy(policy_name)
                self.asus_service.set_throttle_thermal_policy(policy)
        except Exception as e:
            self.logger.error(f"Error while restoring profile: {e}")

        # Inicializa el servicio D-Bus
        DbusImplementation(bus_name)

        self.logger.rem_tab()
        self.logger.info("Initialization finished")
        self.logger.info("#############################################################")

        # Ejecuta el bucle principal
        main_loop.run()


if __name__ == "__main__":
    AsusTray().main()
