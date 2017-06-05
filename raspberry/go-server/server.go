package main

import (
	// "fmt"
	"net/http"
)

func handler(rw http.ResponseWriter, r *http.Request) {

	if r.Method != "POST" {

	}

}

func main() {
	var addr = ":8080"
	http.HandleFunc("/", handler)
	http.ListenAndServe(addr, handler)
}
