#!/bin/bash

# Builds Docker image and pushes to ECR repo

aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin 076415213549.dkr.ecr.eu-west-1.amazonaws.com
docker build -t anpr-custom-inference .
docker tag anpr-custom-inference:latest 076415213549.dkr.ecr.eu-west-1.amazonaws.com/anpr-custom-inference:latest
docker push 076415213549.dkr.ecr.eu-west-1.amazonaws.com/anpr-custom-inference:latest