# chatscript-slackbot4py
This project is a slackbot built on top of the [claytantor/chatscript-docker](https://hub.docker.com/r/claytantor/chatscript-docker/)
image but the slackbot bot client added on top of it.

## Create A slackbot user
To enable your slackbot you need to create a slackbot user. You can find the
documentation for getting your slackbot user token at the
[Bot Users](https://api.slack.com/bot-users) docs.


## Building a configuration
Because configurations are secrets, the application config is not part of the
container. When the container is started an **application.json** file should
be available relative to the mount point (see run instructions below).

```
{
    "slack-bot-token":"[your slack bot user token]",
    "bot-name":"bebot",
    "chatscript-host-name":"localhost",
    "chatscript-port":1024,
    "chatscript-bot-name":"harry"
}
```

## Running The Container
```
export HOST_CONFIG_DIR=/home/claytantor/config
docker run -t -d --name slackbot -v ${HOST_CONFIG_DIR}:/mnt/config \
    -p 1024:1024 claytantor/chatscript-slackbot4py:latest
```

## Building The Container

`docker build -t claytantor/chatscript-slackbot4py:latest .`
