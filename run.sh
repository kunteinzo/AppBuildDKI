#!/bin/bash

if [ $PWD != "$HOME/Api" ];then cd $HOME/Api;fi

source $HOME/.venv/bin/activate
fastapi dev --host 0.0.0.0
