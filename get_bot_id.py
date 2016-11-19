#!/usr/bin/env python
# coding: utf-8

import os
from slackclient import SlackClient
import json

BOT_NAME = 'bebot'

if __name__ == "__main__":

    d = []
    with open('application.json') as json_data:
        d = json.load(json_data)

    #print "using token for bot:{0}".format(d['slack-bot-token'])
    slack_client = SlackClient(d['slack-bot-token'])

    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        # retrieve all users so we can find our bot
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == BOT_NAME:
                print("Bot ID for '" + user['name'] + "' is " + user.get('id'))
    else:
        print("could not find bot user with the name " + BOT_NAME)
