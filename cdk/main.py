# ---------------------------------------------------------------
#                           Imports
# ---------------------------------------------------------------

# CDK Imports - core
import aws_cdk as cdk
from constructs import Construct

# Nested Stack Imports
from cdk.sqs import SqsStack
from cdk.eventbridge import EventBridgeStack

# ---------------------------------------------------------------
#                     Parent Stack Definition
# ---------------------------------------------------------------

class ParentStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, external_params: dict, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # Nested stack definitions
        self.sqs = SqsStack(self, "tubtub-sqs", external_params)
        self.eventbridge = EventBridgeStack(self, "tubtub-eventbridge", external_params, self.sqs)

        # Add dependencies
        self.eventbridge.add_dependency(self.sqs)

        # Tags
        cdk.Tags.of(self).add("app_name", "TubTub")
        cdk.Tags.of(self).add("app_description", "A WhatsApp chatbot that reminds you to hug your partner")
