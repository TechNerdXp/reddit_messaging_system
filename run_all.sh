#!/bin/bash

clear
# Kill all existing screen sessions
killall screen

# Running the Backend
screen -dmS server bash -c 'flask run --port 5010; exec sh'

# Optional Ngrock Step
screen -dmS ngrock bash -c 'ngrok http --domain=https://reddiappinterface.ngrok-free.app 5010; exec sh'

# Running Messaging Module
# We use sleep to delay the execution of the messaging module
screen -dmS messaging bash -c 'sleep 10; python3 messaging.py; exec sh'
