# Doorbell #
Doorbell script to play sound when Hacklab "doorbell" is triggered

## Installation

System prerequirents:
libasound2-dev
python3-dev
python3-pip

For Debian-based systems run: `< requirements.apt xargs sudo apt install -y`

Setup venv:
`python3 -m venv venv`

Activate venv:
`source ./venv/bin/activate`

Install python modules
`pip install -r requirements.txt`

## Config

Example is provided in `config.json.example`, copy it to `config.json` and modify for your enviroment.

Configuration parameters and their meaning:

`"host": "localhost"`, hostname or IP to listen on, string, required  
`"port": 8088`, port to listen on, integer, required

Key-value string pairs inside `"sounds"`-section has request to filename mappings; `"frontdoor": "knockknock.wav"` for example would play `knockknock.wav` when dindong request comes for token `frontdoor`.

Special wildcard key `"*"` can be set to play certain soundfile for any incoming token: `"*": "catchall.wav"`

At least one key-value pair is required.

## Usage

Script waits incoming JSON-requests on configured port. it expects `{'request': 'frontdoor'}` string key-value (standard JSON), where `frontdoor` is the token to play doorbell for. If soundfile mapping exist for `frontdoor` in config, mapped soundfile will play, otherwise wildcard soundfile will play if configured. Failing both returns error to requester.