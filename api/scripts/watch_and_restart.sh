#!/bin/bash

./scripts/start.sh  # Start the server (now in the scripts directory)

while true; do
    files_changed=$(find app -name "*.py" -newermt "5 seconds ago")

    if [[ -n "$files_changed" ]]; then
        sleep 5  # Wait for 5 seconds
        ./scripts/start.sh  # Restart the script
    fi

    sleep 1  # Check for changes every second
done
