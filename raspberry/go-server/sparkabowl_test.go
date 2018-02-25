package main

import (
	"math/rand"
	"os"
	"testing"
	"time"
)

// FINISH TESTING

var letters = []rune("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")

func randSeq(n int) string {
	b := make([]rune, n)
	rand.Seed(time.Now().UTC().UnixNano())
	for i := range b {
		b[i] = letters[rand.Intn(len(letters))]
	}
	return string(b)
}

func TestDownloadConfig(t *testing.T) {
	filename := "/tmp/" + randSeq(8)
	configparams := &DownloadConfigInput{LocalFileName: filename}
	downloadConfig(configparams)
	_, err := os.Stat(filename)
	if err != nil {
		t.Error("File did not download successfully!")
	}
}
