# Build stage
FROM rust:latest AS builder
WORKDIR /usr/src/tubtub

# Copy only the manifest files to cache dependencies
COPY Cargo.toml Cargo.lock ./
RUN cargo build --release || true

# Copy the rest of the application source and build it
COPY . .
RUN cargo build --release

# Final stage - use a minimal base image
FROM alpine:latest
RUN apk update && apk add --no-cache libgcc openssl
COPY --from=builder /usr/src/tubtub/target/release/tubtub /usr/local/bin/tubtub

# Ensure the binary is executable
RUN chmod +x /usr/local/bin/tubtub

# Run the application as a non-root user
RUN adduser -D -u 1000 tubtub-user
USER tubtub-user

CMD ["tubtub"]
