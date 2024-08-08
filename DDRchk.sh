#!/bin/bash

echo DDRchk.sh
#source test.sh
#source SN.sh
source devcfg.sh
rm -f ddrchk_result.sh

# set retry cycle count
COUNT=1
ErrorCode=T00008
memory_location_handle=()

echo -en "\\033[33m\\033[1m check memory configuration \\033[0m\n"
logFilePath="/tools/log"
DDR=2

# memory number check
function memory_number_check() {
    for count in $(seq 1 $1); do
        DDRnumber=$(dmidecode -t 17 | grep "Manufacturer: Kimtigo Semiconductor (HK) Limited" | wc -l)
        if [ "$DDR" == "$DDRnumber" ]; then
            return 0
        else
            ./testMessageBox -FAIL -E:"$ErrorCode" -S:"memory number check fail"

            source devcfg.sh
            # add delay 5 seconds
            ping -c 5 127.0.0.1 >/dev/null 2>&1
        fi
    done
    return 1
}

# memory info check
function memory_info_check() {
    for count in $(seq 1 $1); do
        mem_size_type_slot_check
        if [ $? -eq 0 ]; then
            memory_size_check
            if [ $? -eq 0 ]; then
                memory_speed_check
                if [ $? -eq 0 ]; then
                    return 0
                else
                    ./testMessageBox -FAIL -E:"$ErrorCode" -S:"memory speed check fail"
                    # add delay 5 seconds
                    ping -c 5 127.0.0.1 >/dev/null 2>&1
                fi
            else
                ./testMessageBox -FAIL -E:"$ErrorCode" -S:"memory size check fail"
                # add delay 5 seconds
                ping -c 5 127.0.0.1 >/dev/null 2>&1
            fi
        else
            ./testMessageBox -FAIL -E:"$ErrorCode" -S:"memory type check fail"
            # add delay 5 seconds
            ping -c 5 127.0.0.1 >/dev/null 2>&1
        fi
        rm -f ddrchk_result.sh
        # add delay 5 seconds
        ping -c 5 127.0.0.1 >/dev/null 2>&1
    done
    return 1
}

# memory size type slot check
function mem_size_type_slot_check() {
    DDRtype=$(dmidecode -t 17 | grep "Form Factor: SODIMM" | wc -l)
    if [ "$DDR" == "$DDRtype" ]; then
        return 0
    fi
    return 1
}

# memory size check
#dmidecode -t 17 | grep -A33 $2 | egrep -e "Type:\sDDR|Size:\s[0-9]{1,8}\sMB|Locator:\sDIMM"|sed -e 's/^[\t]//'|sed -e "s/DIMM//g"|sed -e "s/:/=/g"|sed "s/ //g"
function memory_size_check() {
    DDRsize=$(dmidecode -t 17 | grep "Size: 8192 MB" | wc -l)
    if [ "$DDR" == "$DDRsize" ]; then
        return 0
    fi
    return 1
}

# memory type check
function memory_speed_check() {
    DDRspeed=$(dmidecode -t 17 | grep "Configured Memory Speed: 2666 MT/s" | wc -l)
    if [ "$DDR" == "$DDRspeed" ]; then
        return 0
    fi
    return 1
}

echo $(date) "DDR配置检查start"

if [ "$DDR" = "0" ]; then
    echo $(date) "no ddr"
    exit 0
fi

# check memory number
memory_number_check $COUNT
if [ $? -eq 0 ]; then
    # echo memory number check ok
    echo $(date) "DDR数量($DDR)检查pass"
else

    rm -f ddrchk_result.sh
    exit 1
fi

# check memory info
memory_info_check $COUNT
if [ $? -eq 0 ]; then
    # echo memory type check ok
    echo $(date) "DDR配置检查pass"
    exit 0
else
    exit 1
fi
