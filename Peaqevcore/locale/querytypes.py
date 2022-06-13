from datetime import date, datetime, time
from enum import Enum
from dataclasses import dataclass
import logging

"""Peak querytypes"""
QUERYTYPE_BASICMAX = "BasicMax"
QUERYTYPE_AVERAGEOFTHREEDAYS = "AverageOfThreeDays"
QUERYTYPE_AVERAGEOFTHREEHOURS = "AverageOfThreeHours"
QUERYTYPE_AVERAGEOFTHREEDAYS_MIN = "AverageOfThreeDays_Min"
QUERYTYPE_AVERAGEOFTHREEHOURS_MIN = "AverageOfThreeHours_Min"
QUERYTYPE_AVERAGEOFFIVEDAYS = "AverageOfFiveDays"
QUERYTYPE_AVERAGEOFFIVEDAYS_MIN = "AverageOfFiveDays_Min"
QUERYTYPE_HIGHLOAD = "HighLoad"
QUERYTYPE_AVERAGEOFTHREEHOURS_MON_FRI_07_19 = "sala"
QUERYTYPE_AVERAGEOFTHREEHOURS_MON_FRI_07_19_MIN = "sala"
QUERYTYPE_MAX_NOV_MAR_MON_FRI_06_22 = "skövde"
QUERYTYPE_BASICMAX_MON_FRI_07_17_DEC_MAR_ELSE_REGULAR = "kristinehamn"
QUERYTYPE_SOLLENTUNA = "sollentuna"
QUERYTYPE_SOLLENTUNA_MIN = "sollentuna_min"

"""Misc"""
QUARTER_HOURLY = "quarter-hourly"
HOURLY = "hourly"

_LOGGER = logging.getLogger(__name__)

class SumTypes(Enum):
    Max = 1
    Avg = 2
    Min = 3


class TimePeriods(Enum):
    Hourly = 1
    Daily = 2
    Weekly = 3
    BiWeekly = 4
    Monthly = 5
    Yearly = 6
    UnSet = 7


@dataclass(frozen=True)
class SumCounter:
    counter:int = 1
    groupby: TimePeriods = TimePeriods.UnSet


@dataclass(frozen=True)
class QueryProperties:
    sumtype: SumTypes
    timecalc:TimePeriods
    cycle: TimePeriods


@dataclass
class PeaksModel:
    p: dict
    m:int = 0
    is_dirty:bool = False

    def set_init_dict(self, dict_data, dt = datetime.now()):
        if dt.month == self.m:
            ppdict = {}
            for pp in dict_data["p"]:
                tkeys = pp.split("h")
                ppkey = (int(tkeys[0]), int(tkeys[1]))
                ppdict[ppkey] = dict_data["p"][pp]
            if len(self.p) > 0:
                ppdict = self.p | ppdict
            self.p = ppdict
            self.m = dict_data["m"]
            self.is_dirty = True

    def reset(self) -> None:
        self.m = 0
        self.is_dirty = False
        self.p = {}

