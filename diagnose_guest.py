from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import re
import requests
from parser import available_times, available_courts

BASE = "https://reserve.gmuc.co.kr"
DAY = BASE + "/user/tennis/tennisInsideReservDayCheck.do"
COURT = BASE + "/user/tennis/tennisReservNext0Check.do"

def looks_like_login(r):
    u = r.url.lower()
    body = r.text.lower()
    return ("login" in u or "loginproc" in body or
            ("아이디" in r.text and "비밀번호" in r.text))

def post(session, url, data):
    r = session.post(url, data=data, timeout=20, allow_redirects=True)
    print("  status=", r.status_code, "final_url=", r.url,
          "content_type=", r.headers.get("content-type", ""),
          "bytes=", len(r.content), "login_page=", looks_like_login(r))
    r.raise_for_status()
    return r

def main():
    # Deliberately fresh anonymous session: no ID/PW, no copied JSESSIONID.
    s = requests.Session()
    s.headers.update({
        "User-Agent": "Mozilla/5.0",
        "Referer": BASE + "/user/tennis/tennisReservation.do?menu=d&menuFlag=T",
        "X-Requested-With": "XMLHttpRequest",
    })
    now = datetime.now(ZoneInfo("Asia/Seoul")).date()
    candidates = []
    for i in range(15):
        d = now + timedelta(days=i)
        if d.weekday() in (1, 3, 5):  # Tue Thu Sat
            candidates.append(d)

    proved_time = False
    proved_court = False
    for d in candidates:
        print("\nDATE", d.isoformat(), d.strftime("%a"))
        r = post(s, DAY, {"reserveDate": d.strftime("%Y%m%d")})
        times = available_times(r.text)
        tm_ids = sorted(set(re.findall(r"TM\d+", r.text)))
        print("  TM ids:", tm_ids[:20], "count=", len(tm_ids))
        print("  available choiceTime:", times)
        if looks_like_login(r):
            raise SystemExit("FAIL: day request redirected/returned login page")
        if tm_ids:
            proved_time = True

        for slot in times[:3]:
            print("  COURT QUERY", slot)
            cr = post(s, COURT, {
                "timeCode": slot["code"],
                "fromTime": slot["from"],
                "toTime": slot["to"],
                "menuId": "InsideResv",
            })
            courts = available_courts(cr.text)
            tc_ids = sorted(set(re.findall(r"TC\d+", cr.text)))
            print("    TC ids:", tc_ids[:20], "count=", len(tc_ids))
            print("    available choiceCourt:", courts)
            if looks_like_login(cr):
                raise SystemExit("FAIL: court request redirected/returned login page")
            if tc_ids:
                proved_court = True
                break
        if proved_time and proved_court:
            break

    print("\nRESULT")
    print("guest_time_structure=", proved_time)
    print("guest_court_structure=", proved_court)
    if not proved_time:
        raise SystemExit("INCONCLUSIVE: no TM time structure found in anonymous responses")
    if not proved_court:
        raise SystemExit("INCONCLUSIVE: no available time yielded TC court structure")
    print("PASS: anonymous fresh session returned both time and court structures")

if __name__ == "__main__":
    main()
