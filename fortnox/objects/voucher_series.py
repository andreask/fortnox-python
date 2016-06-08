# coding=utf-8
import logging

from fortnox.exceptions import ObjectNotFound
from fortnox.objects.default_object import DefaultObject
from fortnox.requests import Request

logger = logging.getLogger(__name__)


class VoucherSeries(DefaultObject):
    item_url = "/voucherseries"

    def __init__(self, json_data = {}):
        self.url = json_data.get("@url")
        self.code = json_data.get("Code")
        self.description = json_data.get("Description")
        self.manual = json_data.get("Manual")
        self.next_voucher_number = json_data.get("NextVoucherNumber")
        self.year = json_data.get("year")

    def __str__(self):
        return self.code if self.code else ""

    def to_dict(self):
        return {
            'VoucherSeries': {
                'Code': self.code,
                'Description': self.description,
                'Manual': self.manual
            }
        }

    def _update(self, voucher_series):
        self.url = voucher_series.url
        self.code = voucher_series.code
        self.manual = voucher_series.manual
        self.description = voucher_series.description
        self.next_voucher_number = voucher_series.next_voucher_number
        self.year = voucher_series.year

    def create(self):
        response = Request.post(self.item_url, self.to_dict())
        content = response.json()
        logger.debug(content)

        self._update(VoucherSeries(content['VoucherSeries']))

        return self

    def save(self):
        try:
            response = Request.put("%s/%s" % (self.item_url, self.code), self.to_dict())
            content = response.json()
            logger.debug(content)

            self._update(VoucherSeries(content['VoucherSeries']))

            return self

        except ObjectNotFound as e:
            e.message = "Unable to find Voucher series with code: %s" % self.code
            raise e

    @classmethod
    def list(cls):
        return_list = []

        response = Request.get(cls.item_url)
        content = response.json()
        logger.debug(content)
        for item in content['VoucherSeriesCollection']:
            return_list.append(VoucherSeries(item))

        return return_list

    @classmethod
    def get(cls, code):
        try:
            response = Request.get("%s/%s" % (cls.item_url, code))
            content = response.json()
            logger.debug(content)

            return VoucherSeries(content['VoucherSeries'])

        except ObjectNotFound as e:
            e.message = "Unable to find Voucher series with code: %s" % code
            raise e

