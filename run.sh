#!/bin/bash

# where the application config dir should be mounted
export CONFIG_DIR=$1

#docker run -p host:exposed my-image
docker run -t -d --name slackbot -v ${CONFIG_DIR}:/mnt/config -p 1024:1024 claytantor/chatscript-slackbot4py:latest
