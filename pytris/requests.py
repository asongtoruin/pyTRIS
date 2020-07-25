import json
from urllib.parse import urljoin, urlencode
from urllib.request import urlopen


class HTTPRequest:
    BASE_URL = 'http://webtris.highwaysengland.co.uk/api/v{version}/'

    def __init__(self, version, path):
        self.version = version
        self.path = path

    @property
    def url(self):
        return urljoin(self.BASE_URL.format(version=self.version), self.path)

    def fetch(self, params=None):
        if params is not None:
            data = urlencode(params)
            url = self.url + f'?{data}'
        else:
            url = self.url
        print(f"Requesting {url}")
        resp = urlopen(url)

        encoding = resp.info().get_content_charset('utf-8')

        return json.loads(resp.read().decode(encoding))
