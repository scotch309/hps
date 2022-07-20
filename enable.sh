#!/bin/bash

EXPECT='パスワード:'
PSWD='xxxx'
TIMEOUT=30

function reset {
	bluetoothctl power off
	sleep 2
	bluetoothctl power on
	sleep 2
}
function expectCmd {
	echo $1
	expect -c "
		spawn sudo $1
		set timeout $TIMEOUT
		expect $EXPECT
		send $PSWD\n
		interact
	"
}
function checkStatus {
	expectCmd 'hciconfig hci0 sspmode'
	expectCmd 'hcitool cmd 0x03 0x0009'
}


if [ $# -eq 0 ]; then
	# 引数なし
	:
elif [ $1 = "on" ]; then
	# 引数 on
	reset
	expectCmd 'hcitool cmd 0x03 0x0003'
	expectCmd 'hcitool cmd 0x03 0x000a 01'
elif [ $1 = "off" ]; then
	# 引数 off
	reset
fi
checkStatus