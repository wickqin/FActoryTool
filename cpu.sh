#! /bin/bash

echo "Check CPU"
# 读出CPU型号参数
TARGET_CPU="Hygon C86-3G"

# 直接从 /proc/cpuinfo 中检查 CPU 型号
if grep -q "$TARGET_CPU" /proc/cpuinfo; then
    echo -e "\e[1;32m Check CPU PASS \e[0m"
else
    echo -e "\e[1;31m Check CPU Fail \e[0m"
    exit 1
fi