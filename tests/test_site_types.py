import pytest

from pytris.models import SiteType, Site


def test_site_types_available(latest_api):
    assert callable(getattr(latest_api, 'site_types', None))


def test_site_type_missing_methods(latest_api):
    with pytest.raises(NotImplementedError):
        latest_api.site_types().get()


@pytest.mark.vcr()
def test_get_all_site_types(latest_api):
    assert callable(getattr(latest_api.site_types(), 'all', None))

    res = latest_api.site_types().all()

    assert all(isinstance(a, SiteType) for a in res)


@pytest.mark.vcr()
def test_get_one_site_type(latest_api):
    assert callable(getattr(latest_api.site_types(), 'get_children', None))

    res = latest_api.site_types().get_children(1)

    assert all(isinstance(a, Site) for a in res)
