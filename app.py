#!/usr/bin/env python3

# ---------------------------------------------------------------
#                            Imports
# ---------------------------------------------------------------
import os
import json
import cdk_nag as nag
import aws_cdk as cdk
from cdk.main import ParentStack

# ---------------------------------------------------------------
#                            Env Vars
# ---------------------------------------------------------------

ENVIRONMENT_NAME = os.getenv("ENVIRONMENT_NAME", "prod")

# ---------------------------------------------------------------
#                         External Params
# ---------------------------------------------------------------

current_dir = os.path.dirname(os.path.realpath(__file__))
parameters_file_path = os.path.join(current_dir, "params", f"{ENVIRONMENT_NAME}.json")
with open(parameters_file_path) as f:
    application_external_params = json.load(f)

# ---------------------------------------------------------------
#                           App stack
# ---------------------------------------------------------------

# Create the CDK app
app = cdk.App()

# Validate the CDK app against AWS Solutions Best Practices
nag.AwsSolutionsChecks.VALIDATE_NAG_CHECKS = True
cdk.Aspects.of(app).add(nag.AwsSolutionsChecks())

# Define TubTub Chatbot Infrastructure
ParentStack(app, "tubtub-chatbot-infrastructure", application_external_params)

# ---------------------------------------------------------------
#                Generate CloudFromation Template
# ---------------------------------------------------------------

app.synth()