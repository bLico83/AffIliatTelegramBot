import json
import requests
import sys

from backports.configparser import ConfigParser

class AliExpressApi(object):
    API_URL_BASE = 'http://gw.api.alibaba.com/openapi/param2/2/portals.open/'

    def __init__(self):
        self._read_config()

    def _read_config(self):
        """Reads the config file with the API keys which should be placed where aliexpress_api.py is"""
        import os
        file_path = os.path.join(os.path.dirname(__file__), './config.ini')
        config = ConfigParser()
        config.read(file_path)
        self._appkey = config.get('AliExpress', 'appkey')
        self._tracking_id = config.get('AliExpress', 'trackingId')

    @staticmethod #is this necesary?
    def _query_json_api(url, params):
        """Queries a JSON API"""
        response = requests.get(url=url, params=params)
        data = json.loads(response.text)
        return data

    def get_promotion_link(self, product_link):
        """Transforms a regular link into a promotion / referral link"""
        promotion_link_url = self.API_URL_BASE + 'api.getPromotionLinks/' + self._appkey

        params = dict(
            trackingId=self._tracking_id,
            urls=product_link,
        )
        result = self._query_json_api(promotion_link_url, params)['result']
        return result['promotionUrls'][0]['promotionUrl']

    @staticmethod
    def get_product_id_from_link(link):
        """Returns the product id from a regular AliExpress link"""
        import re
        match = re.search(r'.*\.aliexpress\.com/item/.*/(\d*)\.html.*', link)
        return match.group(1)
