import logging
import requests

from fortnox.config import fortnox_config as cfg
from fortnox.exceptions import ObjectNotFound

logger = logging.getLogger(__name__)


class Request:
    server_url = "https://api.fortnox.se/3"

    @classmethod
    def delete(cls, url):
        logging.info("DELETE: %s" % url)
        if url.startswith("http"):
            response = requests.delete(url, headers=cfg.to_dict())
        else:
            response = requests.delete("%s%s" % (cls.server_url, url), headers=cfg.to_dict())
        logging.info(response.json())
        response.raise_for_status()
        return response

    @classmethod
    def get(cls, url, params = {}):
        logging.info("GET: url: %s, params: %s" % (url, params))
        if url.startswith("http"):
            response = requests.get(url, params, headers=cfg.to_dict())
        else:
            response = requests.get("%s%s" % (cls.server_url, url), params, headers=cfg.to_dict())
        logging.info(response.json())
        if response.status_code == 404:
            raise ObjectNotFound
        else:
            response.raise_for_status()
        return response

    @classmethod
    def post(cls, url, data):
        logging.info("POST: url: %s, data: %s" % (url, data))
        if url.startswith("http"):
            response = requests.post(url, headers=cfg.to_dict(), json=data)
        else:
            response = requests.post("%s%s" % (cls.server_url, url), headers=cfg.to_dict(), json=data)
        logging.info(response.json())
        if response.status_code == 400:
            logger.error(response.json())
        response.raise_for_status()
        return response

    @classmethod
    def put(cls, url, data):
        logging.info("PUT: url: %s, data: %s" % (url, data))
        if url.startswith("http"):
            response = requests.put(url, headers=cfg.to_dict(), json=data)
        else:
            response = requests.put("%s%s" % (cls.server_url, url), headers=cfg.to_dict(), json=data)
            logging.info(response.json())
        if response.status_code == 404:
            raise ObjectNotFound
        else:
            response.raise_for_status()
        return response
