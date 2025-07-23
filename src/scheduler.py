import requests
from src.utils.validation import validate_date_in_schedule


class Scheduler:
    def __init__(self, url: str):
        self._url: str = url
        self._data: dict[
            list[dict[int, str, str, str]], list[dict[int, int, str, str]]
        ] = self._load_data()

        self._days: dict[str, list[dict[int, str, str, str]]] = {}

        for day in self._data["days"]:
            self._days[day["date"]] = day

        self._timeslots_by_day = self._organize_timeslots()

    def get_busy_slots(self, date: str) -> list[tuple[str, str]]:
        validate_date_in_schedule(date, self._days)

        if date not in self._timeslots_by_day:
            return []

        return [(slot["start"], slot["end"]) for slot in self._timeslots_by_day[date]]

    def get_free_slots(self, date: str) -> list[tuple[str, str]]:
        validate_date_in_schedule(date, self._days)

        day = self._days[date]
        work_start = self._time_to_minutes(day["start"])
        work_end = self._time_to_minutes(day["end"])

        busy_slots = self.get_busy_slots(date)
        if not busy_slots:
            return [(day["start"], day["end"])]

        free_slots = []
        current_time = work_start

        for busy_start, busy_end in busy_slots:
            busy_start_minutes = self._time_to_minutes(busy_start)
            busy_end_minutes = self._time_to_minutes(busy_end)

            if current_time < busy_start_minutes:
                free_slots.append(
                    (
                        self._minutes_to_time(current_time),
                        self._minutes_to_time(busy_start_minutes),
                    )
                )

            current_time = busy_end_minutes

        if current_time < work_end:
            free_slots.append(
                (self._minutes_to_time(current_time), self._minutes_to_time(work_end))
            )

        return free_slots

    def is_available(self, date: str, start_time: str, end_time: str) -> bool:
        validate_date_in_schedule(date, self._days)

        day = self._days[date]
        work_start = self._time_to_minutes(day["start"])
        work_end = self._time_to_minutes(day["end"])

        slot_start = self._time_to_minutes(start_time)
        slot_end = self._time_to_minutes(end_time)

        if slot_start < work_start or slot_end > work_end:
            raise ValueError("requested slot out of work day")

        busy_slots = self.get_busy_slots(date)
        for busy_start, busy_end in busy_slots:
            busy_start_minutes = self._time_to_minutes(busy_start)
            busy_end_minutes = self._time_to_minutes(busy_end)

            if slot_end > busy_start_minutes and slot_start < busy_end_minutes:
                return False

        return True

    def find_slot_for_duration(self, duration_minutes: int):
        sorted_dates = sorted(self._days.keys())

        for date in sorted_dates:
            free_slots = self.get_free_slots(date)

            for free_start, free_end in free_slots:
                start_minutes = self._time_to_minutes(free_start)
                end_minutes = self._time_to_minutes(free_end)

                if end_minutes - start_minutes >= duration_minutes:
                    found_start = self._minutes_to_time(start_minutes)
                    found_end = self._minutes_to_time(start_minutes + duration_minutes)
                    return (date, found_start, found_end)

        return ()

    def _load_data(self):
        try:
            response = requests.get(self._url)
            response.raise_for_status()
            return response.json()

        except requests.RequestException as e:
            raise Exception(f"Error loading data: {e}")

    def _organize_timeslots(self):
        timeslots_by_day = {}

        for timeslot in self._data["timeslots"]:
            day_id = timeslot["day_id"]

            for day in self._data["days"]:
                if day_id == day["id"]:
                    date = day["date"]

                    if date not in timeslots_by_day:
                        timeslots_by_day[date] = []

                    timeslots_by_day[date].append(timeslot)
                    break

        for date in timeslots_by_day:
            timeslots_by_day[date].sort(key=lambda x: x["start"])

        return timeslots_by_day

    def _time_to_minutes(self, time_str: str) -> int:
        hours, minutes = map(int, time_str.split(":"))
        return hours * 60 + minutes

    def _minutes_to_time(self, minutes: int) -> str:
        hours = minutes // 60
        mins = minutes % 60
        return f"{hours:02d}:{mins:02d}"

    def get_data(self):
        return self._data

    def get_days(self):
        return self._days

    def get_timeslots_by_day(self):
        return self._timeslots_by_day

    def get_url(self) -> str:
        return self._url
