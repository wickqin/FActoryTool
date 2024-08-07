#!/bin/bash

echo CheckFan.sh
# set retry cycle count
COUNT=1
ErrorCode=T00260

echo -en "\\033[33m\\033[1m Fan Speed Check \\033[0m\n"
logFilePath="/tools/log"

function fan_test_check() {
    for count in $(seq 1 $1); do
		fan_speed=$(./sp41-hwmon)
        echo Speed of the fan = $fan_speed
        if [ $fan_speed != "0" ]; then
            return 0
        else
            ../testMessageBox -FAIL -E:"$ErrorCode" -S:"未检测到风扇"
            # add delay 5 seconds
            ping -c 5 127.0.0.1 >/dev/null 2>&1
        fi
    done
    return 1
}

echo $(date) "Fan测试start"
cd ./sp41-hwmon
fan_test_check $COUNT
if [ $? -eq 0 ]; then
    # lcd function test and check ok
    echo $(date) "Fan测试pass"
    cd ..
    exit 0
else
    exit 1
fi
