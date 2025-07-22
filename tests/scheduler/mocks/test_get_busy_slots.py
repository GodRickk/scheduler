import pytest
from tests.conftest import scheduler

from tests.constants import (
    two_slots_2024_10_10,
    no_slots_2024_10_12,
    date_out_of_schedule,
    timesolt_day_1,
)


def test_returns_busy_slots(scheduler):
    busy_slots = scheduler.get_busy_slots(two_slots_2024_10_10)

    assert len(busy_slots) == 2
    assert timesolt_day_1[0] in busy_slots
    assert timesolt_day_1[1] in busy_slots


def test_returns_empty_list(scheduler):
    busy_slots = scheduler.get_busy_slots(no_slots_2024_10_12)

    assert len(busy_slots) == 0


def test_date_out_of_schedule_raise_value_error(scheduler):
    with pytest.raises(ValueError):
        scheduler.get_busy_slots(date_out_of_schedule)
