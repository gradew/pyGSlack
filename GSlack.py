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

        def log(self, msg):
            pass

        def connect(self):
                self.log("Connecting...")
                try:
                        self.slack_client=SlackClient(self.BOT_TOKEN)
                        self.get_channels()
                        self.get_users()
                        self.slack_client.rtm_connect()
                        self.log("Connected!")
                except:
                        return False
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

        def on_message(self, ts, user, channel, output):
            pass

        def parse_slack_output(self):
                output_list = self.slack_client.rtm_read()
                if output_list and len(output_list) > 0:
                        for output in output_list:
                                #print(output)
                                if output and 'text' in output:
                                        return output['ts'], output['user'], output['channel'], output['text']
                return None, None, None, None

        def run(self):
                self.isRunning=True
                timer=0.5
                counter=0
                waitReconnect=10/timer
                networkError=False
                while self.isRunning:
                        # Try to read from pipe, catch possible exceptions
                        try:
                            if networkError==False:
                                ts, user, channel, output = self.parse_slack_output()
                        except:
                            self.log("Connection failed!")
                            networkError=True
                            counter=0
                        # Handle network errors, keep countdown
                        if networkError:
                            if counter<waitReconnect:
                                counter=counter+1
                            else:
                                counter=0
                                self.log("Attempting to reconnect")
                                if self.connect():
                                    networkError=False
                        else:
                            # All is well, handle the message
                            if user and output and channel:
                                self.on_message(ts, self.arrayUsersReverse[user], self.arrayChannelsReverse[channel], output)
                        time.sleep(timer)

        def stop(self):
                self.isRunning=False
