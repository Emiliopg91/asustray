from typing import List, Tuple, Any
from py_modules.utils.di import bean
from py_modules.models.supergfx_models import GpuMode, GfxPower, UserActionRequired
import dbus

@bean
class SuperGfxClient:
    def __init__(self):
        self.bus = dbus.SystemBus()
        self.service_name = "org.supergfxctl.Daemon"
        self.object_path = "/org/supergfxctl/Gfx"
        self.interface_name = "org.supergfxctl.Daemon"
        self.proxy = self.bus.get_object(self.service_name, self.object_path)

    # Métodos de la interfaz que no son propiedades
    @property
    def supported(self) -> List[GpuMode]:
        method = self.proxy.get_dbus_method("Supported", self.interface_name)
        supported_modes = method()
        return [GpuMode(mode) for mode in supported_modes]

    # Propiedades
    @property
    def version(self) -> str:
        return self.proxy.get_dbus_method("Version", self.interface_name)()

    @property
    def mode(self) -> GpuMode:
        return GpuMode(self.proxy.get_dbus_method("Mode", self.interface_name)())

    @mode.setter
    def mode(self, mode: GpuMode):
        method = self.proxy.get_dbus_method("SetMode", self.interface_name)
        method(dbus.UInt32(mode.value))

    @property
    def vendor(self) -> str:
        return self.proxy.get_dbus_method("Vendor", self.interface_name)()

    @property
    def power(self) -> GfxPower:
        return GfxPower(self.proxy.get_dbus_method("Power", self.interface_name)())

    @property
    def pending_mode(self) -> GpuMode:
        return GpuMode(self.proxy.get_dbus_method("PendingMode", self.interface_name)())

    @property
    def pending_user_action(self) -> UserActionRequired:
        return UserActionRequired(self.proxy.get_dbus_method("PendingUserAction", self.interface_name)())

    @property
    def config(self) -> Tuple[bool, bool, bool, bool, bool, int]:
        return self.proxy.get_dbus_method("Config", self.interface_name)()

    @config.setter
    def config(self, config: Tuple[bool, bool, bool, bool, bool, int]):
        method = self.proxy.get_dbus_method("SetConfig", self.interface_name)
        method(dbus.Struct(config, signature='ubbbbtu'))

    # Métodos para leer y escribir propiedades D-Bus genéricos
    def get_property(self, property_name: str):
        return self.proxy.Get(self.interface_name, property_name, dbus_interface="org.freedesktop.DBus.Properties")

    def set_property(self, property_name: str, value: Any):
        self.proxy.Set(self.interface_name, property_name, value, dbus_interface="org.freedesktop.DBus.Properties")