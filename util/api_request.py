import json
import os

from util.retryrequests import RetryRequests


class ApiRequest(object):

    def __init__(self,  service=None, endpoint=None, api_key=None):
        self.REQUEST_TIMEOUT_SECONDS = 30

        self.service = service
        if service is not None:
            self.endpoint = f'https://{service}-api.azurewebsites.net'
        elif endpoint is not None:
            self.endpoint = endpoint
        else:
            raise Exception('Either service name or endpoint should be provided.')

        if api_key is None:
            raise Exception('Api key should be provided.')

        self.api_key = api_key

        self.retry_requests = RetryRequests()

    def get(self, path, data=None):
        url = os.path.join(self.endpoint, path)

        headers = {
            'x-api-key': self.api_key,
            'Content-Type': 'application/json'
        }

        try:
            res = self.retry_requests.get(url=url, headers=headers, params=data, timeout=self.REQUEST_TIMEOUT_SECONDS, verify=True)

            return res.json()
        except Exception as e:
            raise Exception(f'GET {url} failed, request: {data}. {repr(e)}')

    def post(self, path, data):
        url = os.path.join(self.endpoint, path)

        headers = {
            'x-api-key': self.api_key,
            'Content-Type': 'application/json'
        }

        try:
            res = self.retry_requests.post(url=url, headers=headers, data=json.dump(data), timeout=self.REQUEST_TIMEOUT_SECONDS, verify=True)
            if res.status_code != 204:
                return res.json()
        except Exception as e:
            raise Exception(f'POST {url} failed, request: {data}. {repr(e)}')
