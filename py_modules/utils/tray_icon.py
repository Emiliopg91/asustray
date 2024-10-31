from py_modules.controllers.aura_controller import AuraController
from py_modules.controllers.profile_controller import ProfileController
from py_modules.utils.constants import ICON_BASE_PATH

import os

import gi
gi.require_version("Gtk", "3.0")
gi.require_version("AppIndicator3", "0.1")
from gi.repository import AppIndicator3 as appindicator  # noqa: E402
from gi.repository import GLib, Gtk  # noqa: E402

class TrayIcon:
    profile_controller = ProfileController()
    aura_controller = AuraController()

    # Holds a reference to the global loop running, to call loop.quit() when necessary
    loop: GLib.MainLoop = None
    # Holds the GTK Menu instance
    menu: Gtk.Menu = None
    # Holds the Indicator instance
    icon: appindicator.Indicator = None
    # Is set to True when Gtk needs to stop the main loop
    quitting: bool = False

    def __init__(self, loop: GLib.MainLoop) -> None:
        self.loop = loop
        
        self.icon = appindicator.Indicator.new(
            "asusctltray",
            Gtk.STOCK_INFO,
            appindicator.IndicatorCategory.SYSTEM_SERVICES,
        )
        self.icon.set_status(appindicator.IndicatorStatus.ACTIVE)

        self.build_menu()
        self.icon.set_menu(self.menu)
        self.icon.set_icon_theme_path(ICON_BASE_PATH)
        self.icon.set_icon_full("rog-logo", "")

    def build_menu(self) -> None:
        """Create and populate the main menu for the tray icon"""
        self.menu = Gtk.Menu()
        # self.menu = Gtk.Menu.new_from_model(Gio.Menu())

        TrayIcon.aura_controller.attach(self.menu)
        TrayIcon.profile_controller.attach(self.menu)

        icon = Gtk.MenuItem()
        icon.set_label("Quit asusctltray")
        icon.connect("activate", self._quit)
        self.menu.append(icon)

        self.menu.show_all()

    def _quit(self, _) -> None:
        """Simple callback wrapper for GLib.MainLoop.quit()"""
        self.loop.quit()