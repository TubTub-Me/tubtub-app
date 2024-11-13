# Imports
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.batch import (
    BatchProcessor,
    EventType,
    process_partial_response,
)
from aws_lambda_powertools.utilities.data_classes.sqs_event import SQSRecord
from aws_lambda_powertools.utilities.typing import LambdaContext

TRACER = Tracer()
LOGGER = Logger()
processor = BatchProcessor(event_type=EventType.SQS)  


@TRACER.capture_method
def record_handler(record: SQSRecord):  
    payload: str = record.json_body  # if json string data, otherwise record.body for str
    LOGGER.info(payload)


@LOGGER.inject_lambda_context
@TRACER.capture_lambda_handler
def lambda_handler(event, context: LambdaContext):
    return process_partial_response(  
        event=event,
        record_handler=record_handler,
        processor=processor,
        context=context,
    )