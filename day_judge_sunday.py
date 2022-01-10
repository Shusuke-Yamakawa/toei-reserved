from day_judge import DayJudge
import jpholiday

# 水曜日かどうかを判定する
class DayJudgeSunday(DayJudge):
 
    @classmethod
    def target_day(cls, date):
        if date.weekday() == 6:
	        return True
        return False