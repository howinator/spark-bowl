package main

import (
    "io"
    "fmt"
    "github.com/aws/aws-sdk-go/aws/session"
    "github.com/aws/aws-sdk-go/service/s3"
    "net/http"
    "encoding/json"
)

type DogSignal struct {
    Key string
    Type string
}

func hello(w http.ResponseWriter, r *http.Request) {
    io.WriteString(w, "Hello world!")
}

func feed_dogs_handler(w http.ResponseWriter, r *http.Request) {
    var request DogSignal
    if r.Body == nil {
        http.Error(w, "Please send a request body", 400)
        return
    }
    err := json.NewDecoder(r.Body).Decode(&request)
    if err != nil {
        http.Error(w, err.Error(), 500)
        return
    }
    // a := []byte(request.Type)
    // // copy(request.Type, a[:])
    // w.Header().Set("Content-Type", "text/html; charset=utf-8")
    // w.Write(a)
    // w.WriteHeader(200)
    // return
    fmt.Fprintf(w, request.Type)
}

func main() {
    http.HandleFunc("/", feed_dogs_handler)
    http.ListenAndServe(":8080", nil)
}