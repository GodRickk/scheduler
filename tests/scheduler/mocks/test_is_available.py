import pytest
from tests.conftest import scheduler

from tests.constants import (
    two_slots_2024_10_10,
    no_slots_2024_10_12,
    date_out_of_schedule,
    timeslot_free_time_day_1,
    timeslot_day_1,
)


def test_returns_true_for_available_slot(scheduler):
    is_available = scheduler.is_available(
        two_slots_2024_10_10, timeslot_free_time_day_1[0], timeslot_free_time_day_1[1]
    )

    assert is_available is True


def test_returns_true_for_available_slot_whole_day_free(scheduler):
    day = scheduler.get_days()[no_slots_2024_10_12]

    is_available = scheduler.is_available(no_slots_2024_10_12, day["start"], day["end"])

    assert is_available is True


def test_returns_false_for_unavailable_slot_matches_with_busy_time(scheduler):
    busy_start = timeslot_day_1[0][0]
    busy_end = timeslot_day_1[0][1]

    is_available = scheduler.is_available(two_slots_2024_10_10, busy_start, busy_end)

    assert is_available is False


def test_returns_false_for_unavailable_slot_crossing_busy_time_at_start(scheduler):
    is_available = scheduler.is_available(two_slots_2024_10_10, "10:30", "11:30")

    assert is_available is False


def test_returns_false_for_unavailable_slot_crossing_busy_time_at_end(scheduler):
    is_available = scheduler.is_available(two_slots_2024_10_10, "11:30", "12:30")

    assert is_available is False


def test_returns_false_for_unavailable_slot_include_busy_time_at_end(scheduler):
    is_available = scheduler.is_available(two_slots_2024_10_10, "10:30", "12:30")

    assert is_available is False


def test_returns_false_for_unavailable_slot_crossing_two_busy_slots(scheduler):
    is_available = scheduler.is_available(two_slots_2024_10_10, "11:30", "18:00")

    assert is_available is False


def test_returns_false_for_unavailable_slot_whole_day(scheduler):
    day = scheduler.get_days()[two_slots_2024_10_10]

    is_available = scheduler.is_available(
        two_slots_2024_10_10, day["start"], day["end"]
    )

    assert is_available is False


def test_slot_out_of_work_day_raise_value_error(scheduler):
    with pytest.raises(ValueError):
        scheduler.is_available(two_slots_2024_10_10, "08:30", "21:30")


def test_date_out_of_schedule_raise_value_error(scheduler):
    with pytest.raises(ValueError):
        scheduler.is_available(date_out_of_schedule, "some_date", "some_date")
