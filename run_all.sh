#!/bin/bash
#clear screen
clear
# Check if there are any running screen sessions
if screen -list | grep -q "No Sockets found"; then
    echo "No screen sessions found."
else
    # Kill all existing screen sessions
    killall screen
    echo "Killed all screen sessions."
fi

# Running the Backend
screen -dmS server bash -c 'flask run --port 5010; exec sh'

# Optional Ngrock Step
screen -dmS ngrock bash -c 'ngrok http --domain=reddiappinterface.ngrok-free.app 5010; exec sh'

# Running Messaging Module
# We use sleep to delay the execution of the messaging module
screen -dmS messaging bash -c 'sleep 10; python3 messaging.py; exec sh'

# Attach to the messaging screen
screen -r messaging
