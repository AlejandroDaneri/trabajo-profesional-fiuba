FROM golang:latest

WORKDIR /go/src/app

RUN go mod init myapp

COPY . .

RUN go build -o app login.go

ENTRYPOINT ["./app"]
