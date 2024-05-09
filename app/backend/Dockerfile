FROM golang:alpine3.19 as builder

COPY go.mod go.sum /go/src/github.com/bartosz-urbanowicz/bird-sound-recognition/app/backend/

WORKDIR /go/src/github.com/bartosz-urbanowicz/bird-sound-recognition/app/backend

RUN go mod download

COPY . .

RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o build/backend

FROM alpine

RUN apk add --no-cache ca-certificates && update-ca-certificates

COPY --from=builder /go/src/github.com/bartosz-urbanowicz/bird-sound-recognition/app/backend/build/backend /usr/bin/backend

EXPOSE 8080 8080

ENTRYPOINT ["/usr/bin/backend"]