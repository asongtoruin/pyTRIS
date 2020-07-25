import pytest

@pytest.fixture
def latest_api():
    from pytris import API
    from pytris.api import KNOWN_VERSIONS

    return API(version=KNOWN_VERSIONS[-1])