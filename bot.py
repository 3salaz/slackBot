from asyncio import events
from typing import ChainMap
import slack
import os
from flask import Flask
from pathlib import Path
from dotenv import load_dotenv
from slackeventsapi import SlackEventAdapter
env_path = Path('.') / '.env'
app = Flask(__name__)
events_endpoint = '/slack/events'
load_dotenv(dotenv_path=env_path)

slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'] , events_endpoint , app)
client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
BOT_ID = client.api_call("auth.test")['user_id']


@slack_event_adapter.on('message')
def message(slackApiData):
     event = slackApiData.get('event',{})
     token = slackApiData.get('token',{})
     print(slackApiData)
     print(token)
     channel_id = event.get('channel')
     user_id = event.get('user')
     text = event.get('text')

     if BOT_ID != user_id: 
          client.chat_postMessage(channel=channel_id, text=slackApiData);

    
if __name__ == "__main__":
     app.run(debug=True)