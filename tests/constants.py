from dotenv import load_dotenv

load_dotenv()

test_mock_url = "https://test/"

test_real_api_url = "${API_URL}"


two_slots_2024_10_10 = "2024-10-10"
one_slot_2024_10_11 = "2024-10-11"
no_slots_2024_10_12 = "2024-10-12"

date_out_of_schedule = "2025-12-12"


days = [
    {"id": 1, "date": two_slots_2024_10_10, "start": "09:00", "end": "21:00"},
    {"id": 2, "date": one_slot_2024_10_11, "start": "08:00", "end": "17:00"},
    {"id": 3, "date": no_slots_2024_10_12, "start": "09:00", "end": "18:00"},
]


timesolt_day_1 = [("17:30", "20:00"), ("11:00", "12:00")]

timeslots = [
    {
        "id": 2,
        "day_id": days[0]["id"],
        "start": timesolt_day_1[0][0],
        "end": timesolt_day_1[0][1],
    },
    {
        "id": 1,
        "day_id": days[0]["id"],
        "start": timesolt_day_1[1][0],
        "end": timesolt_day_1[1][1],
    },
    {"id": 3, "day_id": days[1]["id"], "start": "09:30", "end": "16:00"},
]


mock_data = {
    "days": days,
    "timeslots": timeslots,
}
