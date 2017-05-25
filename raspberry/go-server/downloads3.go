package main

import (
	"fmt"
	"io"
	"os"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/s3"
	"github.com/aws/aws-sdk-go/service/sts"
	// "gopkg.in/yaml.v2"
	// "github.com/aws/aws-sdk-go/service/s3/s3manager"
)

type DownloadConfigInput struct {
	LocalFileName string
}

func download_config(inp *DownloadConfigInput) {
	sess, err := session.NewSession()
	if err != nil {
		panic(err)
	}

	stssvc := sts.New(sess, &aws.Config{Region: aws.String("us-east-1")})
	stsparams := &sts.AssumeRoleInput{
		RoleArn:         aws.String("arn:aws:iam::742524706181:role/ConfigKeyAccess"),
		RoleSessionName: aws.String("golangAssumeRoleTest"),
	}
	_, err = stssvc.AssumeRole(stsparams)
	if err != nil {
		fmt.Println(err.Error())
		return
	}
	// fmt.Println(stsresp)

	svc := s3.New(sess, &aws.Config{Region: aws.String("us-east-1")})
	params := &s3.GetObjectInput{
		Bucket: aws.String("howinator-config"),
		Key:    aws.String("sparkabowl/config.yml"),
	}

	resp, err := svc.GetObject(params)
	if err != nil {
		fmt.Println(err.Error())
		return
	}

	outFile, err := os.Create(inp.LocalFileName)
	defer outFile.Close()

	_, err = io.Copy(outFile, resp.Body)
	if err != nil {
		fmt.Println(err.Error())
		return
	}

}
