# Define Colors
GREEN  := \033[0;32m
YELLOW := \033[0;33m
NC     := \033[0m  # No Color

# Build CDK Development Environment
.PHONY: dev-cdk
dev-cdk:
	@echo "$(GREEN)Building docker image$(NC)"
	@docker build -t dev-cdk .
	@echo "\n"
	@echo "$(GREEN)Spinning up dev-cdk docker container$(NC)"
	@docker run -it \
		-v ${PWD}:/app \
		-e AWS_ACCESS_KEY_ID=$(aws configure get aws_access_key_id) \
		-e AWS_SECRET_ACCESS_KEY=$(aws configure get aws_secret_access_key) \
		-e AWS_SESSION_TOKEN=$(aws configure get aws_session_token) \
		-e AWS_REGION=$(aws configure get region) \
		-e AWS_DEFAULT_REGION=$(aws configure get region) \
		dev-cdk

# Setup Local Development Environment - Docker Container
.PHONY: dev-env
dev-env:
	@echo "$(GREEN)Creating Python virtual environment$(NC)"
	@python3 -m venv .venv

	@echo "$(GREEN)Activating virtual environment$(NC)"
	@. .venv/bin/activate

	@echo "$(GREEN)Installing dependencies$(NC)"
	@pip3 install .
	@pip3 install .[dev]

	@echo "$(GREEN)Virtual environment now installed with dependencies$(NC)"
	@echo "$(YELLOW)To use the venv, run '. .venv/bin/activate'$(NC)"

# Compile CDK code
.PHONY: synth
synth:
	@echo "$(GREEN)Activating virtual environment$(NC)"
	@. .venv/bin/activate

	@echo "$(GREEN)Compiling your CDK code$(NC)"
	@cdk synth
