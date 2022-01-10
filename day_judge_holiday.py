from day_judge import DayJudge
import jpholiday

# 休日かどうかを判定する
class DayJudgeHoliday(DayJudge):
 
    @classmethod
    def target_day(cls, date):
        if 4 < date.weekday() < 7 or \
	       jpholiday.is_holiday(date):
	        return True
        return False