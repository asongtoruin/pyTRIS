import pytest

from pytris.models import Area


def test_areas_available(latest_api):
    assert callable(getattr(latest_api, 'areas', None))

@pytest.mark.vcr()
def test_get_all_areas(latest_api):
    assert callable(getattr(latest_api.areas(), 'all', None))

    res = latest_api.areas().all()

    # assert isinstance(res, tuple)
    assert all(isinstance(a, Area) for a in res)

@pytest.mark.vcr()
def test_get_one_area(latest_api):
    assert callable(getattr(latest_api.areas(), 'get', None))

    res = latest_api.areas().get(1)

    # assert isinstance(res, tuple)
    assert isinstance(res, Area)