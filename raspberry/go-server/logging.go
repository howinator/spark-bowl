package main

import (
	"fmt"
	"io"
	"log"
	"os"
)

type logOutputs struct {
	Trace   *io.Writer
	Info    *io.Writer
	Warning *io.Writer
	Error   *io.Writer
}

type Loggers struct {
	Trace   *log.Logger
	Info    *log.Logger
	Warning *log.Logger
	Error   *log.Logger
}

var logger Loggers
var loggerOutputs *logOutputs

func init() {
	// FIXME this is overloading the env setting - make more specific log setting flag
	env := os.Getenv("SPARKABOWL_DEPLOY_ENV")

	loggerOutputs = findOutputs(env)

	logger.Trace = log.New(*loggerOutputs.Trace,
		"TRACE: ",
		log.Ldate|log.Ltime|log.Lshortfile)
	logger.Info = log.New(*loggerOutputs.Info,
		"INFO: ",
		log.Ldate|log.Ltime|log.Lshortfile)
	logger.Warning = log.New(*loggerOutputs.Warning,
		"WARNING: ",
		log.Ldate|log.Ltime|log.Lshortfile)
	logger.Error = log.New(*loggerOutputs.Error,
		"ERROR: ",
		log.Ldate|log.Ltime|log.Lshortfile)

}

func findOutputs(env string) *logOutputs {
	file := "log/sparkabowl.log"
	var err error = nil
	var lf io.Writer
	var logToFile bool = env != "" && env != "dev"

	if logToFile {
		lf, err = os.OpenFile(file, os.O_WRONLY|os.O_APPEND|os.O_CREATE, 0644)
	} else {
		lf = os.Stdout
	}
	if err != nil {
		fmt.Printf("openLogFile: os.OpenFile:", err)
		os.Exit(1)
	}
	wr := &lf
	// better logic about what level gets what can go here
	outputs := &logOutputs{wr, wr, wr, wr}
	return outputs
}
