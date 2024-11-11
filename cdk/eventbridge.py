# ---------------------------------------------------------------
#                           Imports
# ---------------------------------------------------------------

import json
import aws_cdk as cdk
from aws_cdk import NestedStack
from aws_cdk import aws_ssm as ssm
from aws_cdk import aws_iam as iam
from aws_cdk import aws_scheduler as scheduler
from constructs import Construct

# ---------------------------------------------------------------
#                     Nested Stack Definition
# ---------------------------------------------------------------

class EventBridgeStack(NestedStack):
    def __init__(self, scope: Construct, construct_id: str, external_params: dict, sqs_stack: NestedStack, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # External params
        self._app_name = external_params["general_params"]["app_name"]
        self._notifications_frequency_in_minutes = external_params["reminders_service"]["notifications_frequency_in_minutes"]
        self._is_scheduled_reminders_enabled = external_params["reminders_service"]["is_scheduled_reminders_enabled"]
        self._scheduled_reminders_rule_description = external_params["reminders_service"]["scheduled_reminders_rule_description"]
        self._scheduled_reminders_queue_message = external_params["reminders_service"]["queue_message_details"]["main_orchestrator"]

        # Retrieve SQS queue ARN from SSM Parameter Store
        self._reminders_queue_arn = ssm.StringParameter.value_for_string_parameter(
            self,
            parameter_name=f"/{self._app_name}/sqs/queue/arn/reminders"
        )

        # Create schedule role & policy
        self._reminders_messages_scheduler_role = iam.Role(
            self,
            "reminders-messages-scheduler-role",
            assumed_by=iam.ServicePrincipal("scheduler.amazonaws.com"),
            inline_policies = {
                "sqs_send_message": iam.PolicyDocument(
                statements=[
                    iam.PolicyStatement(
                        actions=["sqs:SendMessage"],
                        resources=[self._reminders_queue_arn],
                        effect=iam.Effect.ALLOW,
                    )
                ]
            )}
        )

        # Create schedule to send a message to SQS periodically
        self._reminders_messages_scheduler = scheduler.CfnSchedule(
            self,
            "reminders-messages-scheduler",
            flexible_time_window=scheduler.CfnSchedule.FlexibleTimeWindowProperty(
                mode="OFF",
            ),
            schedule_expression= self._notifications_frequency_in_minutes,
            target=scheduler.CfnSchedule.TargetProperty(
                arn=self._reminders_queue_arn,
                role_arn=self._reminders_messages_scheduler_role.role_arn,
                input=json.dumps(self._scheduled_reminders_queue_message)
            )
        )

        # Output
        cdk.CfnOutput(self, "reminders_messages_scheduler_name", value=self._reminders_messages_scheduler.ref)

        # SSM Params
        ssm.StringParameter(
            self,
            "reminders-messages-scheduler-name",
            parameter_name=f"/{self._app_name}/scheduler/name/reminders",
            string_value=self._reminders_messages_scheduler.ref,
        )
