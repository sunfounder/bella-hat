#!/bin/bash

set -e

pid=`ps -ef | grep 'uvicorn app:app' | grep 'python3' | grep -v grep | awk '{print $2}'`
if [[ -n $pid ]]
then
    kill -9 $pid
fi
