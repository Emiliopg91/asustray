from enum import Enum

class PowerProfile(Enum):
    POWER_SAVER = "power-saver"
    BALANCED = "balanced"
    PERFORMANCE = "performance"

    def from_value(cls, value: str):
        """Devuelve la entrada del enumerado que corresponde al valor dado."""
        for profile in cls:
            if profile.value == value:
                return profile
        raise ValueError(f"No se encontró un perfil de energía para el valor '{value}'")
