#!/bin/bash

sudo apt update

sudo apt install python3 python3-pip -y

python3 --version
pip3 --version

pip3 install -r requirements.txt

pip3 list