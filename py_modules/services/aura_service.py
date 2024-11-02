from py_modules.dbus.clients.aura_dbus import AuraClient
from py_modules.models.aura_models import AuraLevel, AuraMode
from py_modules.utils.di import inject, bean
from py_modules.utils.logger import Logger

@bean
@inject
class AuraService:
    inj_aura: AuraClient
    inj_logger: Logger

    def get_aura_mode(self) -> AuraMode:
        return self.inj_aura.led_mode

    def set_aura_mode(self, mode: AuraMode):
        self.inj_logger.info(f"Setting Aura mode to {mode.name}")
        self.inj_aura.led_mode = mode

    def get_aura_level(self) -> AuraLevel:
        return self.inj_aura.brightness
    
    def set_aura_level(self, level: AuraLevel):
        self.inj_logger.info(f"Setting Aura level to {level.name}")
        self.inj_aura.brightness = level