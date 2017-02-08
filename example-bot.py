#!/usr/bin/env python

import os, time, sys, signal
from threading import Thread
from ConfigParser import ConfigParser
from GSlack import GSlack

PIDFILE=''

class SlackClient(GSlack):
    def on_message(self, user, channel, output):
        print("#%s [%s] %s" % (channel, user, output))
    def log(self, msg):
        print("[DEBUG] %s" % msg)


def slackRun(client):
    client.run()

def signal_handler(signal, frame):
    global client, PIDFILE
    client.stop()
    os.remove(PIDFILE)
    sys.exit(0)

# Check config and PID file
config=ConfigParser()
config.read('gradewbot.cfg')
BOT_NAME=config.get('main', 'name')
BOT_TOKEN=config.get('main', 'token')
PIDFILE=config.get('main','pidfile')

if os.path.exists(PIDFILE):
    sys.stderr.write("PID file already present!\n")
    sys.exit(1)

# Fork!
newpid=os.fork()
if newpid!=0:
    sys.exit(0)
file(PIDFILE, 'w').write(str(os.getpid()))

# Initialize Slack
client=SlackClient(BOT_NAME, BOT_TOKEN)
if client.connect()==False:
    print("Could not connect!")
    sys.exit(1)
slackThread=Thread(target=slackRun, args=(client,))
slackThread.start()

# Set up signal handler
signal.signal(signal.SIGTERM, signal_handler)

# Main loop of nothingness
while True:
    time.sleep(1)
