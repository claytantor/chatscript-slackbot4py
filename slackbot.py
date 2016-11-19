#!/usr/bin/env python
# coding: utf-8
import sys
import sockethandler
import json
import time
import sockethandler

from slackclient import SlackClient

# constants
EXAMPLE_COMMAND = "do"

def get_bot_id(slack_client, app_config):
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        # retrieve all users so we can find our bot
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == app_config['bot-name']:
                print("Bot ID for '" + user['name'] + "' is " + user.get('id'))
                return user.get('id')
    else:
        print("could not find bot user with the name " + BOT_NAME)
        return None

def handle_command(
    slack_client, command, channel,
    user="claytantor", robotName="harry",
    hostName="localhost", portNumber=1024):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
               "* command with numbers, delimited by spaces."
    if command.startswith(EXAMPLE_COMMAND):
        response = "Sure...write some more code then I can do that!"
    else:
        #response = "Sure...write some more code then I can do that!"
        client = sockethandler.SocketHandler()
        message = "{0}\x00{1}\x00{2}\x00".format(user, robotName, command);
        client.connect(hostName, portNumber)
        client.send(message)
        response = client.receive()
        client.close()

    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)

def parse_slack_output(slack_client, slack_rtm_output, config, bot_id):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """

    at_bot = "<@{0}>".format(bot_id)
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and at_bot in output['text']:
                # return text after the @ mention, whitespace removed
                return output['user'], output['text'].split(at_bot)[1].strip().lower(), \
                       output['channel']

    return None, None, None

def main(argv):
    configuration_filename = argv[0]

    app_config = []
    with open(configuration_filename) as json_data:
        app_config = json.load(json_data)

    hostName = app_config['chatscript-host-name']
    portNumber = app_config['chatscript-port']
    robotName = app_config['chatscript-bot-name']

    print "starting up slackbot with token: {0}".format(app_config['slack-bot-token'])
    slack_client = SlackClient(app_config['slack-bot-token'])

    bot_id = get_bot_id(slack_client, app_config)

    if bot_id:
        READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
        if slack_client.rtm_connect():
            print("{0} connected and running!".format(app_config['bot-name']))
            while True:
                user, command, channel = parse_slack_output(slack_client, slack_client.rtm_read(), config=app_config, bot_id=bot_id)
                if command and channel:
                    handle_command(slack_client, command, channel, user=user, robotName=robotName)
                time.sleep(READ_WEBSOCKET_DELAY)
        else:
            print("Connection failed. Invalid Slack token or bot ID?")
    else:
        print "could not authenticate token."

if __name__ == "__main__":
    main(sys.argv[1:])
