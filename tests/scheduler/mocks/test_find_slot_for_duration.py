import pytest

from tests.constants import (
    two_slots_2024_10_10,
    no_slots_2024_10_12,
)


def test_returns_free_slot_with_requested_duration_first_date(scheduler):
    slot = scheduler.find_slot_for_duration(30)

    assert slot

    assert slot[0] == two_slots_2024_10_10
    assert slot[1] == "09:00"
    assert slot[2] == "09:30"


def test_returns_free_slot_with_requested_duration_next_date(scheduler):
    slot = scheduler.find_slot_for_duration(460)

    assert slot

    assert slot[0] == no_slots_2024_10_12
    assert slot[1] == "09:00"
    assert slot[2] == "16:40"


def test_returns_empty_tuple_more_than_work_day(scheduler):
    slot = scheduler.find_slot_for_duration(600)

    assert not slot
