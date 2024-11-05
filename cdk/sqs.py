# ---------------------------------------------------------------
#                           Imports
# ---------------------------------------------------------------

import aws_cdk as cdk
from aws_cdk import NestedStack
from aws_cdk import aws_iam as iam
from aws_cdk import aws_ssm as ssm
from aws_cdk import aws_sqs as sqs
from constructs import Construct

# ---------------------------------------------------------------
#                     Nested Stack Definition
# ---------------------------------------------------------------

class SqsStack(NestedStack):
    def __init__(self, scope: Construct, construct_id: str, external_params: dict, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # External params
        self._app_name = external_params["general_params"]["app_name"]
        self._dlq_max_receive_count = external_params["sqs_params"]["dlq_max_receive_count"]
        self._sqs_visibility_timeout_seconds = external_params["sqs_params"]["sqs_visibility_timeout_seconds"]

        # Create SQS Queue
        self._reminders_messages_queue = sqs.Queue(
            self,
            "reminders-sqs-queue",
            queue_name=f"{self._app_name}_reminders_sqs_queue",
            visibility_timeout=cdk.Duration.seconds(self._sqs_visibility_timeout_seconds),
            encryption=sqs.QueueEncryption.KMS_MANAGED,
            enforce_ssl=True,
            dead_letter_queue={
                "queue": sqs.Queue(
                    self,
                    "reminders-dlq-queue",
                    queue_name=f"{self._app_name}_reminders_dlq_queue",
                    enforce_ssl=True,
                    encryption=sqs.QueueEncryption.KMS_MANAGED
                ),
                "max_receive_count": self._dlq_max_receive_count
            }
        )

        # Doc: https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-use-resource-based.html#eb-sqs-permissions
        self._reminders_messages_queue.queue_policy = iam.PolicyDocument(
            statements=[
                iam.PolicyStatement(
                    sid = "AWSEvents_custom-eventbus-ack-sqs-rule_dlq_sqs-rule-target",
                    actions = ["sqs:SendMessage"],
                    effect=iam.Effect.ALLOW,
                    principals = [iam.ServicePrincipal("events.amazonaws.com")],
                    resources = [self._reminders_messages_queue.queue_arn],
                    conditions = {
                        "ArnEquals": {
                            "aws:SourceArn": f"arn:aws:events:${self.region}:${self.account}:rule/{self._app_name}_reminders_messages_scheduled_rule"
                        }
                    }
                )
            ]
        )

        # Output
        cdk.CfnOutput(self, "sqs_queue_arn", value=self._reminders_messages_queue.queue_arn)
        cdk.CfnOutput(self, "sqs_queue_url", value=self._reminders_messages_queue.queue_url)
        cdk.CfnOutput(self, "sqs_queue_name", value=self._reminders_messages_queue.queue_name)

        # SSM Params
        ssm.StringParameter(
            self,
            "message-processing-queue-arn",
            parameter_name=f"/{self._app_name}/sqs/queue/arn/reminders",
            string_value=self._reminders_messages_queue.queue_arn,
        )

        ssm.StringParameter(
            self,
            "message-processing-queue-url",
            parameter_name=f"/{self._app_name}/sqs/queue/url/reminders",
            string_value=self._reminders_messages_queue.queue_url,
        )

        ssm.StringParameter(
            self,
            "message-processing-queue-name",
            parameter_name=f"/{self._app_name}/sqs/queue/name/reminders",
            string_value=self._reminders_messages_queue.queue_url,
        )
