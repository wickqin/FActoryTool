#!/bin/bash

echo "CheckEC.sh"
rm -f ec.txt

# set retry cycle count
COUNT=1
ErrorCode=T00075

echo -en "\\033[33m\\033[1m Check EC & PD_FW capacity check \\033[0m\n"
logFilePath="/tools/log"

# EC check
function ec_check(){
    for count in $(seq 1 $1)
        do
            ./sp41x6g-fw-ver  > ec.txt
            ec_version=$(cat ec.txt | grep -i "EC version: 01.02"|wc -l)
            if [[ $ec_version -eq 1 ]]; then
                return 0
            else
                ../testMessageBox -FAIL -E:"$ErrorCode" -S:"ec check fail"
                # add delay 5 seconds
                ping -c 5 127.0.0.1 >/dev/null 2>&1
            fi
    done
    return 1
}

echo $(date) "Check EC Start"

ec_check $COUNT
if [ $? -eq 0 ]; then
    echo $(date) "EC Check Pass"
    exit 0
else
    exit 1
fi