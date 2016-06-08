# coding=utf-8
import datetime
import logging

from fortnox.exceptions import ObjectNotFound
from fortnox.objects.default_object import DefaultObject
from fortnox.requests import Request
from .voucher_row import VoucherRow

logger = logging.getLogger(__name__)


class Voucher(DefaultObject):
    item_url = "/vouchers"
    valid_search_params = DefaultObject.valid_search_params + ['financialyear', 'financialyeardate']

    def __init__(self, json_data = {}):
        self.url = json_data.get('@url')
        self.comments = json_data.get('Comments')
        self.cost_center = json_data.get('CostCenter')
        self.description = json_data.get('Description')
        self.project = json_data.get('Project')
        self.reference_number = json_data.get("ReferenceNumber")
        self.reference_type = json_data.get("ReferenceType")
        if json_data.get("TransactionDate"):
            self.transaction_date = datetime.datetime.strptime(json_data.get("TransactionDate"), "%Y-%m-%d")
        else:
            self.transaction_date = None
        self.voucher_number = json_data.get("VoucherNumber")
        self.voucher_rows = []
        if json_data.get("VoucherRows"):
            for row in json_data.get("VoucherRows"):
                self.voucher_rows.append(VoucherRow(row))
        self.voucher_series = json_data.get("VoucherSeries")
        self.year = json_data.get("Year")

    def __str__(self):
        return "%s" % self.voucher_number if self.voucher_number else ""

    def to_dict(self):
        return {
            "Voucher": {
                "Description": self.description,
                "VoucherSeries": self.voucher_series,
                "TransactionDate": self.transaction_date.strftime("%Y-%m-%d"),
                "VoucherRows": [row.to_dict() for row in self.voucher_rows]
            }
        }

    def _update(self, voucher):
        self.url = voucher.url
        self.comments = voucher.comments
        self.cost_center = voucher.cost_center
        self.description = voucher.description
        self.project = voucher.project
        self.reference_number = voucher.reference_number
        self.reference_type = voucher.reference_type
        self.transaction_date = voucher.transaction_date
        self.voucher_number = voucher.voucher_number
        self.voucher_rows = voucher.voucher_rows
        self.voucher_series = voucher.voucher_series
        self.year = voucher.year

    def create(self):
        response = Request.post(self.item_url, self.to_dict())
        content = response.json()
        logger.debug(content)

        self._update(Voucher(content['Voucher']))

        return self

    @classmethod
    def list(cls, financial_year=None, financial_year_date=None, params={}):
        return_list = []
        search_params = {}
        done = False

        if params:
            for key in params.keys():
                if key in cls.valid_search_params:
                    search_params[key] = params[key]

        if financial_year:
            search_params['financialyear'] = financial_year

        if financial_year_date:
            search_params['financialyeardate'] = financial_year_date

        while not done:
            response = Request.get(cls.item_url, search_params)
            content = response.json()
            logger.debug(content)
            for item in content['Vouchers']:
                return_list.append(Voucher(item))

            if content['MetaInformation']['@TotalPages'] == content['MetaInformation']['@CurrentPage'] or \
                content['MetaInformation']['@TotalPages'] == 0:
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
    def get(cls, voucher_series_code, voucher_number, financial_year=None, financial_year_date=None):
        try:
            params = {}

            if financial_year:
                params['financialyear'] = financial_year

            if financial_year_date:
                params['financialyeardate'] = financial_year_date

            response = Request.get("%s/%s/%s" % (cls.item_url, voucher_series_code, voucher_number), params=params)

            content = response.json()
            logger.debug(content)

            return Voucher(content['Voucher'])

        except ObjectNotFound as e:
            e.message = "Unable to find Voucher with voucher series code: %s, voucher number: %s" % \
                        (voucher_series_code, voucher_number)
            raise e

    @classmethod
    def get(cls, url):
        try:
            response = Request.get(url)
            content = response.json()
            logger.debug(content)

            return Voucher(content['Voucher'])

        except ObjectNotFound as e:
            e.message = "Unable to find Voucher with url: %s" % url
            raise e
