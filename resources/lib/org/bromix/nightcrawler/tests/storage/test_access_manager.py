__author__ = 'bromix'

import time
import unittest

from resources.lib.org.bromix import nightcrawler
from resources.lib.org.bromix.nightcrawler.core.abstract_settings import AbstractSettings
from resources.lib.org.bromix.nightcrawler.storage import AccessManager


class TestAccessManager(unittest.TestCase):
    def test_do_login(self):
        def _login(username, password):
            return {'access_token': 'abcd',
                    'refresh_token': '1234',
                    'expires_in': int(time.time())}

        def _refresh_token(access_data):
            return access_data

        context = nightcrawler.Context()
        settings = context.get_settings()

        access_manager = context.get_access_manager()
        access_manager.remove_login_credentials()
        access_data = context.get_access_manager().do_login(_login)
        self.assertDictEqual(access_data, {})

        settings.set_string(settings.LOGIN_USERNAME, 'Hans')
        settings.set_string(settings.LOGIN_PASSWORD, '1235')
        access_data = context.get_access_manager().do_login(_login)

        access_data = context.get_access_manager().do_login(_login)
        access_data = context.get_access_manager().do_refresh_token(_refresh_token)
        pass

    def test_access_token_expired(self):
        context = nightcrawler.Context()
        settings = context.get_settings()
        access_manager = AccessManager(settings)

        # set some test data
        settings.set_string(AbstractSettings.LOGIN_ACCESS_TOKEN, '')

        access_token = access_manager.get_access_token()
        self.assertEqual('', access_token)

        # should return False because no access_token was provided
        result = access_manager._is_access_token_expired()
        self.assertEqual(True, result)

        access_manager.update_access_token('1234567890')
        access_token = access_manager.get_access_token()
        self.assertEqual('1234567890', access_token)

        # should return False, because the access_token is fresh
        result = access_manager._is_access_token_expired()
        self.assertEqual(False, result)

        # should return False, we have 5000 seconds
        access_manager.update_access_token('1234567890', time.time() + 5000)
        result = access_manager._is_access_token_expired()
        self.assertEqual(False, result)

        # should return True, we are 5000 seconds in the future
        access_manager.update_access_token('1234567890', time.time() - 5000)
        result = access_manager._is_access_token_expired()
        self.assertEqual(True, result)
        pass

    def test_access_token(self):
        context = nightcrawler.Context()
        settings = context.get_settings()
        access_manager = AccessManager(settings)

        # set some test data
        settings.set_string(AbstractSettings.LOGIN_ACCESS_TOKEN, '')

        access_token = access_manager.get_access_token()
        self.assertEqual('', access_token)

        access_manager.update_access_token('1234567890')
        access_token = access_manager.get_access_token()
        self.assertEqual('1234567890', access_token)
        pass

    def test_is_new_login_credential(self):
        context = nightcrawler.Context()
        settings = context.get_settings()
        access_manager = AccessManager(settings)

        # set some test data
        settings.set_string(AbstractSettings.LOGIN_HASH, '')
        settings.set_string(AbstractSettings.LOGIN_USERNAME, 'Thomas')
        settings.set_string(AbstractSettings.LOGIN_PASSWORD, '1234')

        self.assertEqual(True, access_manager.is_new_login_credential())
        self.assertEqual(False, access_manager.is_new_login_credential())

        # we change the password
        settings.set_string(AbstractSettings.LOGIN_PASSWORD, '12345')
        self.assertEqual(True, access_manager.is_new_login_credential())
        self.assertEqual(False, access_manager.is_new_login_credential())
        pass

    def test_get_login_credentials(self):
        context = nightcrawler.Context()
        settings = context.get_settings()
        access_manager = AccessManager(settings)

        # set some test data
        settings.set_string(AbstractSettings.LOGIN_USERNAME, 'Thomas')
        settings.set_string(AbstractSettings.LOGIN_PASSWORD, '1234')

        username, password = access_manager.get_login_credentials()
        self.assertEqual('Thomas', username)
        self.assertEqual('1234', password)
        pass

    def test_has_login_credentials(self):
        context = nightcrawler.Context()
        settings = context.get_settings()
        access_manager = AccessManager(settings)

        # no username no password
        settings.set_string(AbstractSettings.LOGIN_USERNAME, '')
        settings.set_string(AbstractSettings.LOGIN_PASSWORD, '')
        self.assertEqual(False, access_manager.has_login_credentials())

        # no username but password
        settings.set_string(AbstractSettings.LOGIN_USERNAME, '')
        settings.set_string(AbstractSettings.LOGIN_PASSWORD, '1234')
        self.assertEqual(False, access_manager.has_login_credentials())

        # username but no password
        settings.set_string(AbstractSettings.LOGIN_USERNAME, '1234')
        settings.set_string(AbstractSettings.LOGIN_PASSWORD, '')
        self.assertEqual(False, access_manager.has_login_credentials())

        # username and password
        settings.set_string(AbstractSettings.LOGIN_USERNAME, '1234')
        settings.set_string(AbstractSettings.LOGIN_PASSWORD, '1234')
        self.assertEqual(True, access_manager.has_login_credentials())
        pass

    pass
