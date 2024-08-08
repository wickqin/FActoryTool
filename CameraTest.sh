#!/bin/bash

echo camera.sh

echo -en "\\033[33m\\033[1m camera function test \\033[0m\n"
logFilePath="/tools/log"

# camera function test 
echo "Camera test"
#打开摄像头画面
./camera_test
if [ $? -eq 0 ]; then
   echo -e "\e[1;32m Camera PASS \e[0m";
   else
   echo -e "\e[1;31m Camera test Fail \e[0m"&exit 1;
    fi

echo $(date) "摄像头功能測試start"

