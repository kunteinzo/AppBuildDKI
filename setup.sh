#!/bin/bash

if [ $PWD != $HOME ];then cd $HOME;fi

echo "export ANDROID_HOME=\$HOME/Android/Sdk" >> .bashrc
echo "export PATH=\$PATH:\$ANDROID_HOME/cmdline-tools/latest/bin" >> .bashrc

sdkmanager --licenses

cd Api
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip 'fastapi[standard]' pyjwt
