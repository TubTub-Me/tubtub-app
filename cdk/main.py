# ---------------------------------------------------------------
#                           Imports
# ---------------------------------------------------------------

# CDK Imports - core
import aws_cdk as cdk
from constructs import Construct

# Nested Stack Imports
from cdk.sqs import SqsStack

# ---------------------------------------------------------------
#                     Parent Stack Definition
# ---------------------------------------------------------------

class ParentStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, external_params: dict, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # Nested stack definitions
        SqsStack(self, "tubtub-sqs", external_params)
        
        # Tags
        cdk.Tags.of(self).add("app_name", "TubTub")
        cdk.Tags.of(self).add("app_description", "A WhatsApp chatbot that reminds you to hug your partner")
