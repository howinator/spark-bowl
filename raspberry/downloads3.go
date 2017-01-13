package main

import (
    "fmt"

    "github.com/aws/aws-sdk-go/aws"
    "github.com/aws/aws-sdk-go/aws/session"
    "github.com/aws/aws-sdk-go/service/sts"
    "github.com/aws/aws-sdk-go/service/s3"
    "github.com/aws/aws-sdk-go/service/s3/s3manager"
)

func main() {
    sess, err := session.NewSession()
    if err != nil {
        panic(err)
    }

    stssvc := sts.New(sess)
    params := &sts.AssumeRoleInput{
        RoleArn: aws.String("arn:aws:iam::742524706181:role/ConfigKeyAccess"),
        RoleSessionName: aws.String("golangAssumeRoleTest"),
    }
    resp, err := stssvc.AssumeRole(params)
    svc := s3.New(sess, &aws.Config{Region: aws.String("us-east-1")})
    params := &s3.GetObjectInput{
        Bucket: aws.String("howinator-config"),
        Key: aws.String("sparkabowl/config.yml"),
    }

    resp, err := svc.GetObject(params)
    if err != nil {
        fmt.Println(err.Error())
        return
    }

    fmt.Println(resp)
}