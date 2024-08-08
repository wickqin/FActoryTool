#!/bin/bash

echo CardTest.sh

# set retry cycle count
COUNT=1
ErrorCode=T00051

echo -en "\\033[33m\\033[1m check card reader configuration \\033[0m\n"

logFilePath="/SDCard"
path="/mnt/CardTest.ok"
umount /mnt

# blue tooth check
function sd_crad_test() {
    for count in $(seq 1 $1); do
        sd=$(lsblk | egrep "SD" | sed -n '1p')
        sd=${sd#*└─}
        sd=${sd%% *}
        mount /dev/$sd /mnt
        if [ -f "$path" ]; then
            return 0
        else
            ./testMessageBox -FAIL -E:"$ErrorCode" -S:"check card reader fail"
            # add delay 5 seconds
            ping -c 3 127.0.0.1 >/dev/null 2>&1
        fi
    done
    return 1
}

echo $(date) "card功能测试start"

if [ "$card" = "0" ]; then
    exit 0
fi

sd_crad_test $COUNT
if [ $? -eq 0 ]; then
    echo crad test ok
    umount /dev/$sd
    echo $(date) "card功能测试pass"
    exit 0
else
    exit 1
fi
