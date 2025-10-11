# syntax=docker/dockerfile:1
FROM ubuntu:24.04

SHELL ["/bin/bash", "-c"]

WORKDIR /root
COPY *.py Api/

RUN apt-get update && apt-get install openjdk-21-jdk wget unzip python3 python3-venv python3-pip -y
# RUN python3 -m venv && source .venv/bin/activate && pip install -U pip 'fastapi[standard]' pyjwt
RUN mkdir -p Android/Sdk/cmdline-tools/latest
RUN wget -O cmd.zip "https://dl.google.com/android/repository/commandlinetools-linux-13114758_latest.zip" && unzip cmd.zip && mv cmdline-tools/* Android/Sdk/cmdline-tools/latest/ && rm -rf cmdline-tools
RUN echo "export ANDROID_HOME=\$HOME/Android/Sdk" >> .bashrc
RUN echo "export PATH=\$PATH:\$ANDROID_HOME/cmdline-tools/latest/bin" >> .bashrc

EXPOSE 8000

# CMD ["/bin/bash", "/root/run.sh"]