class LocaleQuery:
    def __init__(
        self, 
        sumtype: SumTypes, 
        timecalc: TimePeriods, 
        cycle: TimePeriods, 
        sumcounter: SumCounter = None
        ) -> None:    
        self._peaks:PeaksModel = PeaksModel({})
        self._props = QueryProperties(
            sumtype, 
            timecalc, 
            cycle
            )
        self._sumcounter:SumCounter= sumcounter
        self._observed_peak_value:float = 0 
        self._charged_peak_value:float = 0

    def reset(self) -> None:
        self._peaks.reset()
        self._observed_peak_value = 0
        self._charged_peak_value = 0

    @property
    def peaks_export(self) -> dict:
        ppdict = {}
        for pp in self._peaks.p:
            ppkey = str(str(pp[0]) + "h" + str(pp[1]))
            ppdict[ppkey] = self._peaks.p[pp]
        return {
            "m": self._peaks.m,
            "p": ppdict
        }

    @property
    def peaks(self) -> PeaksModel:
        if self._peaks.is_dirty:
            self._sanitize_values()
        return self._peaks

    @property
    def sumcounter(self) -> SumCounter:
        if self._sumcounter is not None:
            return self._sumcounter
        return SumCounter()

    @property
    def charged_peak(self) -> float: 
        if self._peaks.is_dirty:
            self._sanitize_values()
        ret = self._charged_peak_value
        return round(ret,2)

    @charged_peak.setter
    def charged_peak(self, val):
        self._charged_peak_value = val

    @property
    def observed_peak(self) -> float: 
        if self._peaks.is_dirty:
            self._sanitize_values()
        ret = self.charged_peak if self._props.sumtype is SumTypes.Max else self._observed_peak_value
        return round(ret, 2)

    @observed_peak.setter
    def observed_peak(self, val):
        self._observed_peak_value = val

    def try_update(self, newval, dt = datetime.now()):
        if self.peaks.is_dirty:
            self._sanitize_values()
        _dt = (dt.day, dt.hour)
        if len(self.peaks.p) == 0:
            """first addition for this month"""
            self._peaks.p[_dt] = newval
            self._peaks.m = dt.month
        elif dt.month != self._peaks.m:
            """new month, reset"""
            self.reset_values(newval, dt)
        else:
            self._set_update_for_groupby(newval, _dt)
        if len(self.peaks.p) > self.sumcounter.counter:
                self.peaks.p.pop(min(self.peaks.p, key=self._peaks.p.get))
        self._update_peaks()

    def _set_update_for_groupby(self, newval, _dt):
        if self.sumcounter.groupby in [TimePeriods.Daily, TimePeriods.UnSet]:
            _datekey = [k for k,v in self.peaks.p.items() if _dt[0] in k]
            if len(_datekey) > 0:
                if newval > self.peaks.p[_datekey[0]]:
                        self.peaks.p.pop(_datekey[0])
                        self.peaks.p[_dt] = newval
            else:
                self.peaks.p[_dt] = newval
        elif self.sumcounter.groupby == TimePeriods.Hourly:
            if _dt in self._peaks.p.keys():
                if newval > self.peaks.p[_dt]:
                        self.peaks.p[_dt] = newval
            else:
                self.peaks.p[_dt] = newval

    def _update_peaks(self):
        if self._props.sumtype is SumTypes.Max:
            self.charged_peak = max(self._peaks.p.values())
        elif self._props.sumtype is SumTypes.Avg:
            self.observed_peak = min(self._peaks.p.values())
            self.charged_peak = sum(self._peaks.p.values()) / len(self._peaks.p)

    def reset_values(self, newval, dt = datetime.now()):
        self._peaks.p.clear()
        self.try_update(newval, dt)

    def _sanitize_values(self):
        def countX(lst, x):
            count = 0
            for ele in lst:
                if ele[0] == x:
                    count = count + 1
            return count

        if self.sumcounter.groupby == TimePeriods.Daily:
            duplicates = set()
            for k in self._peaks.p.keys():
                if countX(self._peaks.p.keys(), k[0]) > 1:
                    duplicates.add(k)
            if len(duplicates) > 0:
                for d in duplicates:
                    comparerkeys = []
                    comparervalues = []
                    for k in self._peaks.p.keys():
                        if k == d:
                            comparerkeys.append(k)
                            comparervalues.append(self._peaks.p[k])                           
                    self._peaks.p.pop(comparerkeys[comparervalues.index(min(comparervalues))])
        while len(self._peaks.p) > self.sumcounter.counter:
            self._peaks.p.pop(min(self._peaks.p, key=self._peaks.p.get))
        self._peaks.is_dirty = False
        self._update_peaks()

QUERYTYPES = {
    QUERYTYPE_AVERAGEOFTHREEHOURS: LocaleQuery(sumtype=SumTypes.Avg, timecalc=TimePeriods.Hourly, cycle=TimePeriods.Monthly, sumcounter=SumCounter(counter=3, groupby=TimePeriods.Hourly)),
    QUERYTYPE_AVERAGEOFTHREEDAYS: LocaleQuery(sumtype=SumTypes.Avg, timecalc=TimePeriods.Hourly, cycle=TimePeriods.Monthly, sumcounter=SumCounter(counter=3, groupby=TimePeriods.Daily)),
    QUERYTYPE_BASICMAX: LocaleQuery(sumtype=SumTypes.Max, timecalc=TimePeriods.Hourly, cycle=TimePeriods.Monthly)
}


# to_state_machine = {'m': 7, 'p': {'14h21': 2, '11h22': 1.49, '12h9': 1.93, '12h14': 0.73}}
# p1 = QUERYTYPES[QUERYTYPE_AVERAGEOFTHREEDAYS]
# p1.reset()
# p1.try_update(newval=1, dt=datetime.combine(date(2022, 7, 15), time(21, 30)))
# p1.peaks.set_init_dict(to_state_machine, datetime.combine(date(2022, 7, 15), time(21, 30)))
# assert len(p1.peaks.p) == 3
# assert p1.charged_peak == 1.5
# assert p1.observed_peak == 1
# p1.try_update(newval=1.5, dt=datetime.combine(date(2022, 7, 15), time(22, 30)))
# assert len(p1.peaks.p) == 3
# assert p1.charged_peak == 1.66
# assert p1.observed_peak == 1.49