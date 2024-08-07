#!/bin/bash

echo "CheckEC.sh"
rm -f pd_fw.txt

# set retry cycle count
COUNT=1
ErrorCode=T00075

echo -en "\\033[33m\\033[1m Check PD_FW \\033[0m\n"
logFilePath="/tools/log"

# PD_FW check
function PD_FW_check(){
    for count in $(seq 1 $1)
        do
            ./sp41x6g-fw-ver  > pd_fw.txt
            PD_FW_version=$(cat pd_fw.txt | grep -i "PD Version: V1.9.16"|wc -l)
            if [[ $PD_FW_version -eq 1 ]]; then
                return 0
            else
                ../testMessageBox -FAIL -E:"$ErrorCode" -S:"PD_FW check fail"
                # add delay 5 seconds
                ping -c 5 127.0.0.1 >/dev/null 2>&1
            fi
    done
    return 1
}

echo $(date) "Check PD_FW Start"

PD_FW_check $COUNT
if [ $? -eq 0 ]; then
    echo $(date) "PD_FW Check Pass"
    exit 0
else
    exit 1
fi