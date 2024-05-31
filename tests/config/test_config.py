import unittest
from unittest.mock import patch, mock_open

from config.config import load_config


class TestConfigFunctions(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data="key: value")
    def test_load_config_success(self, mock_file):
        """
        Test loading configuration successfully.
        Mocks opening a YAML file with valid content and checks if the
        load_config function returns the correct dictionary.
        """
        file_path = 'config.yaml'
        expected_result = {'key': 'value'}
        result = load_config(file_path)
        self.assertEqual(result, expected_result)

    @patch('builtins.open', new_callable=mock_open)
    def test_load_config_file_not_found(self, mock_file):
        """
        Test handling file not found error.
        Mocks the scenario where the file does not exist and ensures
        that load_config raises a FileNotFoundError.
        """
        mock_file.side_effect = FileNotFoundError
        file_path = 'config.yaml'
        with self.assertRaises(FileNotFoundError):
            load_config(file_path)

    @patch('builtins.open', new_callable=mock_open, read_data="key: : value")
    def test_load_config_yaml_error(self, mock_file):
        """
        Test handling YAML parsing error.
        Mocks opening a YAML file with invalid content and checks if the
        load_config function raises a ValueError.
        """
        file_path = 'config.yaml'
        with self.assertRaises(ValueError) as context:
            load_config(file_path)
        self.assertIn("Error parsing configuration file", str(context.exception))


if __name__ == '__main__':
    unittest.main()
