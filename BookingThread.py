import threading

from utils import BASEURL, GRABURL


class BookingThread(threading.Thread):
    def __init__(
            self, start_time, end_time, session, seat_id, area_id, startDate, endDate
    ):
        threading.Thread.__init__(self)
        self.start_time = start_time
        self.end_time = end_time
        self.session = session
        self.seat_id = seat_id
        self.area_id = area_id
        self.startDate = startDate
        self.endDate = endDate
        self.booking_info = {
            "rooms": [
                {
                    "id": self.seat_id,
                    "officeAreaId": self.area_id,
                    "abilities": ["booking"],
                }
            ],
            "times": [
                {
                    "startDate": self.startDate,
                    "startTime": self.start_time,
                    "endDate": self.endDate,
                    "endTime": self.end_time,
                }
            ],
            "subject": "",
        }

    def run(self):
        r = self.session.post(BASEURL + GRABURL, json=self.booking_info, verify=False)
        print(r.text)
