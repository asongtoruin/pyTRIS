import json
from urllib.parse import urljoin 
from urllib.request import urlopen
import warnings

from .errors import UnknownVersionWarning
from .areas import AreaMixin


KNOWN_VERSIONS = ['1.0']

class API(AreaMixin, object):
    def __init__(self, version: str):
        if version not in KNOWN_VERSIONS:
            warnings.warn(
                f'API version "{version}" has not been tested with these '
                f'methods. Performance cannot be guaranteed (known versions: '
                f'{",".join(KNOWN_VERSIONS)})',
                UnknownVersionWarning, stacklevel=2
            )
        self._base_url = f'http://webtris.highwaysengland.co.uk/api/v{version}/'

    def _get(self, endpoint, **kwargs):
        url = urljoin(self._base_url, endpoint)

        resp = urlopen(url)

        encoding = resp.info().get_content_charset('utf-8')

        return json.loads(resp.read().decode(encoding))
