from py_modules.dbus.clients.fan_curves_dbus import FanCurvesClient
from py_modules.dbus.clients.aura_dbus import AuraClient
from py_modules.dbus.clients.platform_dbus import PlatformClient
from py_modules.dbus.clients.power_dbus import PowerProfilesClient
from py_modules.models.aura_level import AuraLevel
from py_modules.models.aura_mode import AuraMode
from py_modules.models.power_profile import PowerProfile
from py_modules.models.throttle_thermal_policy import ThrottleThermalPolicy
from py_modules.services.notification_interface import NotificacionInterface

import os



policy_profile_asoc = {
    ThrottleThermalPolicy.QUIET: PowerProfile.POWER_SAVER,
    ThrottleThermalPolicy.BALANCED: PowerProfile.BALANCED,
    ThrottleThermalPolicy.PERFORMANCE: PowerProfile.PERFORMANCE
}

class AsusService:
    def __init__(self):
        self.fan_curves = FanCurvesClient()
        self.platform = PlatformClient()
        self.power = PowerProfilesClient()
        self.aura = AuraClient()

    def get_aura_mode(self) -> AuraMode:
        return self.aura.led_mode

    def set_aura_mode(self, mode: AuraMode):
        self.aura.led_mode = mode

    def get_aura_level(self) -> AuraLevel:
        return self.aura.brightness
    
    def set_aura_level(self, level: AuraLevel):
        self.aura.brightness = level

    def get_throttle_thermal_policy(self) -> ThrottleThermalPolicy:
        current = int(self.platform.throttle_thermal_policy)
        return ThrottleThermalPolicy(current)

    def set_throttle_thermal_policy(self, policy: ThrottleThermalPolicy):
        try:
            print(f"Setting profile:")
            print(f"    Throttle policy: {policy.name}")
            self.platform.throttle_thermal_policy = policy.value

            print(f"          Fan curve: {policy.name}")
            self.fan_curves.set_curves_to_defaults(policy)
            self.fan_curves.reset_profile_curves(policy)
            self.fan_curves.set_fan_curves_enabled(policy, True)
            
            power_policy = policy_profile_asoc[policy]
            print(f"       Power policy: {power_policy.name}")
            self.power.active_profile = power_policy
            
            print("Profile setted succesfully")
            NotificacionInterface().send_notification("Performance profile", f"Setted {policy.name.capitalize()} profile")

            asustray_file_path = os.path.expanduser("~/.asustray")
            with open(asustray_file_path, "w") as f:
                f.write(f"{policy.name}\n")

        except Exception as e:
            print(f"Error al establecer ThrottleThermalPolicy: {e}")
