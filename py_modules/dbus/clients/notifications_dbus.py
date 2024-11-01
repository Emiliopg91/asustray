import dbus
from typing import List, Optional, Any
from py_modules.utils.di import bean

@bean
class NotificationsClient:
    def __init__(self):
        self.bus = dbus.SessionBus()
        self.service_name = "org.freedesktop.Notifications"
        self.object_path = "/org/freedesktop/Notifications"
        self.interface_name = "org.freedesktop.Notifications"
        self.proxy = self.bus.get_object(self.service_name, self.object_path)

    # Métodos de la interfaz
    def notify(
        self,
        app_name: str,
        replaces_id: int,
        app_icon: str,
        summary: str,
        body: str,
        actions: List[str],
        hints: dict,
        expire_timeout: int
    ) -> int:
        method = self.proxy.get_dbus_method("Notify", self.interface_name)
        return method(app_name, replaces_id, app_icon, summary, body, actions, hints, expire_timeout)

    def close_notification(self, id: int):
        method = self.proxy.get_dbus_method("CloseNotification", self.interface_name)
        method(id)

    # Métodos de información
    @property
    def server_info(self) -> dict:
        method = self.proxy.get_dbus_method("GetServerInformation", self.interface_name)
        name, vendor, version, spec_version = method()
        return {
            "name": name,
            "vendor": vendor,
            "version": version,
            "spec_version": spec_version
        }

    @property
    def capabilities(self) -> List[str]:
        method = self.proxy.get_dbus_method("GetCapabilities", self.interface_name)
        return method()