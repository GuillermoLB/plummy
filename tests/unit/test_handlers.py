"""Unit tests for the Handler classes in the shared framework."""
from plummy.handlers import StepHandler

def test_step_handler_processes_when_can_handle_is_true(
    mock_processor, mock_handler
):
    """
    Tests that StepHandler calls its processor and the next handler
    when can_handle() returns True.
    """
    # 1. Arrange
    mock_processor.can_handle.return_value = True
    test_data = {"key": "value"}

    # Create the handler instance we are testing
    handler = StepHandler(processor=mock_processor)
    handler.set_next(mock_handler)

    # 2. Act
    handler.handle(test_data)

    # 3. Assert
    # Verify the processor was called as expected
    mock_processor.can_handle.assert_called_once_with(test_data)
    mock_processor.process.assert_called_once_with(test_data)
    
    # Verify the chain continued
    mock_handler.handle.assert_called_once()


def test_step_handler_skips_when_can_handle_is_false(
    mock_processor, mock_handler
):
    """
    Tests that StepHandler skips its processor but still calls the next handler
    when can_handle() returns False.
    """
    # 1. Arrange
    mock_processor.can_handle.return_value = False
    test_data = {"key": "value"}

    handler = StepHandler(processor=mock_processor)
    handler.set_next(mock_handler)

    # 2. Act
    handler.handle(test_data)

    # 3. Assert
    # Verify the processor's 'can_handle' was checked, but 'process' was not called
    mock_processor.can_handle.assert_called_once_with(test_data)
    mock_processor.process.assert_not_called()

    # Verify the chain still continued
    mock_handler.handle.assert_called_once_with(test_data)
    

def test_step_handler_at_end_of_chain(mock_processor):
    """
    Tests that a StepHandler correctly processes data and returns the result
    when it is the last handler in the chain (i.e., no next_handler is set).
    """
    # 1. Arrange
    test_data = {"status": "new"}
    processed_data = {"status": "processed"}

    # Configure the mock processor to accept the data and return a specific result
    mock_processor.can_handle.return_value = True
    mock_processor.process.return_value = processed_data

    # Create the handler instance, but DO NOT set a next handler
    handler = StepHandler(processor=mock_processor)

    # 2. Act
    result = handler.handle(test_data)

    # 3. Assert
    # Verify that the processor's methods were called correctly
    mock_processor.can_handle.assert_called_once_with(test_data)
    mock_processor.process.assert_called_once_with(test_data)

    # Verify that the final result is the data returned by our processor
    assert result == processed_data