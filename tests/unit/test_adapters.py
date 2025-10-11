"""Unit tests for the adapter classes in the shared framework."""
from plummy.adapters import FunctionalProcessor

def test_functional_processor_holds_functions():
    """
    Tests that the FunctionalProcessor correctly stores and provides
    the functions it was initialized with.
    """
    # 1. Arrange
    # Create two simple lambda functions to act as our logic
    def can_handle_func(data):
        return True
    def process_func(data):
        return {"processed": True}

    # 2. Act
    # Create an instance of the adapter with the functions
    processor = FunctionalProcessor(
        can_handle=can_handle_func,
        process=process_func
    )

    # 3. Assert
    # Check that the attributes of the instance are the functions we passed in
    assert processor.can_handle is can_handle_func
    assert processor.process is process_func