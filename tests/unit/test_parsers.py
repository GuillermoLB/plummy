"""Unit tests for the reusable parser functions in the shared framework."""
from plummy.parsers import ParsedAPIGatewayRequest, parse_api_gateway_event, parse_sqs_event, ParsedSQSRecord


def test_parse_sqs_event_with_valid_record():
    """Tests that the parser correctly extracts data from a valid SQS event."""
    # Arrange
    valid_event = {
        "Records": [{
            "eventSourceARN": "arn:aws:sqs:us-east-1:123:MyQueue",
            "body": '{"message": "hello"}'
        }]
    }

    # Act
    parsed_records = list(parse_sqs_event(valid_event))

    # Assert
    assert len(parsed_records) == 1
    assert isinstance(parsed_records[0], ParsedSQSRecord)
    assert parsed_records[0].source_arn == "arn:aws:sqs:us-east-1:123:MyQueue"
    assert parsed_records[0].body["message"] == "hello"

def test_parse_sqs_event_with_invalid_event():
    """Tests that the parser handles a completely malformed event without crashing."""
    # Arrange
    invalid_event = {"message": "this is not an SQS event"}

    # Act
    parsed_records = list(parse_sqs_event(invalid_event))

    # Assert
    assert len(parsed_records) == 0


def test_parse_sqs_event_with_multiple_records():
    """Tests that the parser correctly handles an event with multiple records."""
    # Arrange
    multi_record_event = {
        "Records": [
            {"eventSourceARN": "arn:1", "body": '{"id": 1}'},
            {"eventSourceARN": "arn:2", "body": '{"id": 2}'},
        ]
    }

    # Act
    parsed_records = list(parse_sqs_event(multi_record_event))

    # Assert
    assert len(parsed_records) == 2
    assert parsed_records[0].body["id"] == 1
    assert parsed_records[1].body["id"] == 2

def test_parse_sqs_event_skips_record_with_bad_json():
    """
    Tests that the parser gracefully skips a record with a malformed JSON body
    but still processes other valid records in the same event.
    """
    # Arrange
    mixed_event = {
        "Records": [
            {"eventSourceARN": "arn:good", "body": '{"status": "ok"}'},
            {"eventSourceARN": "arn:bad", "body": '{"malformed_json":'}, # Invalid JSON
            {"eventSourceARN": "arn:good_too", "body": '{"status": "ok_too"}'},
        ]
    }

    # Act
    parsed_records = list(parse_sqs_event(mixed_event))

    # Assert
    assert len(parsed_records) == 2
    assert parsed_records[0].source_arn == "arn:good"
    assert parsed_records[1].source_arn == "arn:good_too"

def test_parse_sqs_event_with_empty_records_list():
    """Tests that the parser handles an event with an empty 'Records' list."""
    # Arrange
    empty_event = {"Records": []}

    # Act
    parsed_records = list(parse_sqs_event(empty_event))

    # Assert
    assert len(parsed_records) == 0
    
def test_parse_api_gateway_event_with_valid_post_request():
    """Tests that the parser correctly handles a valid POST request with a JSON body."""
    # Arrange
    api_event = {
        "httpMethod": "POST",
        "path": "/invoices",
        "headers": {"Content-Type": "application/json"},
        "body": '{"amount": 100, "client_id": "client_123"}'
    }

    # Act
    parsed_request = parse_api_gateway_event(api_event)

    # Assert
    assert parsed_request is not None
    assert isinstance(parsed_request, ParsedAPIGatewayRequest)
    assert parsed_request.http_method == "POST"
    assert parsed_request.path == "/invoices"
    assert parsed_request.body["amount"] == 100

def test_parse_api_gateway_event_with_valid_get_request():
    """Tests that the parser correctly handles a valid GET request with no body."""
    # Arrange
    api_event = {
        "httpMethod": "GET",
        "path": "/invoices/inv_123",
        "headers": {},
        "body": None # GET requests often have no body
    }

    # Act
    parsed_request = parse_api_gateway_event(api_event)

    # Assert
    assert parsed_request is not None
    assert parsed_request.http_method == "GET"
    assert parsed_request.body == {} # Should default to an empty dict

def test_parse_api_gateway_event_with_invalid_json_body():
    """Tests that the parser returns None for a request with a malformed JSON body."""
    # Arrange
    api_event = {
        "httpMethod": "POST",
        "path": "/invoices",
        "body": '{"amount": 100, "client_id":' # Incomplete JSON
    }

    # Act
    parsed_request = parse_api_gateway_event(api_event)

    # Assert
    assert parsed_request is None

def test_parse_api_gateway_event_with_non_api_event():
    """Tests that the parser returns None for an event that is not from API Gateway."""
    # Arrange
    sqs_event = {"Records": [{}]} # An SQS event structure

    # Act
    parsed_request = parse_api_gateway_event(sqs_event)

    # Assert
    assert parsed_request is None