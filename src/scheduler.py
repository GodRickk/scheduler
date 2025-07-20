import requests

test_url = "https://ofc-test-01.tspb.su/test-task/"


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

    def _load_data(self) -> dict:
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

    def get_data(self):
        return self.__data

    def get_days(self):
        return self.__days

    def get_timeslots_by_day(self):
        return self.__timeslots_by_day


scheduler = Scheduler(test_url)

print("row data", scheduler.get_data())

print()

print("date - day", scheduler.get_days())

print()

print("date - timeslot", scheduler.get_timeslots_by_day())
