from golang:alpine

workdir /go/src/app/
add . .

ENV GO111MODULE off
RUN go build -o helloworld

expose 6112

cmd ["./helloworld"]
