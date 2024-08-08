#! /bin/bash
rm -f bluetooth.txt

echo "Check WIFI Device"
#读出型号
wifi=$(grep -qi "description: Wireless interface"| lshw -c network |wc -l)
 
if grep -q "hci0" bluetooth.txt; then echo -e "\e[1;32m Check WIFI PASS \e[0m"; else
    echo -e "\e[1;31m Check WIFI Fail \e[0m" &
    exit 1
fi
