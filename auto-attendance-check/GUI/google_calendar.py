# google calender

import datetime
from datetime import timedelta
from re import T
from googleapiclient.discovery import build
import google.auth
import toml
from typing import List, Tuple, Optional


def entry(date: List[int], table_name: str):
    """
    google calenderに時間割を登録する

    parameter:
        date[]: 登録する日付 ( [0][1][2] : 年月日 )
        table_name: 登録する時間割名
    """
    calendar_id, gapi_creds = auth()
    service = build("calendar", "v3", credentials=gapi_creds)

    event = {
        "summary": table_name,
        "start": {
            "date": datetime.date(date[0], date[1], date[2]).isoformat(),
            "timeZone": "Japan",
        },
        "end": {
            "date": datetime.date(date[0], date[1], date[2]).isoformat(),
            "timeZone": "Japan",
        },
    }

    service.events().insert(calendarId=calendar_id, body=event).execute()


def read(timefrom: str = "") -> Optional[List]:
    """
    カレンダーの現在からの10件の予定を取得する

    parameter:
    num: 取得するイベントの最大数
    return: events (イベント情報のリスト)
    """
    calendar_id, gapi_creds = auth()
    service = build("calendar", "v3", credentials=gapi_creds)

    if timefrom == "":
        timefrom = datetime.datetime.utcnow().isoformat() + "Z"
    else:
        timefrom = (
            datetime.datetime.strptime(timefrom, "%Y-%m-%d") - timedelta(1)
        ).isoformat() + "Z"

    events_result = (
        service.events()
        .list(
            calendarId=calendar_id,
            timeMin=timefrom,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )

    events = events_result.get("items", [])

    return events


def auth() -> Tuple[str, google.auth.credentials.Credentials, Optional[str]]:
    SCOPES = ["https://www.googleapis.com/auth/calendar"]
    gapi_creds = google.auth.load_credentials_from_file("credentials.json", SCOPES)[0]

    with open("calendar_id.toml", "rt") as fp:
        data = toml.load(fp)
    calendar_id = data["calendar_id"]

    return calendar_id, gapi_creds
