import warnings

from .errors import UnknownVersionWarning


KNOWN_VERSIONS = ['1.0']

class API:
    def __init__(self, version: str):
        if version not in KNOWN_VERSIONS:
            warnings.warn(
                f'API version "{version}" has not been tested with these '
                f'methods. Performance cannot be guaranteed (known versions: '
                f'{",".join(KNOWN_VERSIONS)})',
                UnknownVersionWarning, stacklevel=2
            )
        self._base_url = f'http://webtris.highwaysengland.co.uk/api/v{version}'
