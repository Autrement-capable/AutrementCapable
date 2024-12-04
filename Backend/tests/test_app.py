import unittest
from unittest.mock import patch, MagicMock
import app

class TestApp(unittest.TestCase):

    @patch('app.server.scheduler')
    def test_cleanup(self, mock_scheduler):
        # Arrange
        mock_scheduler.running = True

        # Act
        app.CleanUp()

        # Assert
        mock_scheduler.shutdown.assert_called_once_with(wait=False)

    @patch('app.server.Run')
    @patch('atexit.register')
    def test_main_execution(self, mock_atexit_register, mock_server_run):
        # Act
        with patch('builtins.__name__', '__main__'):
            exec(open('app.py').read())

        # Assert
        mock_server_run.assert_called_once()
        mock_atexit_register.assert_called_once_with(app.CleanUp)

if __name__ == '__main__':
    unittest.main()