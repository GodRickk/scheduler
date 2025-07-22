import requests


class Scheduler:
    __url: str = ""
    __data: dict[list[dict[int, str, str, str]], list[dict[int, int, str, str]]] = {}
    __days: dict[str, dict[int, str, str, str]] = {}
    __timeslots_by_day = {}

    def __init__(self, url: str):
        self.__url = url
        self.__data = self._load_data()

        for day in self.__data["days"]:
            self.__days[day["date"]] = day

        self.__timeslots_by_day = self._organize_timeslots()

    def get_busy_slots(self, date: str) -> list[tuple[str, str]]:
        if date not in self.__timeslots_by_day:
            return []

        return [(slot["start"], slot["end"]) for slot in self.__timeslots_by_day[date]]

    def get_free_slots(self, date: str) -> list[tuple[str, str]]:
        if date not in self.__days:
            return []

        day = self.__days[date]
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
        if date not in self.__days:
            raise ValueError("date wasn't found in schedule")

        day = self.__days[date]
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

    def _load_data(self):
        try:
            response = requests.get(self.__url)
            response.raise_for_status()
            return response.json()

        except requests.RequestException as e:
            raise Exception(f"Ошибка при загрузке данных: {e}")

    def _organize_timeslots(self):
        timeslots_by_day = {}

        for timeslot in self.__data["timeslots"]:
            day_id = timeslot["day_id"]

            for day in self.__data["days"]:
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
        return self.__data

    def get_days(self):
        return self.__days

    def get_timeslots_by_day(self):
        return self.__timeslots_by_day

    def get_url(self) -> str:
        return self.__url

    def set_url(self, new_url: str):
        self.__url = new_url
