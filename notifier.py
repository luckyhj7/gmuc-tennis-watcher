import requests

def notify(topic, title, message, click_url):
    if not topic:
        raise RuntimeError("NTFY_TOPIC is not configured")
    url = "https://ntfy.sh/" + topic
    r = requests.post(url, data=message.encode("utf-8"), headers={
        "Title": title.encode("utf-8"),
        "Click": click_url,
        "Tags": "tennis_ball",
    }, timeout=15)
    r.raise_for_status()
