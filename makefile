# Define Colors
GREEN  := \033[0;32m
YELLOW := \033[0;33m
NC     := \033[0m  # No Color

# Define variables
STACK_NAME=tubtub-app

# Clouformation Packaging
.PHONY: cfn-package
cfn-package:
	@echo "$(GREEN)Packging CloudFormation templates$(NC)"
	@mkdir ./cfn/templates/build | true
	@aws cloudformation package \
		--s3-bucket $$BUCKET \
		--template-file ./cfn/templates/main.yaml \
		--force-upload \
		--output-template-file ./cfn/templates/build/main.yaml > /dev/null;
	@echo "$(GREEN)Successfully packged CloudFormation templates$(NC)"

# Clouformation Deployments
.PHONY: cfn-deploy
cfn-deploy: cfn-package
	@echo "$(GREEN)Deploying CloudFormation templates$(NC)\n"
	@aws cloudformation deploy \
		--template-file ./cfn/templates/build/main.yaml \
		--stack-name $(STACK_NAME) \
		--s3-bucket $$BUCKET \
		--force-upload \
		--parameter-overrides file://cfn/params/main.json \
		--capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND
	@echo "$(GREEN)Successfully deployed CloudFormation templates$(NC)\n"
