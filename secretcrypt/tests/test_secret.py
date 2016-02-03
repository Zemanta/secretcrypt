import unittest
import mock

import secretcrypt
from secretcrypt import Secret


class TestSecret(unittest.TestCase):

    @mock.patch('importlib.import_module')
    def test_decrypt(self, mock_import_module):
        mock_crypter_module = mock.MagicMock()
        mock_crypter_module.__name__ = 'secretcrypt.mock_crypter'

        def mock_import_side_effect(*args, **kwargs):
            self.assertEqual(kwargs['package'], secretcrypt.__name__)
            if args[0] == 'secretcrypt.mock_crypter':
                return mock_crypter_module
            raise Exception('Importing wrong module')
        mock_import_module.side_effect = mock_import_side_effect

        secret = Secret('secretcrypt.mock_crypter:myciphertext')
        secret.decrypt()
        mock_crypter_module.decrypt.assert_called_with('myciphertext')
