package main

import (
    "io"
    "net/http"
    "encoding/json"
)

func hello(w http.ResponseWriter, r *http.Request) {
    io.WriteString(w, "Hello world!")
}

func main() {
    http.HandleFunc("/", hello)
    http.ListenAndServe(":8000", nil)
}