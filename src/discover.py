import os, slackclient

SLACK_FUN_NAME = os.environ.get('SLACK_FUN_NAME')
SLACK_FUN_TOKEN = os.environ.get('SLACK_FUN_TOKEN')
# initialize slack client
slack_client = slackclient.SlackClient(SLACK_FUN_TOKEN)
# check if everything is alright
print(SLACK_FUN_NAME)
print(SLACK_FUN_TOKEN)
is_ok = slack_client.api_call("users.list").get('ok')
# find the id of our slack bot
if(is_ok):
    for user in slack_client.api_call("users.list").get('members'):
        if user.get('name') == SLACK_FUN_NAME:
            print(user.get('id'))
print(is_ok)
