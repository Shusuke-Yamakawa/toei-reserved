from day_judge import DayJudge
import jpholiday

# 水曜日かどうかを判定する
class DayJudgeMiddleWeek(DayJudge):
 
    @classmethod
    def target_day(cls, date):
        if 0 < date.weekday() < 4:
	        return True
        return False