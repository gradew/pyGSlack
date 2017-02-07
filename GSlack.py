#!/usr/bin/env python

import os, time
from slackclient import SlackClient

class GSlack:
        slack_client = None
        arrayChannels={}
        arrayChannelsReverse={}
        arrayUsers={}
        arrayUsersReverse={}
        isRunning = None

        def __init__(self, botName, botToken):
                self.BOT_NAME=botName
                self.BOT_TOKEN=botToken
                self.isRunning=False

        def connect(self):
                try:
                        self.slack_client=SlackClient(self.BOT_TOKEN)
                except:
                        return False
                self.get_channels()
                self.get_users()
                self.slack_client.rtm_connect()
                return True

        def get_channels(self):
                api_call = self.slack_client.api_call("channels.list")
                if api_call.get('ok'):
                        channels = api_call.get('channels')
                        for channel in channels:
                                channelID=channel['id']
                                channelName=channel['name']
                                self.arrayChannels[channelName]=channelID
                                self.arrayChannelsReverse[channelID]=channelName
                else:
                        return False

                api_call = self.slack_client.api_call("groups.list")
                if api_call.get('ok'):
                        channels = api_call.get('groups')
                        for channel in channels:
                                channelID=channel['id']
                                channelName=channel['name']
                                self.arrayChannels[channelName]=channelID
                                self.arrayChannelsReverse[channelID]=channelName
                else:
                        return False

        def get_users(self):
                api_call = self.slack_client.api_call("users.list")
                if api_call.get('ok'):
                        users = api_call.get('members')
                        for user in users:
                                userID=user['id']
                                userName=user['name']
                                self.arrayUsers[userName]=userID
                                self.arrayUsersReverse[userID]=userName

        def send_message(self, channel, message):
            self.slack_client.api_call("chat.postMessage", channel=self.arrayChannels[channel], text=message, as_user=True)

        def on_message(self, user, channel, output):
            pass

        def parse_slack_output(self):
                output_list = self.slack_client.rtm_read()
                if output_list and len(output_list) > 0:
                        for output in output_list:
                                #print(output)
                                if output and 'text' in output:
                                        return output['user'], output['channel'], output['text']
                return None, None, None

        def run(self):
                self.isRunning=True
                while self.isRunning:
                        user, channel, output = self.parse_slack_output()
                        if user and output and channel:
                            self.on_message(self.arrayUsersReverse[user], self.arrayChannelsReverse[channel], output)
                        time.sleep(0.5)

        def stop(self):
                self.isRunning=False

