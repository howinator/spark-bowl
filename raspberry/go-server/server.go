package main

import (
	// "errors"
	"fmt"
	"log"
	"net/http"
	"os"
	"bytes"
	"github.com/stianeikeland/go-rpio"
)

var secretKey = getSecretKey()


func handler(rw http.ResponseWriter, r *http.Request) {
	// platform specific code
	if r.Method != "POST" {
		http.Error(rw, "Must be a POST request", 405)
		logger.Error.Println("method was wrong")
	}
	if r.Body == nil {
		http.Error(rw, "Request must have body", 400)
	}
	m := Message{}
	signature := r.Header.Get("Signature")

	err := m.processMessage(r.Body)

	if err != nil {
		logger.Error.Println("Message processing error")
		return
	}

	buf := bytes.Buffer{}
	buf.ReadFrom(r.Body)

	validHMAC := signatureValid(buf.String(), signature, secretKey)

	if !validHMAC {
		logger.Error.Println("Invalid HMAC Signature - stranger danger!")
		return
	}

	if !m.validElapsedTime() {
		logger.Error.Println("Too much time has elapsed between message send and now")
		return
	}


	if m.Type == "FeedDogsNow" {
		err = rpio.Open()
		pin := rpio.Pin(10)
		pin.Output()

		pin.High()
		pin.Low()

		rpio.Close()
	}
	// json.NewDecoder(r.Body).Decode(&m)
	// if err != nil {
	// 	panic(err)
	// }

}



func main() {
	var port string

	port = ":" + os.Getenv("SPARKABOWL_PORT")
	if port == "" {
		port = ":8082"
	}


	// s := &http.Server{
	// 	Handler: handler,
	// }

	http.HandleFunc("/", handler)
	log.Fatal(http.ListenAndServe(port, nil))
	fmt.Printf("got here")
}
