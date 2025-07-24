import pytest


def test_real_api_connection(scheduler_with_real_api):
    assert scheduler_with_real_api.get_data() is not None
    assert "days" in scheduler_with_real_api.get_data()
    assert "timeslots" in scheduler_with_real_api.get_data()


def test_real_data_processing(scheduler_with_real_api):
    first_date = list(scheduler_with_real_api.get_days().keys())[0]

    busy_slots = scheduler_with_real_api.get_busy_slots(first_date)
    free_slots = scheduler_with_real_api.get_free_slots(first_date)

    assert isinstance(busy_slots, list)
    assert isinstance(free_slots, list)
