import warnings

from .errors import UnknownVersionWarning


KNOWN_VERSIONS = ['1.0']

class API:
    def __init__(self, version: str):
        if version not in KNOWN_VERSIONS:
            warnings.warn(
                f'Version {version} has not been tested with these methods.'
                f'Performance cannot be guaranteed (known versions: {",".join(KNOWN_VERSIONS)})',
                UnknownVersionWarning
            )
        self._base_url = f'http://webtris.highwaysengland.co.uk/api/v{version}'
