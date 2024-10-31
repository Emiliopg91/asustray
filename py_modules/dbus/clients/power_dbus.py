import dbus
from py_modules.models.power_profile import PowerProfile
from py_modules.utils.di import bean

@bean
class PowerProfilesClient:
    def __init__(self):
        self.bus = dbus.SystemBus()
        self.service_name = "net.hadess.PowerProfiles"
        self.object_path = "/net/hadess/PowerProfiles"
        self.interface_name = "net.hadess.PowerProfiles"
        self.proxy = self.bus.get_object(self.service_name, self.object_path)

    # Métodos de la interfaz
    def get_profiles(self):
        """Obtiene la lista de perfiles de energía disponibles."""
        method = self.proxy.get_dbus_method("GetProfiles", self.interface_name)
        return method()

    def get_active_profile(self) -> PowerProfile:
        """Obtiene el perfil de energía activo."""
        return PowerProfile(self.proxy.Get(self.interface_name, "ActiveProfile", dbus_interface=dbus.PROPERTIES_IFACE))

    def set_active_profile(self, profile: PowerProfile):
        """Establece el perfil de energía activo."""
        self.proxy.Set(self.interface_name, "ActiveProfile", profile.value, dbus_interface=dbus.PROPERTIES_IFACE)

    # Propiedades
    @property
    def active_profile(self) -> PowerProfile:
        return self.get_active_profile()

    @active_profile.setter
    def active_profile(self, profile: PowerProfile):
        self.set_active_profile(profile)
    """
    @property
    def balanced_available(self) -> bool:
        return self.proxy.Get(self.interface_name, "BalancedAvailable", dbus_interface=dbus.PROPERTIES_IFACE)

    @property
    def performance_available(self) -> bool:
        return self.proxy.Get(self.interface_name, "PerformanceAvailable", dbus_interface=dbus.PROPERTIES_IFACE)

    @property
    def power_saver_available(self) -> bool:
        return self.proxy.Get(self.interface_name, "PowerSaverAvailable", dbus_interface=dbus.PROPERTIES_IFACE)
    """