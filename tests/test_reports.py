import pytest

from pytris.models import Report, DailyReport, MonthlyReport, AnnualReport


REPORT_CLASSES = ['daily_reports', 'monthly_reports', 'annual_reports']
MODEL_CLASSES = [DailyReport, MonthlyReport, AnnualReport]


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

        res = method().get(
            sites=8438, start_date='30122019', end_date='02012020'
        )

        assert isinstance(res, Report)
        assert isinstance(res, model)


def test_missing_param(latest_api):
    for rep, model in zip(REPORT_CLASSES, MODEL_CLASSES):
        method = getattr(latest_api, rep)

        params_dict = {
            'sites': 8438,
            'start_date': '30122019',
            'end_date': '02012019'
        }

        for key in params_dict.keys():
            partial_dict = {k: v for k, v in params_dict.items() if k != key}
            
            with pytest.raises(ValueError) as err:
                method().get(**partial_dict)

            assert key in str(err.value)