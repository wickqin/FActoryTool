#! /bin/bash
echo ""
echo -----------------------
echo   Scan SN and Write
echo -----------------------
#扫描SN
read -p "ScanSN:" ScanSN
SN=$(echo "$ScanSN" | tr '[:lower:]' '[:upper:]')
if test ${#SN} != 15;then
echo -e "\e[1;31m ScanSN Fail \e[0m"
exit 1
fi

