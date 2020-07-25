import pytest

from pytris.models import Site


def test_sites_available(latest_api):
    assert callable(getattr(latest_api, 'sites', None))


@pytest.mark.vcr()
def test_get_all_sites(latest_api):
    assert callable(getattr(latest_api.sites(), 'all', None))

    res = latest_api.sites().all()

    assert all(isinstance(a, Site) for a in res)


@pytest.mark.vcr()
def test_get_one_site(latest_api):
    assert callable(getattr(latest_api.sites(), 'get', None))

    res = latest_api.sites().get(1)

    assert isinstance(res, Site)