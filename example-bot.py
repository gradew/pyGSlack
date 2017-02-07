#!/usr/bin/env python

import os, time, sys
from threading import Thread
from ConfigParser import ConfigParser
from GSlack import GSlack

class SlackClient(GSlack):
    def on_message(self, user, channel, output):
        print("#%s [%s] %s" % (channel, user, output))

config=ConfigParser()
config.read('gradewbot.cfg')
BOT_NAME=config.get('main', 'name')
BOT_TOKEN=config.get('main', 'token')

client=SlackClient(BOT_NAME, BOT_TOKEN)
if client.connect()==False:
    print("Could not connect!")
    sys.exit(1)
client.run()
