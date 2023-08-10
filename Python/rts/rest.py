#!/usr/bin/env python
import json
import requests


class R2RestClient(object):
    def __init__(self, base_url, **kwargs):
        self.verify = kwargs.get("verify")
        self.base_url = base_url
        if self.verify is None:
            self.verify= True
        self.json_header = {
            "Content-Type": "application/json",
            "Accept": "text/plain"
        }

    def build_path(self, route):
        if len(route) == 0 or route == "/":
            return self.base_url
        elif route[0] == "/":
            return "/".join([self.base_url, route[1:]])
        else:
            return "/".join([self.base_url, route])

    def convert_dict_to_json_string(self, data, headers, verify):
        if data is not None and type(data) is dict:
            data = json.dumps(data)
            if headers is None:
                headers = self.json_header
            else:
                headers.update(self.json_header)
        if verify is None:
            verify = self.verify
        else:
            self.verify = verify
        return data, headers, verify

    def prep_request(self, route, **kwargs):
        path = self.build_path(route)
        data = kwargs.get("data")
        headers = kwargs.get("headers")
        verify = kwargs.get("verify")
        data, headers, verify = self.convert_dict_to_json_string(data, headers, verify)
        return path, data, headers, verify

    def get(self, route, **kwargs):
        path, data, headers, verify = self.prep_request(route, **kwargs)
        return requests.get(path, headers=headers, data=data, verify=verify)

    def put(self, route, **kwargs):
        path, data, headers, verify = self.prep_request(route, **kwargs)
        return requests.put(path, headers=headers, data=data, verify=verify)

    def post(self, route, **kwargs):
        path, data, headers, verify = self.prep_request(route, **kwargs)
        return requests.post(path, headers=headers, data=data, verify=verify)

    def delete(self, route, **kwargs):
        path, data, headers, verify = self.prep_request(route, **kwargs)
        return requests.delete(path, headers=headers, data=data, verify=verify)

    def patch(self, route, **kwargs):
        path, data, headers, verify = self.prep_request(route, **kwargs)
        return requests.patch(path, headers=headers, data=data, verify=verify)