import json
import codecs
from instagram_private_api import (
        Client, ClientError, ClientLoginError,
        ClientCookieExpiredError, ClientLoginRequiredError,
        __version__ as client_version)

class GenerateSession:

    def __init__(self, config_path: str) -> None:
        self.session = None
        self.device_id = None
        self.config_data = None
        self.settings_file = config_path

        self.authenticate()

    @property
    def Session(self) -> Client:
        return self.session

    def to_json(self, python_object):
        if isinstance(python_object, bytes):
            return { 
                     '__class__': 'bytes',
                     '__value__': codecs.encode(python_object, 'base64').decode()
                    }
        raise TypeError(repr(python_object) + ' is not JSON serializable')

    def from_json(self, json_object):
        if '__class__' in json_object and json_object['__class__'] == 'bytes':
            return codecs.decode(json_object['__value__'].encode(), 'base64')
        return json_object

    def onlogin_callback(self, api):
        cache_settings: dict = api.settings
        cache_settings.update({"username": self.config_data['username'], "password": self.config_data['password']})
        with open(self.settings_file, 'w') as outfile:
            json.dump(cache_settings, outfile, default=self.to_json)
            print('SAVED: {0!s}'.format(self.settings_file))

    def authenticate(self) -> None:
        
        try:
            with open(self.settings_file) as file:
                self.config_data = json.load(file)

            if 'cookie' not in self.config_data:
                # settings file does not exist
                print('Unable to find session')
                
                # login new
                self.session = Client(
                    self.config_data['username'], self.config_data['password'],
                    on_login=lambda x: self.onlogin_callback(x))
            else:
                with open(self.settings_file) as file_data:
                    cached_settings = json.load(file_data, object_hook=self.from_json)
                print('Reusing settings: {0!s}'.format(self.settings_file))

                self.device_id = cached_settings.get('device_id')
                # reuse auth settings
                self.session = Client(
                    self.config_data['username'], self.config_data['password'],
                    settings=cached_settings)

        except (ClientCookieExpiredError, ClientLoginRequiredError) as e:
            print('ClientCookieExpiredError/ClientLoginRequiredError: {0!s}'.format(e))

            # Login expired
            # Do relogin but use default ua, keys and such
            self.session = Client(
                self.config_data['username'], self.config_data['password'],
                device_id=self.device_id,
                on_login=lambda x: self.onlogin_callback(x))

        except ClientLoginError as e:
            print('ClientLoginError {0!s}'.format(e))
            exit(9)
        except ClientError as e:
            print('ClientError {0!s} (Code: {1:d}, Response: {2!s})'.format(e.msg, e.code, e.error_response))
            exit(9)
        except Exception as e:
            print('Unexpected Exception: {0!s}'.format(e))
            exit(99)

