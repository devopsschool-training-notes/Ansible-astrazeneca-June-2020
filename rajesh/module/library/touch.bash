#!/bin/bash
# import variables from ansible
source $1
state=${state:-present}
if [[ $state == "present" ]]; then
	if [ ! -e $file ]; then
		touch $file
		echo { \"changed\": true }
		exit 0
	else
		echo { \"changed\": false }
		exit 0
	fi
fi

if [[ $state == "absent" ]]; then
	if [ -e $file ]; then
		rm $file
		echo { \"changed\": true }
		exit 0
	else
		echo { \"changed\": false}
		exit 0
	fi
fi
