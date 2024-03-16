#!/bin/bash

clear

declare -a arr=("server" "ngrock" "messaging")

if screen -list | grep -q "No Sockets found"; then
    echo "No screen sessions found."
else
    for i in "${arr[@]}"
    do
        pkill -f "$i"
        echo "Killed screen session $i."
    done
fi

screen -dmS server bash -c 'flask run --port 5010; exec sh'

screen -dmS ngrock bash -c 'ngrok http --domain=reddiappinterface.ngrok-free.app 5010; exec sh'

screen -dmS messaging bash -c 'sleep 10; python3 messaging.py; exec sh'

sleep 5

screen -r messaging
