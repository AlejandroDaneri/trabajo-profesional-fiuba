# Use the official Golang image as a base image
FROM golang:alpine

# Set the working directory inside the container
WORKDIR /go/src/app

# Copy the local package files to the container's workspace
COPY . .

# Download and install any required dependencies
# RUN go get -d -v ./...

# Build the application
# RUN go install -v ./...

# Expose port 8080 to the outside world
EXPOSE 8080

# Command to run the executable

CMD ["go", "run", "main.go"]