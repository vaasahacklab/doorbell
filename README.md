# doorbell #
Doorbell script to play sound when Hacklab "doorbell" is triggered

## Installation

System prerequirents:
libasound2-dev
python3-dev

For Debian-based systems run: `< requirements.apt xargs sudo apt install -y`

Setup venv:
`python3 -m venv venv`

Activate venv:
`source ./venv/bin/activate`

Install python modules
`pip install -r requirements.txt`

## Config

Config.json.example provides example config, copy it to config.json and modify for your enviroment.

Configuration parameters and their meaning:

`"host": "localhost"`, hostname or IP to listen on
`"port": 8088`, port to listen on
`"dooropen": null`, sound filename that plays when door is open
`"doorbell": "2.wav"`, sound filename that plays when doorbell is ringed

Either sound file setting can be set to `null` but not both together.
