__author__ = 'sumeet'

import sys
import cherrypy

# file management
import json
import os
from crypto_manager import CryptoManager


class InvalidFilePath(Exception):
    def __init__(self):
        pass


class SafeBox(object):
    def __init__(self, location, password):
        cherrypy.log("location: {location}, password: {password}".format(location=location, password=password))

        if not os.path.exists(location):
            raise InvalidFilePath

        self.filepath = os.path.join(location, 'safe.json')
        self.crypto = CryptoManager(password)

    def get_data(self):
        data = {}
        enc_filepath = self.filepath + '.enc'
        if not os.path.isfile(enc_filepath):
            return data

        self.crypto.decrypt_file(enc_filepath)

        with open(self.filepath, 'r') as data_file:
            data = json.load(data_file)

        os.unlink(self.filepath)
        return data

    def save_data(self, data):
        with open(self.filepath, 'w') as safe_file:
            safe_file.write(json.dumps(data))

        self.crypto.encrypt_file(self.filepath)
        os.unlink(self.filepath)

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def save(self):
        data = self.get_data()
        sites = cherrypy.request.json
        cherrypy.log("sites: {sites}".format(sites=sites))
        for site in sites.keys():
            data[site] = sites[site]

        self.save_data(data)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get(self, site):
        data = self.get_data()
        if site in data:
            return data[site]
        else:
            raise cherrypy.HTTPError(404, 'site not found')


def main(*args):
    conf = {
        '/': {
            'tools.sessions.on': True
        }
    }

    cherrypy.quickstart(SafeBox(*args), '/', conf)

if __name__ == '__main__':
    main(*sys.argv[1:])
