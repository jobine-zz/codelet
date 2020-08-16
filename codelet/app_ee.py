import os
import json
import pyperclip

from log.logger import Logger
from util.api_request import ApiRequest

EXPORT_CLIPBOARD = 'ClIPBOARD'
EXPORT_FILE = 'FILE'

TARGET_FINAL = 'FINAL'
TARGET_INCREMENTAL = 'INCREMENTAL'


class AppEE(object):
    def __init__(self, service=None, endpoint=None, api_key=None, export=EXPORT_CLIPBOARD):
        self.export = export
        self.api_request = ApiRequest(service=service, endpoint=endpoint, api_key=api_key)
        self.logger = Logger().get_logger()

    def __export_app(self, app_uuid, text, target):
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

    def __export_all_apps(self, text):
        try:
            if self.export == EXPORT_CLIPBOARD:
                pyperclip.copy(text)
                self.logger.info('Your generated script is copied to clipboard!')

            elif self.export == EXPORT_FILE:
                file_path = 'insert_all_apps.sql'

                with open(file_path, 'w') as f:
                    f.write(text)
                    self.logger.info(f'Your generated script is written to the file {file_path}.')
        except Exception as e:
            self.logger.exception(f'Failed to export your script.', exc_info=e)

    def get_app(self, uuid):
        path = f'timeSeriesGroups/apps/{uuid}'
        return self.api_request.get(path=path)

    def get_all(self):
        path = 'timeSeriesGroups/apps/all'
        return self.api_request.get(path=path)

    def is_super_user(self):
        path = 'superusers/check'
        res = self.api_request.get(path=path)
        return res['value']

    def sql_update_parameters(self, app_uuid):
        try:
            app = self.get_app(uuid=app_uuid)
            parameters = json.dumps(app['parameters']).replace("'", "''")

            res = f"UPDATE time_series_group_app SET parameters = '{parameters}'::jsonb WHERE time_series_group_app_uuid = '{app_uuid}'::uuid;"

            self.logger.info('----- UPDATE APP PARAMETERS STATEMENT -----')
            self.logger.info(res)

            self.__export_app(app_uuid, res, TARGET_INCREMENTAL)

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

            self.__export_app(app_uuid, res, TARGET_FINAL)
        except Exception as e:
            self.logger.exception(f'Failed to get app {app_uuid}.', exc_info=e)

    def sql_insert_all(self, only_public=True):
        try:
            if not self.is_super_user():
                raise PermissionError('You do not have the permission to generate script for all apps.')

            apps = self.get_all()

            if only_public:
                apps = filter(lambda app: app['stage'] == 'Public', apps['value'])

            res = "TRUNCATE TABLE time_series_group_app;" + os.linesep
            res += "INSERT INTO time_series_group_app(time_series_group_app_uuid, time_series_group_app_name, display_name, settings, parameters, endpoint_meta, endpoint_train, endpoint_inference, stage, type) VALUES "

            for app in apps:
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

                stmt = os.linesep + f"('{app['appId']}', '{app['appName']}', '{app['displayName']}', '{settings_str}', '{parameters_str}', '{app['endpointMeta']}', '{app['endpointTrain']}', '{app['endpointInference']}', 'Public', 'Internal'),"

                res += stmt

            res = res.rstrip(',') + ';'

            self.logger.info('----- INSERT APPS STATEMENT -----')
            self.logger.info(res)

            self.__export_all_apps(res)

        except Exception as e:
            self.logger.exception('Failed to generate script for all apps.', exc_info=e)


if __name__ == '__main__':
    api_key = 'fbf81c2b-fb56-4a99-af9e-605bba953d30'
    app_id = '9820d3c5-25d2-47a7-9b9f-3729199350f0'
    ae = AppEE(service='stock-exp3', api_key=api_key)
    # ae.sql_update_parameters(app_id)
    # ae.sql_insert_final(app_id)
    ae.sql_insert_all()
