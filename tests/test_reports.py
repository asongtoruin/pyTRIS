from pandas import DataFrame
import pytest
import vcr

from pytris.errors import DataUnavailableError
from pytris.models import Report, DailyReport, MonthlyReport, AnnualReport


REPORT_CLASSES = ['daily_reports', 'monthly_reports', 'annual_reports']
MODEL_CLASSES = [DailyReport, MonthlyReport, AnnualReport]

PARAMS_DICT = dict(sites=8438, start_date='30122019', end_date='02012020')


def test_reports_available(latest_api):
    for rep in REPORT_CLASSES:
        assert callable(getattr(latest_api, rep, None))


def test_site_type_missing_methods(latest_api):
    # We shouldn't have "all" methods for reports
    for rep in REPORT_CLASSES:
        method = getattr(latest_api, rep)
        with pytest.raises(NotImplementedError):
            method().all()


@pytest.mark.vcr()
def test_get_reports(latest_api):
    for rep, model in zip(REPORT_CLASSES, MODEL_CLASSES):
        method = getattr(latest_api, rep)
        assert callable(getattr(method(), 'get', None))

        res = method().get(**PARAMS_DICT)

        assert isinstance(res, Report)
        assert isinstance(res, model)


@vcr.use_cassette('tests/cassettes/test_get_reports.yaml')
def test_daily_to_frame(latest_api):
    res = latest_api.daily_reports().get(**PARAMS_DICT)

    frame = res.to_frame()

    assert isinstance(frame, DataFrame)


@vcr.use_cassette('tests/cassettes/test_get_reports.yaml')
def test_annual_to_frame(latest_api):
    res = latest_api.annual_reports().get(**PARAMS_DICT)

    frame = res.to_frame()

    assert isinstance(frame, DataFrame)


@vcr.use_cassette('tests/cassettes/test_get_reports.yaml')
def test_monthly_to_frame(latest_api):
    res = latest_api.monthly_reports().get(**PARAMS_DICT)

    frames = res.to_frame()

    expected_names = set((
        'Days', 'Daily Aggregations', 
        'Hourly Aggregations', 'Summary Aggregations'
    ))

    assert set(frames.keys()) == expected_names
    assert all(isinstance(v, DataFrame) for v in frames.values())


def test_missing_param(latest_api):
    for rep, model in zip(REPORT_CLASSES, MODEL_CLASSES):
        method = getattr(latest_api, rep)

        # Try each missing parameter in turn
        for key in PARAMS_DICT.keys():
            partial_dict = {k: v for k, v in PARAMS_DICT.items() if k != key}
            
            with pytest.raises(ValueError) as err:
                method().get(**partial_dict)

            assert key in str(err.value)


@pytest.mark.vcr()
def test_no_data(latest_api):
    for rep, model in zip(REPORT_CLASSES, MODEL_CLASSES):
        method = getattr(latest_api, rep)

        with pytest.raises(DataUnavailableError):
            method().get(
                sites=PARAMS_DICT['sites'], 
                start_date='01012011', end_date='02012011'
            )