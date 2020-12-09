# Doorbell #
Doorbell script to play sound when Hacklab "doorbell" is triggered

## Installation

For Debian-based systems:

Best practice is to run service as own system user, one can be created for example with:
`sudo useradd -c "Doorbell System" -d /opt/doorbell -G audio -m -r -s /bin/nologin -U doorbell`

Above creates system user named doorbell, home folder in /opt/doorbell, without login capabilies, and access to audio devices.

One can login locally to such user for setupping with:  
`sudo -Hu doorbell /bin/bash`

System prerequirements:
libasound2-dev
python3-dev
python3-pip

Run as admin user: `< requirements.apt xargs sudo apt install -y`

Run these as doorbell user:

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

### Systemd unit

doorbell.service.example is provided as an example systemd service unit file, it assumes setup done as per installation section, adjust for your modifications.
