#! /bin/bash
echo ""
echo -----------------------
echo   Scan SN and Check
echo -----------------------
#扫描SN
read -p "ScanSN:" ScanSN
SN=$(echo "$ScanSN" | tr '[:lower:]' '[:upper:]')
if test ${#SN} != 15;then
echo -e "\e[1;31m ScanSN Fail \e[0m"
exit 1
fi


#读取SN并格式化
dmidecode -t 2 |grep 'Serial Number' >readSN.txt
#sed -i "s/://g" readSN.txt

#核对SN
if grep -i -q "$SN" readSN.txt; then echo -e "\e[1;32m Check SN PASS \e[0m";else echo -e "\e[1;31m Check SN Fail \e[0m"&exit 1;fi
