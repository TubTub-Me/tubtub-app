# ---------------------------------------------------------------
#                           Imports
# ---------------------------------------------------------------

import aws_cdk as cdk
from aws_cdk import NestedStack
from aws_cdk import aws_ssm as ssm
from aws_cdk import aws_events as eventbridge
from constructs import Construct

# ---------------------------------------------------------------
#                     Nested Stack Definition
# ---------------------------------------------------------------

class EventBridgeStack(NestedStack):
    def __init__(self, scope: Construct, construct_id: str, external_params: dict, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # External params
        self._app_name = external_params["general_params"]["app_name"]
        self._notifications_frequency_in_hours = external_params["reminders_service"]["notifications_frequency_in_hours"]
        self._is_scheduled_reminders_enabled = external_params["reminders_service"]["is_scheduled_reminders_enabled"]
        self._scheduled_reminders_rule_description = external_params["reminders_service"]["scheduled_reminders_rule_description"]

        # Create EventBridge scheduled rule - reminders messages
        self._reminders_messages_scheduled_rule = eventbridge.Rule(
            self,
            "reminders-messages-scheduled-rule",
            description = self._scheduled_reminders_rule_description,
            enabled = self._is_scheduled_reminders_enabled,
            rule_name = f"{self._app_name}_reminders_messages_scheduled_rule",
            schedule=eventbridge.Schedule.rate(
                cdk.Duration.hours(self._notifications_frequency_in_hours)
            ),
            # TODO: Add SQS as a target
            targets = [
                
            ],
            # TODO: Add an event pattern
            event_pattern = ""
        )