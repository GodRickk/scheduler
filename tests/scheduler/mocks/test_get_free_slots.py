import pytest
from tests.conftest import scheduler

from tests.constants import (
    two_slots_2024_10_10,
    no_slots_2024_10_12,
    date_out_of_schedule,
    timeslot_day_1,
)


def test_returns_free_slots(scheduler):
    free_slots = scheduler.get_free_slots(two_slots_2024_10_10)

    day = scheduler.get_days()[two_slots_2024_10_10]

    assert timeslot_day_1[0] not in free_slots
    assert timeslot_day_1[1] not in free_slots

    assert len(free_slots) == 3

    assert (day["start"], timeslot_day_1[0][0]) in free_slots
    assert (timeslot_day_1[0][1], timeslot_day_1[1][0]) in free_slots
    assert (timeslot_day_1[1][1], day["end"]) in free_slots


def test_without_slots_returns_day_start_end(scheduler):
    free_slots = scheduler.get_free_slots(no_slots_2024_10_12)

    day = scheduler.get_days()[no_slots_2024_10_12]

    assert len(free_slots) == 1
    assert free_slots[0] == (day["start"], day["end"])


def test_date_out_of_schedule_raise_value_error(scheduler):
    with pytest.raises(ValueError):
        scheduler.get_free_slots(date_out_of_schedule)
