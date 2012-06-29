#!/bin/bash
VALUE="`snmpget -$1 -c $2 -OUvq $3 1.3.6.1.4.1.14988.1.1.1.2.1.6.$4 2>/dev/null`"
#echo "Version: "$1
#echo "Community: "$2
#echo "IP: "$3
#echo "MAC: "$4

if [[ $VALUE =~ ^[0-9]+$ ]]
then 
	echo 'SNMP Status OK|ssStatus=1'
else 
	echo 'SNMP Status OK|ssStatus=0' 
fi

