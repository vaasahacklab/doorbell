#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging, logging.config
logging.config.fileConfig("logging.ini")

from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import sys
import json
import simpleaudio

__all__ = ["Doorbell"]

log = logging.getLogger("Doorbell")

# Load config from file
log.debug("Loading config file")
try:
    with open(os.path.join(sys.path[0], "config.json"), "r") as f:
        config = json.load(f)
    f.close()
except ValueError as e:
    log.critical("config.json is malformed, got error:\n\t" + str(e))
    f.close()
except Exception as e:
    log.critical("Failed loading config file, got error:\n\t" + str(e))
    quit()

class Doorbell(BaseHTTPRequestHandler):
    def do_PUT(self):
        try: 
            content_len = int(self.headers.get('Content-Length'))
            data = json.loads(self.rfile.read(content_len))
            if data['dooropened']:
                log.info("Got request for successful door open")
                self.send_response(204)
                self.end_headers()
                self.playAudio(config['dooropen'])
            elif data['dooropened'] is False:
                log.info("Got request for doorbell")
                self.send_response(204)
                self.end_headers()
                self.playAudio(config['doorbell'])
        except Exception as e:
            log.error("Got invalid request, propably incorrect parameter in request, needs JSON \"dooropened\" true/false")
            self.send_response(400)
            self.end_headers()

    def playAudio(self, file):
        if file is None:
            log.info("Audio disabled for request, skipping play")
        if file is not None:
            log.info("Playing audio for request")
            wave_obj = simpleaudio.WaveObject.from_wave_file(file)
            play_obj = wave_obj.play()
            play_obj.wait_done()

if __name__ == '__main__':
    if config['dooropen'] is None and config['doorbell'] is None:
        log.critical("Both dooropen and doorbell setting is disabled, quitting.")
        quit()

    if not config['dooropen'] is None:
        if not os.path.exists(os.path.join(config['dooropen'])):
            log.critical("Door open enabled and sound file for door open doesn't exists")
            quit()
    if not config['doorbell'] is None:
        if not os.path.exists(os.path.join(config['doorbell'])):
            log.critical("Doorbell sound enabled and sound file for doorbell doesn't exists")
            quit()

    httpd = HTTPServer((config['host'], config['port']), Doorbell)
    log.info("Starting")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    log.info("Stopped")
