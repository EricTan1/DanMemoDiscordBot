#!/bin/bash

# How many seconds to wait between heartbeat checks
HEARTRATE=300
# How many times to retry before restarting the bot
RETRIES=3

# This makes sure the bot is shutdown if
# the sentinel script itself is killed or interrupted
__cleanup()
{
    SIGNAL=$1

    # Kill the bot, if it is still running
    if [[ $(ps -p $pid) == *"python"* ]]
    then
        kill -15 $pid
    fi

    # when this function was called due to receiving a signal
    # disable the previously set trap and kill yourself with
    # the received signal
    if [ -n "$SIGNAL" ]
    then
        trap $SIGNAL
        kill -${SIGNAL} $$
    fi
}

trap '__cleanup 1' HUP
trap '__cleanup 2' INT
trap '__cleanup 3' QUIT
trap '__cleanup 13' PIPE
trap '__cleanup 15' TERM


# Change to dir that contains this script
cd "$(dirname "$0")"

while true
do
    echo "Starting bot"
    ./run.sh &
    # Short wait to make sure the python interpreter is running
    sleep 1
    pid=$(ps x | grep app.py | grep python | awk '{print $1}')
    echo "Bot running with PID $pid"

    # Give the bot some time to start and write the first timestamp
    sleep 10

    timestamp=$(cat DanMemoDiscordBot/heartbeat-file.txt)
    count=0
    while [ "$count" -lt $RETRIES ]
    do
        sleep $HEARTRATE
        new_timestamp=$(cat DanMemoDiscordBot/heartbeat-file.txt)

        if [ $timestamp -eq $new_timestamp ]
        then
            count=$((count+1))
            echo "No heartbeat. Retrying $count..."
        fi

        timestamp=$new_timestamp
    done

    # Kill the bot, if it is still running
    if [[ $(ps -p $pid) == *"python"* ]]
    then
        kill -15 $pid
    fi
done
