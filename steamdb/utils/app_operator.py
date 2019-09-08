#! /usr/bin/python3.7

import requests

from .constants import Constants


class AppOperator(object):

    def __init__(self):
        self.api_key = Constants.API_KEY
        self.steam_id = Constants.STEAM_ID
        self.api_host = "https://api.steampowered.com"
        self.store_host = "https://store.steampowered.com/api"

    def _request(self, url, method, kwargs):
        resp = requests.request(method, url, **kwargs)
        if 200 <= resp.status_code < 300:
            return True, resp.json()
        else:
            return False, {}

    def get_app_list(self):
        """get all app list

        method : GET
        interface : ISteamApps
        action : GetAppList
        :return:
        """
        method = "GET"
        interface = "ISteamApps"
        action = "GetAppList"
        version = "v2"
        suffix = "?key=%s" % self.api_key
        kwargs = {}

        req_url = "/".join([self.api_host, interface, action, version, suffix])
        ret, content = self._request(req_url, method, kwargs)
        return content.get("applist").get("apps").get("app")

    def get_app_info(self, app_id):
        """get full app info

        :param app_id:
        :return:
        """
        method = "GET"
        interface = "appdetails"
        suffix = "?appids=%s" % app_id
        kwargs = {}

        req_url = "/".join([self.store_host, interface, suffix])
        ret, content = self._request(req_url, method, kwargs)
        return content
