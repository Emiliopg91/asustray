from enum import Enum

class AuraMode(Enum):
    STATIC = 0
    BREATHE = 1
    PULSE = 10
    RAINBOW_CYCLE = 2
    RAINBOW_WAVE = 3

    def getNext(self):
        if(self == AuraMode.STATIC):
            return AuraMode.BREATHE
        if(self == AuraMode.BREATHE):
            return AuraMode.PULSE
        if(self == AuraMode.PULSE):
            return AuraMode.RAINBOW_CYCLE
        if(self == AuraMode.RAINBOW_CYCLE):
            return AuraMode.RAINBOW_WAVE
        if(self == AuraMode.RAINBOW_WAVE):
            return AuraMode.STATIC

    @classmethod
    def from_value(cls, value: str):
        """Devuelve la entrada del enumerado que corresponde al valor dado."""
        for profile in cls:
            if profile.value == value:
                return profile
        raise ValueError(f"No se encontró un modo para el valor '{value}'")
