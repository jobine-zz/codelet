import os
import json
import pyperclip
import tkinter.messagebox as mb

from log.logger import Logger
from util.retryrequests import RetryRequests

REQUEST_TIMEOUT_SECONDS = 30
EXPORT_CLIPBOARD = 'ClIPBOARD'
EXPORT_FILE = 'FILE'

TARGET_FINAL = 'FINAL'
TARGET_INCREMENTAL = 'INCREMENTAL'


class AppEE(object):
    def __init__(self, service=None, endpoint=None, api_key=None, export=EXPORT_CLIPBOARD):
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
        self.export = export

        self.retry_requests = RetryRequests()
        self.logger = Logger().get_logger()

    def __get(self, path, data=None):
        url = os.path.join(self.endpoint, path)

        headers = {
            'x-api-key': self.api_key,
            'Content-Type': 'application/json'
        }

        try:
            res = self.retry_requests.get(url=url, headers=headers, params=data, timeout=REQUEST_TIMEOUT_SECONDS, verify=True)

            return res.json()
        except Exception as e:
            raise Exception(f'GET {url} failed, request: {data}. {repr(e)}')

    def __post(self, path, data):
        url = os.path.join(self.endpoint, path)

        headers = {
            'x-api-key': self.api_key,
            'Content-Type': 'application/json'
        }

        try:
            res = self.retry_requests.post(url=url, headers=headers, data=json.dump(data), timeout=REQUEST_TIMEOUT_SECONDS, verify=True)
            if res.status_code != 204:
                return res.json()
        except Exception as e:
            raise Exception(f'POST {url} failed, request: {data}. {repr(e)}')

    def __export(self, app_uuid, text, target):
        try:
            if self.export == EXPORT_CLIPBOARD:
                pyperclip.copy(text)
                self.logger.info('Your generated script is copied to clipboard!')
                # mb.showinfo('Info', 'Your generated script is copied to clipboard!')

            elif self.export == EXPORT_FILE:
                file_path = ''

                if target == TARGET_INCREMENTAL:
                    file_path = os.path.join(os.getcwd(), f'update_app_parameters_{app_uuid}.sql')
                elif target == TARGET_FINAL:
                    file_path = os.path.join(os.getcwd(), f'final_app_{app_uuid}.sql')
                else:
                    raise Exception(f"The file path '{file_path}' does not exist.")

                with open(file_path, 'w') as f:
                    f.write(text)
                    self.logger.info(f'Your generated script is written to the file {file_path}.')
                    # mb.showinfo('Info', f'Your generated script is written to the file {file_path}.')
        except Exception as e:
            self.logger.exception(f'Failed to export your script.', exc_info=e)
            # mb.showerror('Error', f'Failed to export your script. {repr(e)}')

    def get_app(self, uuid):
        path = f'timeSeriesGroups/apps/{uuid}'
        return self.__get(path=path)

    def sql_update_parameters(self, app_uuid):
        try:
            app = self.get_app(uuid=app_uuid)
            parameters = json.dumps(app['parameters']).replace("'", "''")

            res = f"UPDATE time_series_group_app SET parameters = '{parameters}'::jsonb WHERE time_series_group_app_uuid = '{app_uuid}'::uuid;"

            self.logger.info('----- UPDATE APP PARAMETERS STATEMENT -----')
            self.logger.info(res)

            self.__export(app_uuid, res, TARGET_INCREMENTAL)

        except Exception as e:
            self.logger.exception(f'Failed to get app {app_uuid}.', exc_info=e)

    def sql_insert_final(self, app_uuid):
        try:
            app = self.get_app(uuid=app_uuid)

            settings = {}
            if 'description' in app:
                settings['description'] = app['description']
            if 'show_result' in app:
                settings['show_result'] = app['show_result']
            if 'alertable' in app:
                settings['alertable'] = app['alertable']
            if 'trainable' in app:
                settings['trainable'] = app['trainable']
            if 'inferenceable' in app:
                settings['inferenceable'] = app['inferenceable']

            settings_str = json.dumps(settings).replace("'", "''")

            parameters_str = json.dumps(app['parameters']).replace("'", "''")

            res = "INSERT INTO time_series_group_app(time_series_group_app_uuid, time_series_group_app_name, display_name, settings, parameters, endpoint_meta, endpoint_train, endpoint_inference, stage, type) VALUES (" + \
                  f"'{app_uuid}', '{app['appName']}', '{app['displayName']}', '{settings_str}', '{parameters_str}', '{app['endpointMeta']}', '{app['endpointTrain']}', '{app['endpointInference']}', 'Public', 'Internal'" + \
                  ");"

            self.logger.info('----- INSERT APP STATEMENT -----')
            self.logger.info(res)

            self.__export(app_uuid, res, TARGET_FINAL)
        except Exception as e:
            self.logger.exception(f'Failed to get app {app_uuid}.', exc_info=e)


if __name__ == '__main__':
    api_key = 'fbf81c2b-fb56-4a99-af9e-605bba953d30'
    app_id = '939a23a3-27b5-437b-9a3c-e74c4051a441'
    ae = AppEE(service='stock-exp3', api_key=api_key)
    ae.sql_update_parameters(app_id)
    # ae.sql_insert_final(app_id)