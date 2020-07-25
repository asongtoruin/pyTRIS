import json
from urllib.parse import urljoin
from urllib.request import urlopen


class HTTPRequest:
    BASE_URL = 'http://webtris.highwaysengland.co.uk/api/v{version}/'

    def __init__(self, version, path):
        self.version = version
        self.path = path

    @property
    def url(self):
        return urljoin(self.BASE_URL.format(version=self.version), self.path)

    def fetch(self):
        print(f"Requesting {self.url}")
        resp = urlopen(self.url)

        encoding = resp.info().get_content_charset('utf-8')

        return json.loads(resp.read().decode(encoding))
