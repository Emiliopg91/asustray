from py_modules.utils.constants import ICON_PATH

import dbus
import os

class NotificacionInterface:
    def send_notification(self, title, message):

        # Obtener el servicio de notificaciones
        notify = dbus.Interface(dbus.SessionBus().get_object('org.freedesktop.Notifications', '/org/freedesktop/Notifications'),'org.freedesktop.Notifications')

        # Llamar al método Notify
        notify.Notify(
            'AsusTray',  # Identificador de la aplicación
            0,                # ID de la notificación (0 si no se quiere un ID)
            ICON_PATH,               # Icono (puedes poner un icono aquí o dejarlo vacío)
            title,           # Título de la notificación
            message,         # Mensaje de la notificación
            [],              # Acciones
            {"urgency": 1},              # Opciones
            3000               # Tiempo de expiración (0 para tiempo indefinido)
        )