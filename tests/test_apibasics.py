import warnings

from pytris import API
from pytris.errors import UnknownVersionWarning


def test_api_known():
    api = API('1.0')

    assert hasattr(api, '_base_url')
    assert isinstance(api._base_url, str)


def test_api_unknown(recwarn):
    warnings.simplefilter('always')

    api = API('Adam')

    assert len(recwarn) == 1
    assert recwarn.pop(UnknownVersionWarning)
