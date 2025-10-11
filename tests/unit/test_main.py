"""Unit tests for the main module functionality."""
from unittest.mock import patch
from plummy import main


def test_main_prints_hello_message():
    """Tests that the main function prints the expected message."""
    # Use patch to capture the print output
    with patch('builtins.print') as mock_print:
        # Act
        main()
        
        # Assert
        mock_print.assert_called_once_with("Hello from plummy!")
