import time
import requests

BASE = "https://reserve.gmuc.co.kr"
DAY_URL = BASE + "/user/tennis/tennisInsideReservDayCheck.do"
COURT_URL = BASE + "/user/tennis/tennisReservNext0Check.do"

class GmucClient:
    def __init__(self, timeout=15, delay=1.5):
        self.timeout = timeout
        self.delay = delay
        self.s = requests.Session()
        self.s.headers.update({
            "User-Agent": "Mozilla/5.0",
            "Referer": BASE + "/user/tennis/tennisInsideReservation.do?menu=c&menuFlag=T",
            "X-Requested-With": "XMLHttpRequest",
        })

    def _post(self, url, data):
        time.sleep(self.delay)
        r = self.s.post(url, data=data, timeout=self.timeout)
        r.raise_for_status()
        if "text/html" not in r.headers.get("Content-Type", ""):
            raise RuntimeError("Unexpected response content type")
        return r.text

    def get_day(self, yyyymmdd):
        return self._post(DAY_URL, {"reserveDate": yyyymmdd})

    def get_courts(self, time_code, from_time, to_time):
        return self._post(COURT_URL, {
            "timeCode": time_code,
            "fromTime": from_time,
            "toTime": to_time,
            "menuId": "InsideResv",
        })
