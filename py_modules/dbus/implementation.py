import dbus
import dbus.service
import functools
from py_modules.utils.tray_icon import TrayIcon

def log_method_call(method):
    @functools.wraps(method)  # Esto preserva la firma y metadatos del método original
    def wrapper(self, *args, **kwargs):
        # Combinar args y kwargs en una lista
        combined_args = list(args) + [f"{key}={value}" for key, value in kwargs.items()]
        
        # Imprimir el nombre del método y los argumentos en el formato deseado
        print(f"Invoking dbus method {method.__name__}({', '.join(map(str, combined_args))})")
        
        # Llamar al método original
        result = method(self, *args, **kwargs)
        
        # Imprimir el valor de retorno
        print(f"Method returning value: {result}")
        return result  # Retornar el valor del método original

    return wrapper


class DbusImplementation(dbus.service.Object):
    def __init__(self, bus_name):
        dbus.service.Object.__init__(self, bus_name, '/es/emiliopg91/asustray')

    @dbus.service.method('es.emiliopg91.asustray.platform', out_signature='s')
    @log_method_call
    def NextProfile(self) -> str:
        nextProfile = TrayIcon.profile_controller.active_item.getNext()
        nextProfileTxt = nextProfile.name.capitalize()

        for item in TrayIcon.profile_controller.menu_items:
            if(item.get_label() == nextProfileTxt):
                item.set_active(True)

        return nextProfileTxt

    @dbus.service.method('es.emiliopg91.asustray.aura', out_signature='s')
    @log_method_call
    def IncreaseBrightness(self) -> str:
        nextLevel = TrayIcon.aura_controller.active_level.getNext()
        nextLevelTxt = nextLevel.name.capitalize()

        for item in TrayIcon.aura_controller.menu_items_level:
            if(item.get_label() == nextLevelTxt):
                item.set_active(True)

        return nextLevelTxt

    @dbus.service.method('es.emiliopg91.asustray.aura', out_signature='s')
    @log_method_call
    def DecreaseBrightness(self) -> str:
        nextLevel = TrayIcon.aura_controller.active_level.getPrevious()
        nextLevelTxt = nextLevel.name.capitalize()

        for item in TrayIcon.aura_controller.menu_items_level:
            if(item.get_label() == nextLevelTxt):
                item.set_active(True)

        return nextLevelTxt

    @dbus.service.method('es.emiliopg91.asustray.aura', out_signature='s')
    @log_method_call
    def NextLedMode(self) -> str:
        nextMode = TrayIcon.aura_controller.active_mode.getNext()
        nextModeTxt = nextMode.name.capitalize().replace("_", " ")

        for item in TrayIcon.aura_controller.menu_items_mode:
            if(item.get_label() == nextModeTxt):
                item.set_active(True)

        return nextModeTxt