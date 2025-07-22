def validate_date_in_schedule(
    date: str, days: dict[str, list[dict[int, str, str, str]]]
):
    if date not in days:
        raise ValueError("date wasn't found in schedule")
