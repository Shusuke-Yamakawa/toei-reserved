from abc import *

# 曜日判定の基底クラス
class DayJudge(metaclass = ABCMeta):
 
    @classmethod
    @abstractmethod
    def target_day(cls, date):
        pass