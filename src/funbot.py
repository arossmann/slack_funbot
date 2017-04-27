import os, random, time
from slackclient import SlackClient

# delay in seconds before checking for new events
SOCKET_DELAY = 1
# slackbot environment variables
SLACK_FUN_NAME = os.environ.get('SLACK_FUN_NAME')
SLACK_FUN_TOKEN = os.environ.get('SLACK_FUN_TOKEN')
SLACK_FUN_ID = os.environ.get('SLACK_FUN_ID')

SLACK_FUN_client = SlackClient(SLACK_FUN_TOKEN)

def is_for_me(event):
    """Know if the message is dedicated to me"""
    # check if not my own event
    type = event.get('type')
    if type and type == 'message' and not(event.get('user')==SLACK_FUN_ID):
        # in case it is a private message return true
        if is_private(event):
            return True
        # in case it is not a private message check mention
        if len(event.get('text')) > 0:
            text = event.get('text')
            channel = event.get('channel')
            if SLACK_FUN_mention in text.strip().split():
                return True
        else:
            return False

def post_message(message, channel):
    SLACK_FUN_client.api_call('chat.postMessage', channel=channel,
                          text=message, as_user=True)
def is_private(event):
    """Checks if private slack channel"""
    return event.get('channel').startswith('D')

def get_mention(user):
    return '<@{user}>'.format(user=user)

SLACK_FUN_mention = get_mention(SLACK_FUN_ID)

def is_roflcopter(message):
    tokens = [word.lower() for word in message.strip().split()]
    return any(g in tokens
               for g in ['roflcopter', 'rofl'])

def is_hi(message):
    tokens = [word.lower() for word in message.strip().split()]
    return any(g in tokens
               for g in ['hello', 'bonjour', 'hey', 'hi', 'sup', 'morning', 'hola', 'ohai', 'yo'])


def is_bye(message):
    tokens = [word.lower() for word in message.strip().split()]
    return any(g in tokens
               for g in ['bye', 'goodbye', 'revoir', 'adios', 'later', 'cya'])

def say_hi(user_mention):
    """Say Hi to a user by formatting their mention"""
    response_template = random.choice(['Sup, {mention}...',
                                       'Yo!',
                                       'Hola {mention}',
                                       'Bonjour!'])
    return response_template.format(mention=user_mention)


def say_bye(user_mention):
    """Say Goodbye to a user"""
    response_template = random.choice(['see you later, alligator...',
                                       'adios amigo',
                                       'Bye {mention}!',
                                       'Au revoir!'])
    return response_template.format(mention=user_mention)

def say_roflcopter():
    """ Give the user the roflcopter"""
    reponse = "You asked for the roflcopter? Here you go. http://i.imgur.com/AeAFkEf.gif"
    return reponse

def message_too_short():
    """message has no content"""
    response = 'Yep. it\'s me.'
    return response

def handle_message(message, user, channel):
    if len(message) == 0:
        post_message(message=message_too_short(),channel=channel)
    elif is_hi(message):
        user_mention = get_mention(user)
        post_message(message=say_hi(user_mention), channel=channel)
    elif is_bye(message):
        user_mention = get_mention(user)
        post_message(message=say_bye(user_mention), channel=channel)
    elif is_roflcopter(message):
        post_message(message=say_roflcopter(),channel=channel)

def run():
    if SLACK_FUN_client.rtm_connect():
        print('[.] FUN Bot is ON...')
        while True:
            event_list = SLACK_FUN_client.rtm_read()
            if len(event_list) > 0:
                for event in event_list:
                    print(event)
                    if is_for_me(event):
                        handle_message(message=event.get('text'), user=event.get('user'), channel=event.get('channel'))
            time.sleep(SOCKET_DELAY)
    else:
        print('[!] Connection to Slack failed.')

if __name__=='__main__':
    run()