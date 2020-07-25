import pytest

from pytris.api import API, KNOWN_VERSIONS
from pytris.areas import Area


@pytest.mark.vcr()
def test_get_all_areas():
    # Use latest known API version
    api = API(KNOWN_VERSIONS[-1])

    res = api.get_all_areas()

    assert isinstance(res, tuple)
    assert all(isinstance(a, Area) for a in res)