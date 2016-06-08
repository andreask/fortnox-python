# coding=utf-8
import datetime
import logging

from fortnox.exceptions import ObjectNotFound
from fortnox.objects.default_object import DefaultObject
from fortnox.requests import Request

logger = logging.getLogger(__name__)


class FinancialYear(DefaultObject):
    item_url = '/financialyears'

    valid_search_params = DefaultObject.valid_search_params + ['date', 'fromDate', 'toDate']

    def __init__(self, json_data = {}):
        self.id = json_data.get("Id")
        self.url = json_data.get("@url")
        if json_data.get("FromDate"):
            self.from_date = datetime.datetime.strptime(json_data.get("FromDate"), "%Y-%m-%d")
        else:
            self.from_date = None
        if json_data.get("ToDate"):
            self.to_date = datetime.datetime.strptime(json_data.get("ToDate"), "%Y-%m-%d")
        else:
            self.to_date = None
        self.accounting_method = json_data.get("AccountingMethod")
        self.account_chart_type = json_data.get("AccountChartType")

    def _update(self, financial_year):
        self.id = financial_year.id
        self.url = financial_year.url
        self.from_date = financial_year.from_date
        self.to_date = financial_year.to_date
        self.accounting_method = financial_year.accounting_method
        self.account_chart_type = financial_year.account_chart_type

    def to_dict(self):
        return {
            'FinancialYear': {
                'FromDate': self.from_date.strftime("%Y-%m-%d"),
                'ToDate': self.to_date.strftime("%Y-%m-%d"),
                'AccountingMethod': self.accounting_method,
                'AccountChartType': self.account_chart_type
            }
        }

    def create(self):
        response = Request.post(self.item_url, self.to_dict())
        content = response.json()
        logger.debug(content)

        self._update(FinancialYear(content['FinancialYear']))

        return self

    @classmethod
    def list(cls, params=None):
        return_list = []
        search_params = {}
        done = False

        if params:
            for key in params.keys():
                if key in cls.valid_search_params:
                    search_params[key] = params[key]

        while not done:
            response = Request.get(cls.item_url, search_params)
            content = response.json()
            logger.debug(content)
            for item in content['FinancialYears']:
                return_list.append(FinancialYear(item))

            if content['MetaInformation']['@TotalPages'] == content['MetaInformation']['@CurrentPage']:
                done = True
            else:
                if 'page' in params.keys():
                    done = True
                elif 'limit' in params.keys() and int(params['limit']) == len(return_list):
                    done = True
                elif content['MetaInformation']['@TotalPages'] < content['MetaInformation']['@CurrentPage'] + 1:
                    search_params['page'] = content['MetaInformation']['@CurrentPage'] + 1
                else:
                    done = True

        return return_list

    @classmethod
    def get(cls, id):
        try:
            response = Request.get("%s/%s" % (cls.item_url, id))
            content = response.json()
            logger.debug(content)

            return FinancialYear(content['FinancialYear'])

        except ObjectNotFound as e:
            e.message = "Unable to find Financial year with id: %s" % id
            raise e

