import dbus
import re
import subprocess
from py_modules.models.aura_level import AuraLevel
from py_modules.models.aura_mode import AuraMode

class AuraClient:
    def __init__(self):
        self.bus = dbus.SystemBus()
        
        # Detecting aura device path
        result = subprocess.run(["asusctl", "led-mode", "--help"], capture_output=True, text=True, check=True)
        match = re.search(r"Found aura device at (.+?)(?:,|$)", result.stdout)
        aura_path = "/org/asuslinux"
        if match:
            aura_path = match.group(1)

        self.aura_proxy = self.bus.get_object("org.asuslinux.Daemon", aura_path)
        self.properties_iface = dbus.Interface(self.aura_proxy, dbus_interface="org.freedesktop.DBus.Properties")

    # Methods for org.freedesktop.DBus.Peer
    def ping(self):
        self.aura_proxy.Ping(dbus_interface="org.freedesktop.DBus.Peer")

    def get_machine_id(self):
        return self.aura_proxy.GetMachineId(dbus_interface="org.freedesktop.DBus.Peer")

    # Methods for org.freedesktop.DBus.Properties
    def get_property(self, interface_name: str, property_name: str):
        return self.properties_iface.Get(interface_name, property_name)

    def set_property(self, interface_name: str, property_name: str, value):
        self.properties_iface.Set(interface_name, property_name, value)

    def get_all_properties(self, interface_name: str):
        return self.properties_iface.GetAll(interface_name)

    # Methods for org.asuslinux.Aura
    def all_mode_data(self):
        return self.aura_proxy.AllModeData(dbus_interface="org.asuslinux.Aura")

    def direct_addressing_raw(self, data):
        self.aura_proxy.DirectAddressingRaw(data, dbus_interface="org.asuslinux.Aura")

    # Properties for org.asuslinux.Aura
    @property
    def brightness(self) -> AuraLevel:
        return AuraLevel.from_value(self.get_property("org.asuslinux.Aura", "Brightness"))

    @brightness.setter
    def brightness(self, value: AuraLevel):
        self.set_property("org.asuslinux.Aura", "Brightness", dbus.UInt32(value.value))

    @property
    def device_type(self):
        return self.get_property("org.asuslinux.Aura", "DeviceType")

    @property
    def led_mode(self) -> AuraMode:
        return AuraMode.from_value(self.get_property("org.asuslinux.Aura", "LedMode"))

    @led_mode.setter
    def led_mode(self, value: AuraMode):
        self.set_property("org.asuslinux.Aura", "LedMode", dbus.UInt32(value.value))

    @property
    def led_mode_data(self):
        return self.get_property("org.asuslinux.Aura", "LedModeData")

    @led_mode_data.setter
    def led_mode_data(self, value):
        self.set_property("org.asuslinux.Aura", "LedModeData", value)

    @property
    def led_power(self):
        return self.get_property("org.asuslinux.Aura", "LedPower")

    @led_power.setter
    def led_power(self, value):
        self.set_property("org.asuslinux.Aura", "LedPower", value)

    @property
    def supported_basic_modes(self):
        return self.get_property("org.asuslinux.Aura", "SupportedBasicModes")

    @property
    def supported_basic_zones(self):
        return self.get_property("org.asuslinux.Aura", "SupportedBasicZones")

    @property
    def supported_brightness(self):
        return self.get_property("org.asuslinux.Aura", "SupportedBrightness")

    @property
    def supported_power_zones(self):
        return self.get_property("org.asuslinux.Aura", "SupportedPowerZones")