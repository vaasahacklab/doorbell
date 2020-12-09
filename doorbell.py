#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import sys
import json
import simpleaudio

# Create logs -folder if not exist
if not os.path.isdir(os.path.join(sys.path[0], "logs")):
    os.mkdir(os.path.join(sys.path[0], "logs"), 0o755)

import logging, logging.config
logging.config.fileConfig("logging.ini")

log = logging.getLogger("Doorbell")

__all__ = ["Doorbell"]

# Load config from file
log.debug("Loading config file")
try:
    with open(os.path.join(sys.path[0], "config.json"), "r") as f:
        config = json.load(f)
    f.close()
except ValueError as e:
    log.critical("config.json is malformed, got error:\n\t" + str(e))
    f.close()
    raise e
except Exception as e:
    log.critical("Failed loading config file, got error:\n\t" + str(e))
    raise e

if not config['sounds']:
    error = "Need at least one resultcode:soundfile key-value -pair in config under \"sounds\"!"
    log.critical(error)
    raise ValueError(error)

filesnotfound = []
for file in config['sounds']:
    if not os.path.isfile(os.fsencode(os.path.join("sounds", str(config['sounds'][file])))):
        filesnotfound.append(file)
for file in filesnotfound:
    log.warning("File \"" + str(config['sounds'][file]) + "\" for result-value \"" + file + "\" not found")
    del config['sounds'][file]
del filesnotfound

class Doorbell(BaseHTTPRequestHandler):
    def do_PUT(self):
        try:
            content_len = int(self.headers.get('Content-Length'))
            data = json.loads(self.rfile.read(content_len))
            if data['request']:
                log.info("Got request: " + str(data['request']))
                try:
                    self.playAudio(config['sounds'][str(data['request'])])
                    self.send_response(204)
                except KeyError:
                    try:
                        if config['sounds']['*']:
                            log.info("Using wildcard soundfile")
                            self.playAudio(config['sounds']['*'])
                            self.send_response(204)
                    except KeyError:
                        log.error("Soundfile configuration for \"" + str(data) + "\" does not exist!")
                        self.send_error(415, message="Soundfile configuration for \"" + str(data) + "\" does not exist!")
                except Exception as e:
                    log.error("Unkown error: " + str(e))
                    self.send_error(415, message="Unkown error: " + str(e))
        except KeyError as e:
            print(str(e))
            log.error("Request did not contain \"request\" variable, got:\n\t" + (str(data)))
            self.send_error(400, message="Request did not contain \"request\" variable, got: \"" + (str(data)) + "\"")
        except Exception as e:
            log.error("Unkown error: " + str(e))
            self.send_error(500, message=str(e))
        finally:
            self.end_headers()

    def playAudio(self, file):
        log.info("Playing audiofile \"" + str(file) + "\"")
        wave_obj = simpleaudio.WaveObject.from_wave_file(os.path.join("sounds", file))
        play_obj = wave_obj.play()
        #play_obj.wait_done()

# If is run as standalone program
if __name__ == "__main__":
    __name__ = "Doorbell"

    log.info("Starting")
    httpd = HTTPServer((config['host'], config['port']), Doorbell)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        log.debug("Caught Keyboard interrupt")
    log.info("Stopping")
    httpd.shutdown()
