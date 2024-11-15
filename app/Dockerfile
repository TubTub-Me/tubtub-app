# Build stage
FROM --platform=linux/arm64 rust:latest AS builder
WORKDIR /usr/src/tubtub

# Copy only the manifest files to cache dependencies
COPY Cargo.toml Cargo.lock ./
RUN cargo build --release || true

# Copy the rest of the application source and build it
COPY . .
RUN cargo build --release

# Final stage - use a minimal base image
FROM --platform=linux/arm64 gcr.io/distroless/cc-debian12
COPY --from=builder /usr/src/tubtub/target/release/tubtub /usr/local/bin/tubtub
CMD ["tubtub"]
