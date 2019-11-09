#!/bin/sh

if [ ! -z $PORT ]; then
    python main.py --port ${PORT}
else
    python main.py
fi