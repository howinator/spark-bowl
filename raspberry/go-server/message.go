package main

import (
	//"encoding/json"
	"io"
	//"bytes"
	"time"
	"crypto/hmac"
	"crypto/sha512"
)

type Message struct {
	Timestamp int64 `json:"timestamp"`
	Type      string `json:"type"`
}

const allowedMessageExpiry = 2

func (m *Message) processMessage(mbody io.ReadCloser) error {


	//buf := new(bytes.Buffer)
	//buf.ReadFrom(mbody)
	//
	//err := json.Unmarshal(buf.Bytes(), m)
	//
	//return err
	return nil

}

func (m *Message) validElapsedTime() bool {

	sendTime := time.Unix(m.Timestamp, 0)
	now := time.Now()

	elapsed := sendTime.Sub(now)

	elapsedInSec := int64(elapsed/time.Second)

	if elapsedInSec < allowedMessageExpiry {
		return true
	} else {
		return false
	}
}

func signatureValid(reqBody string, sentMAC string, secret string) bool  {

	mac := hmac.New(sha512.New, []byte(secret))
	mac.Write([]byte(reqBody))

	expectedMac := mac.Sum(nil)
	return hmac.Equal([]byte(sentMAC), expectedMac)

}
