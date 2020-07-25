import warnings

from pytris import API
from pytris.errors import UnknownVersionWarning


def test_api_known(latest_api):
    assert hasattr(latest_api, 'version')
    assert isinstance(latest_api.version, str)


def test_api_unknown(recwarn):
    warnings.simplefilter('always')

    api = API('Adam')

    assert len(recwarn) == 1
    assert recwarn.pop(UnknownVersionWarning)
