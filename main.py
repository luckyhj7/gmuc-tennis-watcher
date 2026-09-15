import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import yaml
from gmuc import GmucClient, BASE
from parser import available_times, available_courts
from notifier import notify

STATE = Path("state.json")
BOOKING_URL = BASE + "/user/tennis/tennisInsideReservation.do?menu=c&menuFlag=T"

def load_state():
    try:
        return set(json.loads(STATE.read_text(encoding="utf-8")))
    except Exception:
        return set()

def save_state(items):
    STATE.write_text(json.dumps(sorted(items), ensure_ascii=False, indent=2), encoding="utf-8")

def main():
    cfg = yaml.safe_load(Path("config.yaml").read_text(encoding="utf-8"))
    tz = ZoneInfo(cfg["timezone"])
    today = datetime.now(tz).date()
    client = GmucClient(**{
        "timeout": cfg["request"]["timeout_seconds"],
        "delay": cfg["request"]["delay_seconds"],
    })
    seen = load_state()
    current = set()
    topic = os.environ.get("NTFY_TOPIC", "")
    exclude = set(cfg["exclude_courts"])

    for offset in range(cfg["lookahead_days"] + 1):
        d = today + timedelta(days=offset)
        day_key = d.strftime("%a").upper()
        wanted = set(cfg["schedule"].get(day_key, []))
        if not wanted:
            continue

        html = client.get_day(d.strftime("%Y%m%d"))
        for slot in available_times(html):
            slot_key = f'{slot["from"]}-{slot["to"]}'
            if slot_key not in wanted:
                continue
            courts_html = client.get_courts(slot["code"], slot["from"], slot["to"])
            for court in available_courts(courts_html):
                if court["no"] in exclude:
                    continue
                key = f'{d.isoformat()}|{slot_key}|{court["no"]}'
                current.add(key)
                if key not in seen:
                    title = "광명 테니스 빈자리"
                    msg = f'{d:%Y-%m-%d} {slot_key} / {court["no"]}번 코트'
                    print("FOUND", msg)
                    notify(topic, title, msg, BOOKING_URL)

    save_state(current)

if __name__ == "__main__":
    main()
