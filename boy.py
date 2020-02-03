import os
import re
import slack

# This script is inspired by the
#   tutorial https://github.com/mattmakai/slack-starterbot/blob/master/starterbot.py
# and is adopted to slackclient v.2.x using
#   https://github.com/slackapi/python-slackclient/wiki/Migrating-to-2.x


EXAMPLE_COMMAND = "do"  # sample command
MENTION_REGEX = "^<@([WU].+)>(.*)"  # RegEx for parsing command

# don't forget to set the environmental variable SLACK_BOT_TOKEN using
# export SLACK_API_TOKEN='Your Bot User OAuth Access Token'
# or hardcode

slack_token = 'xoxb-918330940978-935245068791-ewj3Ry9FSDiZIy1Ewyj7zqBJ'


@slack.RTMClient.run_on(event='message')
def say_hello(**payload):
    data = payload['data']

    # uncomment if you want to see metadata of all messages
    # print(data)

    if 'text' in data:  # some text is present, let's parse it
        msg_txt = data['text']

        # uncomment if you want to see text of all messages
        print(msg_txt)

        is_the_message_for_me, cmd = parse_message(msg_txt)

        if is_the_message_for_me:
            cmd_result = handle_command(cmd)

            channel_id = data['channel']
            thread_ts = data['ts']
            user = data['user']

            webclient = payload['web_client']
            webclient.chat_postMessage(
                channel=channel_id,
                text="{}".format(cmd_result),
                thread_ts=thread_ts
            )


def parse_message(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the tuple [True, text of the command]
        If there is no direct mention, returns [False, None]
    """
    matches = re.search(MENTION_REGEX, message_text)
    if matches and matches.group(1) == my_user_id:
        return True, matches.group(2).strip()
    else:
        return False, None


def handle_command(cmd):
    """
    Process command and return a result to be printed in a message to a user
    """
    # Default response is help text for the user
    response = "Not sure what you mean. Try *{}*.".format(EXAMPLE_COMMAND)

    # Finds and executes the given command, filling in response
    # This is where you start to implement more commands!
    if cmd.startswith("Echo"):
        cmd = cmd.split()
        response = " ".join(cmd[1:])
        #cmd = cmd.split()
        #response = " ".join(cmd[1:]) if len(cmd[1:])>=1 else ""

    return response


def get_my_user_id(slack_api_token):
    """
    Get bot user id as per https://api.slack.com/methods/auth.test
    """
    return slack.WebClient(slack_token).auth_test()['user_id']


# get user id of the bot
my_user_id = get_my_user_id(slack_token)

# start the bot
rtmclient = slack.RTMClient(token=slack_token)
rtmclient.start()
