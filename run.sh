#!/bin/bash

if [ $PWD != "$HOME/Api" ];then cd $HOME/Api;fi

/root/Android/Sdk/cmdline-tools/latest/bin/sdkmanager --licenses

source $HOME/.venv/bin/activate
fastapi dev --host 0.0.0.0
