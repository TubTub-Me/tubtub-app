# Use latest Node.js image based on Debian
FROM node:22-bullseye

# Install Python and other dependencies
RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    git \
    && rm -rf /var/lib/apt/lists/*

# Upgrade PIP
RUN pip3 install --upgrade pip

# Install AWS CLI v2
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    rm -rf aws awscliv2.zip

# Install AWS CDK globally
RUN npm install -g aws-cdk@latest

# Create a working directory
WORKDIR /app

# Create a non-root user
RUN useradd -m -s /bin/bash cdk-user && \
    chown -R cdk-user:cdk-user /app
USER cdk-user

# Set environment variables for AWS authentication
ENV AWS_DEFAULT_REGION=us-east-1
ENV AWS_ACCESS_KEY_ID=""
ENV AWS_SECRET_ACCESS_KEY=""
ENV AWS_SESSION_TOKEN=""

# Keep container running
CMD ["bash"]
