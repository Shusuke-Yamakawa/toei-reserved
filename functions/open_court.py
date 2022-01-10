from day_judge_tuesday import DayJudgeTuesday
from day_judge_middle_week import DayJudgeMiddleWeek
from day_judge_sunday import DayJudgeSunday
from day_judge_saturday import DayJudgeSaturday
from day_judge_wednesday import DayJudgeWednesday
from day_judge_holiday import DayJudgeHoliday
from selenium.webdriver.common.keys import Keys
import requests
import time
import jpholiday
import datetime
from datetime import date, timedelta
import calendar
import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import sys
sys.path.append("../")

class GetOpenCourt:
    COURT_TYPES = {"ハード": "2-1000-1020", "人工芝": "2-1000-1030"}

    TARGET_COURT = ['井の頭恩賜公園', '野川公園', '小金井公園', '府中の森公園', '武蔵野中央公園']

    USER_ID = "86329044"
    PASSWD = "19870513"

    RETRY_USER_ID = "86560751"
    RETRY_PASSWD = "19550223"

    RETRY2_USER_ID = "86329053"
    RETRY2_PASSWD = "19470602"

    GET_LIMIT_DAY = 5
    NOTIFY_OPEN_COURT = 5

    TOEI_URL = "https://yoyaku.sports.metro.tokyo.lg.jp/"

    LINE_NOTIFY_TOKEN = 'Qeuzd60OWvkoG0ZbctkpkkWFb9fUmYJYcTDBujxypsV'
    LINE_NOTIFY_API = 'https://notify-api.line.me/api/notify'

    def __init__(self, from_time, to_time, court, target_day):
        chrome_options = webdriver.ChromeOptions()

        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1280x1696')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--hide-scrollbars')
        chrome_options.add_argument('--enable-logging')
        chrome_options.add_argument('--log-level=0')
        chrome_options.add_argument('--v=99')
        chrome_options.add_argument('--single-process')
        chrome_options.add_argument('--ignore-certificate-errors')

        chrome_options.binary_location = os.getcwd() + "/headless-chromium"    
        self.driver = webdriver.Chrome(os.getcwd() + "/chromedriver",chrome_options=chrome_options)
        self.driver.implicitly_wait(1)
        
        self.from_time = from_time
        self.to_time = to_time
        self.court = court
        self.court_string = self.COURT_TYPES[self.court]
        self.target_day = target_day
        self.day = ""

    # public method

    def run(self):
        try:
            now = datetime.datetime.now()
            msg = "今月{0}-{1}時の空きテニスコート({2}・{3}) {4} 現在\n".format(
                self.from_time, self.to_time, self.court, self.target_day, now.strftime("%Y-%m-%d %H:%M:%S"))
            msg += self.TOEI_URL
            msg += self.search_by_target_day(now.year, now.month, now.day)
            print(msg)
            if msg.find('空きコートあり！！') != -1:
                self.post_process(msg, now.year, now.month)
            if now.day >= 22:
                msg = "来月{0}-{1}時の空きテニスコート({2}) {3} 現在\n".format(
                    self.from_time, self.to_time, self.court, now.strftime("%Y-%m-%d %H:%M:%S"))
                msg += self.TOEI_URL
                year = now.year + 1 if now.month == 12 else now.year
                month = 1 if now.month == 12 else now.month + 1
                msg += self.search_by_target_day(year, month, 1)
                print(msg)
                if msg.find('空きコートあり！！') != -1:
                    self.post_process(msg, year, month)
        except Exception as e:
            tb = sys.exc_info()[2]
            print("\n" + "--------------" + "\n" +
                  "エラーメッセージ:{0}".format(e.with_traceback(tb)))
        finally:
            self.driver.close()
            self.driver.quit()
            return

    # private method

    # 検索対象の日にちを絞り込み、検索処理を実行する
    def search_by_target_day(self, year, month, day):
        msg = ""
        for day in self._handle_dates(year, month, day):
            day_type_list = {"Holiday": DayJudgeHoliday, "Wednesday": DayJudgeWednesday,
                             "Tuesday": DayJudgeTuesday, "MiddleWeek": DayJudgeMiddleWeek,
                             "Saturday": DayJudgeSaturday, "Sunday": DayJudgeSunday}
            if month == 12 and day == 30: msg += self.search_open_court(year, month, day)
            if self.target_day in day_type_list:
                day_judge = day_type_list[self.target_day]
            else:
                # 指定がなかった場合は、全ての日をターゲットとする
                msg += self.search_open_court(year, month, day)
            if day_judge.target_day(datetime.date(year, month, day)):
                msg += self.search_open_court(year, month, day)
        # コートが取得できた場合、印をつけておく
        if not msg:
            return ""
        else:
            msg += "\n" + "空きコートあり！！"
            return msg

    def search_open_court(self, year, month, day):
        self.driver.get(self.TOEI_URL + "user/view/user/homeIndex.html")
        web_elements = self.search_day_time(year, month, day)
        # 曜日を求める
        week = self._handle_week(year, month, day)
        msg = self.write_open_court(day, week, web_elements)

        # 次のページがある場合実行する
        while True:
            try:
                self.driver.find_element_by_id('goNextPager').click()
                web_elements = self.driver.find_elements_by_id("bnamem")
                msg += self.write_open_court(day, week, web_elements)
            except NoSuchElementException:
                # 次のページが押せなくなったらループから抜ける
                break
        return msg

    # 対象のコートの空きがある場合、msgに情報を記録する
    def write_open_court(self, day, week, web_elements):
        if len(web_elements) > 0:
            for e in web_elements:
                # 指定したコートの場合のみ表示させる
                if(self.target_court(e.text)):
                    continue
                else:
                    self.day = day
                    msg = "\n" + "{0}({1}) : {2}".format(day, week, e.text)
                    return msg
        return ""

    def target_court(self, openCourt):
        if openCourt in self.TARGET_COURT:
            return False
        return True

    def search_day_time(self, year, month, day):
        self.driver.find_element_by_id('dateSearch').click()
        self.driver.find_element_by_name(
            'layoutChildBody:childForm:year').send_keys(str(year))
        self.driver.find_element_by_name(
            'layoutChildBody:childForm:month').send_keys(str(month) + "月")
        self.driver.find_element_by_name(
            'layoutChildBody:childForm:day').send_keys(str(day) + "日")
        self.driver.find_element_by_name(
            'layoutChildBody:childForm:sHour').send_keys(str(self.from_time) + "時")
        self.driver.find_element_by_name(
            'layoutChildBody:childForm:eHour').send_keys(str(self.to_time) + "時")
        self.driver.find_element_by_xpath(
            "//input[@value='{0}']".format(self.court_string)).click()
        self.driver.find_element_by_id('srchBtn').click()
        return self.driver.find_elements_by_id("bnamem")

    def post_process(self, msg, year, month):
        self.driver.get(self.TOEI_URL + "user/view/user/homeIndex.html")
        today = date.today()
        # 指定した日以内であれば予約する
        limit_day = today + timedelta(self.GET_LIMIT_DAY)
        target_dt = datetime.date(year, month, self.day)
        if target_dt > limit_day:
            msg = self.now_reserve(msg, year, month, False)
        # LINEに結果を通知する
        payload = {'message': msg}
        headers = {'Authorization': 'Bearer ' + self.LINE_NOTIFY_TOKEN}  # 発行したトークン
        notify_day = today + timedelta(self.NOTIFY_OPEN_COURT)
        if target_dt > notify_day:
            line_notify = requests.post(
                self.LINE_NOTIFY_API, data=payload, headers=headers)

    def now_reserve(self, msg, year, month, retry):
        self.driver.find_element_by_id('login').click()
        # コートが重複してリトライする場合は、サブのユーザーで実行する
        if retry:
            if msg.count('重複してます') == 1:
                self.driver.find_element_by_id(
                    'userid').send_keys(self.RETRY_USER_ID)
                self.driver.find_element_by_id(
                    'passwd').send_keys(self.RETRY_PASSWD)
            elif msg.count('重複してます') == 2:
                self.driver.find_element_by_id(
                    'userid').send_keys(self.RETRY2_USER_ID)
                self.driver.find_element_by_id(
                    'passwd').send_keys(self.RETRY2_PASSWD)
            else:
                msg += '全て重複しています。'
                return
        else:
            self.driver.find_element_by_id('userid').send_keys(self.USER_ID)
            self.driver.find_element_by_id('passwd').send_keys(self.PASSWD)
        time.sleep(3)
        self.driver.find_element_by_id('login').click()
        web_elements = self.search_day_time(year, month, self.day)
        msg = self.reserve_court(web_elements, msg, year, month)
        # 次のページがある場合実行する
        while True:
            try:
                self.driver.find_element_by_id('goNextPager').click()
                web_elements = self.driver.find_elements_by_id("bnamem")
                msg = self.reserve_court(web_elements, msg, year, month)
            except NoSuchElementException:
                # 次のページが押せなくなったらループから抜ける
                break
        return msg

    def reserve_court(self, web_elements, msg, year, month):
        if len(web_elements) > 0:
            for e in web_elements:
                # 指定したコートの場合のみ表示させる
                if(self.target_court(e.text)):
                    continue
                else:
                    icon_elements = self.driver.find_elements_by_id(
                        'emptyStateIcon')
                    if len(icon_elements) > 0:
                        for i in icon_elements:
                            icon = i.get_attribute("alt")
                            if (icon == "空き"):
                                i.click()
                                break
                    self.driver.find_element_by_id('doReserve').click()
                    try:
                        self.driver.find_element_by_id('apply').click()
                        apply_conf = self.driver.find_elements_by_id('apply')
                        # 同日日時に別コートが取得されている場合を考慮
                        if len(apply_conf) > 0:
                            msg += "\n" + "重複してます"
                            self.driver.find_element_by_xpath(
                                "//input[@value='ログアウト']").click()
                            msg = self.now_reserve(msg, year, month, True)
                        else:
                            msg += "\n予約済\nFunctions"
                        return msg
                    except NoSuchElementException:
                        msg += "\n" + "予約取れず"
                        return msg
        return msg

    # static method

    @staticmethod
    def _handle_dates(year, month, day):
        mr = calendar.monthrange(year, month)
        # システム予約は2日前までなので、2日後以降を対象とする ※翌月の場合は、1日から対象とする
        day = day+2 if day != 1 else day
        return range(day, mr[1] + 1)

    @staticmethod
    def _handle_week(year, month, day):
        d = datetime.datetime(year, month, day, 0, 0, 0)
        week = ["月", "火", "水", "木", "金", "土", "日"]
        return week[d.weekday()]
