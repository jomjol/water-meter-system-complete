#!/bin/bash

myscript(){
    python3 ./wasseruhr.py
}

until myscript; do
    echo "'wasseruhr.py' crashed with exit code $?. Restarting..." >&2
    sleep 1
done