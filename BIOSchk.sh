#!/bin/bash

echo BIOSchk.sh
rm -f bioschk_result.sh

# set retry cycle count
COUNT=1
ErrorCode=T00181

Version="Version=NBEH3350M03"
ReleaseDate="ReleaseDate=07/23/2024"
echo -en "\\033[33m\\033[1m check bios configuration \\033[0m\n"
logFilePath="/tools/log"

# bios version check
function bios_version_check() {
    BiosVer=$(dmidecode -t bios | grep "Version:" | sed -e "s/:/=/g" | sed -e 's/^[\t]//' \-e'/Version:/i\\' | sed "s/ //g")
    echo -----$BiosVer-----
    if [ "$BiosVer" == "$Version" ]; then
        return 0
    else
        ./testMessageBox -FAIL -E:"$ErrorCode" -S:"check bios version fail"
        rm -f bioschk_result.sh
        source devcfg.sh
        # add delay 5 seconds
        ping -c 5 127.0.0.1 >/dev/null 2>&1
    fi
    return 1
}

# bios date check
function bios_date_check() {
    BiosDate=$(dmidecode -t bios | grep "Release Date:" | sed -e "s/:/=/g" | sed -e 's/^[\t]//' \-e'/Version:/i\\' | sed "s/ //g")
    echo -----$BiosDate-----
    if [ "$BiosDate" == "$ReleaseDate" ]; then
        return 0
    else
        ./testMessageBox -FAIL -E:"$ErrorCode" -S:"check bios date fail"
        rm -f bioschk_result.sh
        source devcfg.sh
        # add delay 5 seconds
        ping -c 5 127.0.0.1 >/dev/null 2>&1
    fi
    return 1
}

echo $(date) "bios版本日期检查start"

bios_version_check $COUNT
if [ $? -eq 0 ]; then
    # echo bios version check ok
    echo $(date) "bios Version($BiosVer)版本检查pass"
else
    rm -f bioschk_result.sh
    exit 1
fi

bios_date_check $COUNT
if [ $? -eq 0 ]; then
    # bios date check ok
    echo $(date) "bios Date($BiosDate)日期检查pass"
    rm -f $0.ttt
    rm -f bioschk_result.sh
    exit 0
else
    rm -f bioschk_result.sh
    exit 1
fi
