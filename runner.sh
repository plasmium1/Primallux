#!/usr/bin/env bash
/opt/virtualenvs/python3/bin/python3 -m pip install --upgrade pip
export PYTHONHASHSEED="$hashNumber"
python3 main.py