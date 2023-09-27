import pytest

from tilly.api.services.schemas import Timeslots


def test_timeslots(mock_timeslots):
    """Test if Timeslots class works as expected"""
    slots = Timeslots(**mock_timeslots)
    assert True


def test_wrong_input_timeslots():
    """Test if wrong input raises TypeError"""
    with pytest.raises(TypeError):
        Timeslots(**{"ID": "string"})


def test_timeslots_to_frame(mock_timeslots):
    """Test if Timeslots class works as expected"""
    slots = Timeslots(mock_timeslots)
    frame = slots.to_frame()
    assert frame.to_dict(orient="records") == mock_timeslots
