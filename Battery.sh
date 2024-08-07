#!/bin/bash

echo battery.sh
rm -f batterycapacity.txt

# set retry cycle count
COUNT=1
ErrorCode=T00075

echo -en "\\033[33m\\033[1m battery capacity check \\033[0m\n"
logFilePath="/tools/log"

# battery capacity check
function battery_capacity_check(){
    for count in $(seq 1 $1)
        do
            acpi >batterycapacity.txt
            battery=$(cat batterycapacity.txt)
            batteryID=${battery#*,}
            batteryID=${batteryID%%%*}
            if [[ $batteryID -gt 20 ]]; then
                return 0
            else
                ./testMessageBox -FAIL -E:"$ErrorCode" -S:"battery capacity check fail"
                # add delay 5 seconds
                ping -c 5 127.0.0.1 >/dev/null 2>&1
            fi
    done
    return 1
}

echo $(date) "电池电量检查开始"

battery_capacity_check $COUNT
if [ $? -eq 0 ]; then
    # battery capacity check
    echo $(date) "电池电量($batteryID)检查开始pass"
    rm -f $0.ttt
    exit 0
else
    ./uploadErrorCode.sh $0 $ErrorCode
    exit 1
fi