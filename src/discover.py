import os, slackclient

SLACK_FUN_NAME = os.environ.get('SLACK_FUN_NAME')
SLACK_FUN_TOKEN = os.environ.get('SLACK_FUN_TOKEN')
# initialize slack client
valet_slack_client = slackclient.SlackClient(SLACK_FUN_TOKEN)
# check if everything is alright
print(SLACK_FUN_NAME)
print(SLACK_FUN_TOKEN)
is_ok = valet_slack_client.api_call("users.list").get('ok')
print(is_ok)