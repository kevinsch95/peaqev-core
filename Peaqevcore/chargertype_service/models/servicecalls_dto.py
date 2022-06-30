from dataclasses import dataclass
from calltype import CallType

@dataclass
class ServiceCallsDTO:
    on: CallType
    off: CallType
    pause: CallType = None
    resume: CallType = None
    update_current: CallType = None
    
    def __post_init__(self):
        if self.pause is None:
            self.pause = self.off
        if self.resume is None:
            self.resume = self.on



test1 = CallType("hej", {})
model = ServiceCallsDTO(test1, test1)
print(model.resume)