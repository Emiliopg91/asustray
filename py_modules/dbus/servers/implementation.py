import dbus
import dbus.service
import functools
from py_modules.utils.logger import Logger
from py_modules.utils.tray_icon import TrayIcon

class DbusImplementation(dbus.service.Object):
    def __init__(self, bus_name):
        dbus.service.Object.__init__(self, bus_name, '/es/emiliopg91/asustray')

    @dbus.service.method('es.emiliopg91.asustray.platform', out_signature='s')
    def NextProfile(self) -> str:
        nextProfile = TrayIcon.profile_controller.active_item.getNext()
        nextProfileTxt = nextProfile.name.capitalize()

        for item in TrayIcon.profile_controller.menu_items:
            if(item.get_label() == nextProfileTxt):
                item.set_active(True)

        return nextProfileTxt

    @dbus.service.method('es.emiliopg91.asustray.aura', out_signature='s')
    def IncreaseBrightness(self) -> str:
        nextLevel = TrayIcon.aura_controller.active_level.getNext()
        nextLevelTxt = nextLevel.name.capitalize()

        for item in TrayIcon.aura_controller.menu_items_level:
            if(item.get_label() == nextLevelTxt):
                item.set_active(True)

        return nextLevelTxt

    @dbus.service.method('es.emiliopg91.asustray.aura', out_signature='s')
    def DecreaseBrightness(self) -> str:
        nextLevel = TrayIcon.aura_controller.active_level.getPrevious()
        nextLevelTxt = nextLevel.name.capitalize()

        for item in TrayIcon.aura_controller.menu_items_level:
            if(item.get_label() == nextLevelTxt):
                item.set_active(True)

        return nextLevelTxt

    @dbus.service.method('es.emiliopg91.asustray.aura', out_signature='s')
    def NextLedMode(self) -> str:
        nextMode = TrayIcon.aura_controller.active_mode.getNext()
        nextModeTxt = nextMode.name.capitalize().replace("_", " ")

        for item in TrayIcon.aura_controller.menu_items_mode:
            if(item.get_label() == nextModeTxt):
                item.set_active(True)

        return nextModeTxt