from day_judge import DayJudge
import jpholiday

# 火曜日かどうかを判定する
class DayJudgeTuesday(DayJudge):
 
    @classmethod
    def target_day(cls, date):
        if date.weekday() == 1:
	        return True
        return False