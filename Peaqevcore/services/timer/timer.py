from dataclasses import dataclass
from datetime import datetime, timedelta
from .const import DEFAULT_OVERRIDE, MONTHS

@dataclass(frozen=False)
class Timer:
    expire:datetime = datetime.now()

    @property
    def is_override(self) -> bool:
        return self.expire > datetime.now()

    @property
    def override_string(self) -> str:
        if self.expire.day != datetime.now().day:
            _dt = f"{self.expire.day} {MONTHS[self.expire.month]} - {self.expire.hour}:{self.expire.minute}"
        else:
            _dt = f"{self.expire.hour}:{self.expire.minute}"
        return f"Nonhours ignored until {_dt}"

    def update(self, value_in_hours:int=DEFAULT_OVERRIDE):
        if not self.is_override:
            self.expire = datetime.now()
        try:
            assert isinstance(value_in_hours, int)
        except AssertionError as a:
            return
        value_in_seconds = value_in_hours * 3600
        self.expire += timedelta(seconds=value_in_seconds)
