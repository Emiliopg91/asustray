from enum import IntEnum

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
