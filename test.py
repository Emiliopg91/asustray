from typing import List, Tuple, Any
from py_modules.utils.di import bean
from enum import IntEnum
import dbus

class GpuMode(IntEnum):
    Hybrid = 0
    Integrated = 1
    NvidiaNoModeset = 2
    Vfio = 3
    AsusEgpu = 4
    AsusMuxDgpu = 5
    None_ = 6  # Se usa 'None_' para evitar conflictos con la palabra reservada 'None' en Python

class UserActionRequired(IntEnum):
    Logout = 0
    Reboot = 1
    SwitchToIntegrated = 2
    AsusEgpuDisable = 3
    Nothing = 4

class GfxPower(IntEnum):
    Active = 0
    Suspended = 1
    Off = 2
    AsusDisabled = 3
    AsusMuxDiscreet = 4
    Unknown = 5

# Ejemplo de uso
client = SuperGfxClient()
print("Versión:", client.version)
print("Modo actual:", client.mode.name)
print("Modos soportados:", client.supported)
print("Proveedor:", client.vendor)
print("Estado:", client.power.name)
print("Acción pendiente del usuario:", client.pending_user_action.name)

client.mode=GpuMode.Hybrid
print(client.pending_mode.name, "->", client.pending_user_action.name)