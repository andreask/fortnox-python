# coding=utf-8
import datetime
import json
import unittest
import responses
from fortnox.config import fortnox_config
from fortnox.exceptions import ObjectNotFound
from fortnox.objects import FinancialYear


class FinancialYearTest(unittest.TestCase):
    financial_year_list = {
        "MetaInformation": {
            "@TotalResources": 5,
            "@TotalPages": 1,
            "@CurrentPage": 1
        },
        "FinancialYears": [
            {
                "@url": "https://api.fortnox.se/3/financialyears/5",
                "Id": 5,
                "FromDate": "2013-01-01",
                "ToDate": "2013-12-31",
                "AccountingMethod": "ACCRUAL"
            },
            {
                "@url": "https://api.fortnox.se/3/financialyears/4",
                "Id": 4,
                "FromDate": "2012-01-01",
                "ToDate": "2012-12-31",
                "AccountingMethod": "ACCRUAL"
            },
            {
                "@url": "https://api.fortnox.se/3/financialyears/3",
                "Id": 3,
                "FromDate": "2011-01-01",
                "ToDate": "2011-12-31",
                "AccountingMethod": "ACCRUAL"
            },
            {
                "@url": "https://api.fortnox.se/3/financialyears/2",
                "Id": 2,
                "FromDate": "2010-01-01",
                "ToDate": "2010-12-31",
                "AccountingMethod": "ACCRUAL"
            },
            {
                "@url": "https://api.fortnox.se/3/financialyears/1",
                "Id": 1,
                "FromDate": "2009-01-01",
                "ToDate": "2009-12-31",
                "AccountingMethod": "ACCRUAL"
            }
        ]
    }

    financial_year_single = {
        "FinancialYear": {
            "@url": "https://api.fortnox.se/3/financialyears/1",
            "Id": 1,
            "FromDate": "2009-01-01",
            "ToDate": "2009-12-31",
            "AccountChartType": "Bas 2012",
            "AccountingMethod": "ACCRUAL"
        }
    }

    def setUp(self):
        fortnox_config.access_token = 'access-token'
        fortnox_config.client_secret = 'client-secret'

    def test_to_dict(self):
        financial_year = FinancialYear()
        financial_year.from_date = datetime.datetime.strptime("2016-01-01", "%Y-%m-%d")
        financial_year.to_date = datetime.datetime.strptime("2016-12-31", "%Y-%m-%d")
        financial_year.accounting_method = "ACCRUAL"
        financial_year.account_chart_type = "Bas 2012"

        self.assertEqual({
            'FinancialYear': {
                'FromDate': "2016-01-01",
                'ToDate': "2016-12-31",
                'AccountingMethod': "ACCRUAL",
                'AccountChartType': "Bas 2012"
            }
        }, financial_year.to_dict())

    def test_create(self):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.POST, 'https://api.fortnox.se/3/financialyears',
                     json=self.financial_year_single, status=200,
                     content_type='application/json')

            financial_year = FinancialYear()
            financial_year.account_chart_type = "Bas 2012"
            financial_year.accounting_method = "ACCRUAL"
            financial_year.from_date = datetime.datetime.strptime("2009-01-01", "%Y-%m-%d")
            financial_year.to_date = datetime.datetime.strptime("2009-12-31", "%Y-%m-%d")
            financial_year.create()

            self.assertEqual("https://api.fortnox.se/3/financialyears/1", financial_year.url)
            self.assertEqual(1, financial_year.id)
            self.assertEqual("ACCRUAL", financial_year.accounting_method)
            self.assertEqual("Bas 2012", financial_year.account_chart_type)

            self.assertEqual(1, len(rsps.calls))
            self.assertEqual("https://api.fortnox.se/3/financialyears", rsps.calls[0].request.url)
            self.assertEqual(json.dumps(financial_year.to_dict()), rsps.calls[0].request.body)

    def test_list(self):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, 'https://api.fortnox.se/3/financialyears',
                     json=self.financial_year_list, status=200,
                     content_type='application/json')

            financial_year_array = FinancialYear.list()
            for idx, val in enumerate(financial_year_array):
                self.assertEqual(self.financial_year_list['FinancialYears'][idx]["@url"], val.url)
                self.assertEqual(self.financial_year_list['FinancialYears'][idx]["Id"], val.id)
                self.assertEqual(self.financial_year_list['FinancialYears'][idx]["FromDate"],
                                 val.from_date.strftime("%Y-%m-%d"))
                self.assertEqual(self.financial_year_list['FinancialYears'][idx]["ToDate"],
                                 val.to_date.strftime("%Y-%m-%d"))
                self.assertEqual(self.financial_year_list['FinancialYears'][idx]["AccountingMethod"],
                                 val.accounting_method)

            self.assertEqual(1, len(rsps.calls))
            self.assertEqual("https://api.fortnox.se/3/financialyears", rsps.calls[0].request.url)

    def test_get(self):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, 'https://api.fortnox.se/3/financialyears/1',
                     json=self.financial_year_single, status=200,
                     content_type='application/json')

            financial_year = FinancialYear.get(1)
            self.assertEqual(self.financial_year_single['FinancialYear']["@url"], financial_year.url)
            self.assertEqual(self.financial_year_single['FinancialYear']["Id"], financial_year.id)
            self.assertEqual(self.financial_year_single['FinancialYear']["FromDate"],
                             financial_year.from_date.strftime("%Y-%m-%d"))
            self.assertEqual(self.financial_year_single['FinancialYear']["ToDate"],
                             financial_year.to_date.strftime("%Y-%m-%d"))
            self.assertEqual(self.financial_year_single['FinancialYear']["AccountChartType"],
                             financial_year.account_chart_type)
            self.assertEqual(self.financial_year_single['FinancialYear']["AccountingMethod"],
                             financial_year.accounting_method)

            self.assertEqual(1, len(rsps.calls))
            self.assertEqual("https://api.fortnox.se/3/financialyears/1", rsps.calls[0].request.url)

    def test_invalid_get(self):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, 'https://api.fortnox.se/3/financialyears/1',
                     json={}, status=404,
                     content_type='application/json')

            with self.assertRaises(ObjectNotFound):
                FinancialYear.get(1)
