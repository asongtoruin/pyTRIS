import pytest

from pytris.api import API, KNOWN_VERSIONS
from pytris.models import Area


@pytest.mark.vcr()
def test_get_all_areas(latest_api):

    res = latest_api.areas().all()

    # assert isinstance(res, tuple)
    assert all(isinstance(a, Area) for a in res)