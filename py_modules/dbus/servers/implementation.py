import dbus
import dbus.service
import time
from functools import wraps
from py_modules.controllers.aura_controller import AuraController
from py_modules.controllers.profile_controller import ProfileController
from py_modules.utils.di import bean,inject
from py_modules.utils.logger import Logger

def log_execution(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        class_name = self.__class__.__name__
        self.logger.info(f"Invoking {class_name}.{func.__name__}({', '.join(map(str, args))})")
        self.logger.add_tab()
        
        start_time = time.time()
        try:
            result = func(self, *args, **kwargs)
            execution_time = time.time() - start_time
            self.logger.rem_tab()
            self.logger.info(f"Invocation finished after {execution_time:.3f} with result: {result}")
        except Exception as e:
            execution_time = time.time() - start_time
            self.logger.rem_tab()
            self.logger.info(f"Invocation finished after {execution_time:.3f} with error: {e}")
            raise e
        
        return result
    return wrapper

@inject
class DbusImplementation(dbus.service.Object):
    inj_profile_controller: ProfileController
    inj_aura_controller: AuraController
    inj_logger: Logger

    def __init__(self, bus_name):
        dbus.service.Object.__init__(self, bus_name, '/es/emiliopg91/asustray')
        self.logger = self.inj_logger

    @dbus.service.method('es.emiliopg91.asustray.platform', out_signature='s')
    @log_execution
    def NextProfile(self) -> str:
        return self.inj_profile_controller.set_next_profile()

    @dbus.service.method('es.emiliopg91.asustray.aura', out_signature='s')
    @log_execution
    def IncreaseBrightness(self) -> str:
        return self.inj_aura_controller.set_next_aura_level()

    @dbus.service.method('es.emiliopg91.asustray.aura', out_signature='s')
    @log_execution
    def DecreaseBrightness(self) -> str:
        return self.inj_aura_controller.set_previous_aura_level()

    @dbus.service.method('es.emiliopg91.asustray.aura', out_signature='s')
    @log_execution
    def NextLedMode(self) -> str:
        return self.inj_aura_controller.set_next_aura_mode()