import databutton as db
slack_token = db.secrets.get("slack-token")


import json
import requests

def post_message_to_slack(text, slack_channel, 
                                slack_icon_emoji, 
                                slack_user_name, 
                                blocks = None):
    return requests.post('https://slack.com/api/chat.postMessage', {
        'token': slack_token,
        'channel': slack_channel,
        'text': text,
        'icon_emoji': slack_icon_emoji,
        'username': slack_user_name,
        'blocks': json.dumps(blocks) if blocks else None
    }).json()

