from py_modules.dbus.clients.fan_curves_dbus import FanCurvesClient
from py_modules.dbus.clients.notifications_dbus import NotificationsClient
from py_modules.dbus.clients.platform_dbus import PlatformClient
from py_modules.dbus.clients.power_dbus import PowerProfilesClient
from py_modules.models.power_models import PowerProfile
from py_modules.models.platform_models import ThrottleThermalPolicy
from py_modules.utils.constants import LAST_PROFILE, ICON_PATH
from py_modules.utils.di import inject, bean
from py_modules.utils.logger import Logger

policy_profile_asoc = {
    ThrottleThermalPolicy.QUIET: PowerProfile.POWER_SAVER,
    ThrottleThermalPolicy.BALANCED: PowerProfile.BALANCED,
    ThrottleThermalPolicy.PERFORMANCE: PowerProfile.PERFORMANCE
}

@bean
@inject
class PlatformService:
    inj_fan_curves: FanCurvesClient
    inj_platform: PlatformClient
    inj_power: PowerProfilesClient
    inj_notifications: NotificationsClient
    inj_logger: Logger

    def get_throttle_thermal_policy(self) -> ThrottleThermalPolicy:
        return self.inj_platform.throttle_thermal_policy

    def set_throttle_thermal_policy(self, policy: ThrottleThermalPolicy, temporal = False):
        try:
            self.inj_logger.info(f"Setting profile:")
            self.inj_logger.add_tab()
            self.inj_logger.info(f"Throttle policy: {policy.name}")
            self.inj_platform.throttle_thermal_policy = policy

            self.inj_logger.info(f"Fan curve: {policy.name}")
            self.inj_fan_curves.set_curves_to_defaults(policy)
            self.inj_fan_curves.reset_profile_curves(policy)
            self.inj_fan_curves.set_fan_curves_enabled(policy, True)
            
            power_policy = policy_profile_asoc[policy]
            self.inj_logger.info(f"Power policy: {power_policy.name}")
            self.inj_power.active_profile = power_policy
            self.inj_logger.rem_tab()
            self.inj_logger.info("Profile setted succesfully")

            if(temporal != True):
                self.inj_notifications.notify("AsusTray",0, ICON_PATH, "Performance profile", f"Setted {policy.name.capitalize()} profile", [], {"urgency": 1}, 3000)
                with open(LAST_PROFILE, "w") as f:
                    f.write(f"{policy.name}\n")

        except Exception as e:
            self.inj_logger.info(f"Error al establecer ThrottleThermalPolicy: {e}")

    def restore_throttle_thermal_policy(self):
        self.inj_logger.info(f"Restoring profile")
        self.inj_logger.add_tab()
        try:
            with open(LAST_PROFILE, "r") as f:
                policy_name = f.readline().strip()
                policy = ThrottleThermalPolicy.map_to_throttle_policy(policy_name)
                self.set_throttle_thermal_policy(policy)
        except Exception as e:
            self.inj_logger.error(f"Error while restoring profile: {e}")
        self.inj_logger.rem_tab()
        self.inj_logger.info("Restored succesfully")
