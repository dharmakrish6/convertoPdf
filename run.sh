#!/bin/sh
echo "Installing if any new dependencies"
pip3 install -r requirements.txt

echo "Starting the server "

flask run --host=0.0.0.0 --port=8080