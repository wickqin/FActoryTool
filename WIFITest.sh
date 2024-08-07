#!/bin/bash

retry_count=1
error_code="T00358"
wifi_device="SSID: B41F_NPI_5G"

get_wireless_device() {
    local wireless_device=$(iw dev | awk '/Interface/ {print $2}')
    echo "$wireless_device"
}

function check_wireless_device() {
    if ! ip link show "$wireless_device" &> /dev/null; then
        echo "$(date) Wireless device $wireless_device does not exist."
        return 1
    fi
    return 0
}

function wifi_network_check() {
    local attempt
    local ssid_found=0

    for (( attempt=1; attempt<=retry_count; attempt++ )); do
        local scan_output=$(sudo iw dev "$wireless_device" scan | grep "$wifi_device")

        if [[ "$scan_output" != "" ]]; then
            ssid_found=1
            break
        fi

        sleep 5
    done

    if [[ $ssid_found -eq 1 ]]; then
        return 0
    else
        return 1
    fi
}

echo "$(date) Checking for wireless device..."

wireless_device=$(get_wireless_device)

if check_wireless_device; then
    echo "$(date) Wireless device $wireless_device found. Starting WiFi network scan..."

    if wifi_network_check; then
        echo "$(date) WiFi network scan passed"
        exit 0
    else
        echo "$(date) WiFi network scan failed"
        exit 1
    fi
else
    echo "$(date) No wireless device found. Exiting."
    exit 1
fi