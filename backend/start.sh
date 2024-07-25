#! /bin/bash
DIR_PATH=$(cd "$(dirname "$0")"; pwd)

while true;
do
   python ${DIR_PATH}/src/monitor.py
done