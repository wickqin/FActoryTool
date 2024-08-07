#!/bin/bash

# Set retry cycle count
retry_count=1

function blue_tooth_check() {
    local scan_output
    local found_device=0

    for (( attempt=1; attempt<=retry_count; attempt++ )); do
        scan_output=$(hcitool scan)

        if [[ -n "$scan_output" ]]; then
            found_device=1
            break
        fi

        sleep 5
    done

    if [[ $found_device -eq 1 ]]; then
        return 0
    else
        return 1
    fi
}

echo "$(date) BlueTooth function test started"

if blue_tooth_check "$retry_count"; then
    echo "$(date) BlueTooth function test passed"
    exit 0
else
    echo "$(date) No Bluetooth devices detected"
    exit 1
fi