from dataclasses import dataclass, field
from typing import List, Dict
from .hourobject import HourObject

@dataclass(frozen=False)
class HoursModel:
    non_hours: List[int] = field(default_factory=lambda : [])
    caution_hours: List[int] = field(default_factory=lambda : [])
    dynamic_caution_hours: Dict[int, float] = field(default_factory=lambda : {})
    hours_today: HourObject = field(default_factory=lambda : HourObject([],[],dict()))
    hours_tomorrow: HourObject = field(default_factory=lambda : HourObject([],[],dict()))
    conserve_top_up: bool = False

    def update_non_hours(
        self, 
        hour:int
        ) -> None:
        ret = []
        if self.conserve_top_up is False:
            ret.extend(h for h in self.hours_today.nh if h >= hour)
            ret.extend(h for h in self.hours_tomorrow.nh if h < hour)
        else:
            ret = [h for h in self.non_hours if (hour >= 13 and h < hour) or h >= hour]
        self.non_hours = ret
    
    def update_caution_hours(
        self, 
        hour:int
        ) -> None:
        ret = []
        if self.conserve_top_up is False:
            ret.extend(h for h in self.hours_today.ch if h >= hour)
            ret.extend(h for h in self.hours_tomorrow.ch if h < hour)
        else:
            ret = [h for h in self.caution_hours if (hour >= 13 and h < hour) or h >= hour]
        self.caution_hours = ret

    def update_dynanmic_caution_hours(
        self, 
        hour:int
        ) -> None:
        ret = {}
        if self.conserve_top_up is False:
            ret.update({k: v for k, v in self.hours_today.dyn_ch.items() if k >= hour})
            ret.update({k: v for k, v in self.hours_tomorrow.dyn_ch.items() if k < hour})
        else:
            ret = {k: v for k, v in self.dynamic_caution_hours.items()  if (hour >= 13 and k < hour) or k >= hour}
        self.dynamic_caution_hours = ret


@dataclass(frozen=False)
class HourSelectionOptions:
    cautionhour_type: float = 0
    absolute_top_price: float = 0
    min_price: float = 0
    allow_top_up: bool = False

    @staticmethod
    def set_absolute_top_price(val) -> float:
        if val is None:
            return float("inf")
        if val <= 0:
            return float("inf")
        return float(val)


@dataclass(frozen=False)
class HourSelectionModel:
    prices_today: List[float] = field(default_factory=lambda : [])
    prices_tomorrow: List[float] = field(default_factory=lambda : [])
    hours: HoursModel = HoursModel()
    options: HourSelectionOptions = HourSelectionOptions

    def validate(self):
        assert 0 < self.options.cautionhour_type <= 1