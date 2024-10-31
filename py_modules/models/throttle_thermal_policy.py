from enum import Enum

class ThrottleThermalPolicy(Enum):
    PERFORMANCE = 1
    BALANCED = 0
    QUIET = 2

    def getNext(self):
        if(self == ThrottleThermalPolicy.BALANCED):
            return ThrottleThermalPolicy.PERFORMANCE
        if(self == ThrottleThermalPolicy.PERFORMANCE):
            return ThrottleThermalPolicy.QUIET
        if(self == ThrottleThermalPolicy.QUIET):
            return ThrottleThermalPolicy.BALANCED
        
    @staticmethod
    def map_to_throttle_policy(policy_name: str):
        policy_name = policy_name.upper()
        for policy in ThrottleThermalPolicy:
            if policy.name == policy_name:
                return policy
        raise ValueError(f"Policy '{policy_name}' no es válida.")