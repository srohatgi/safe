__author__ = 'sumeet'

import cherrypy

# file management
import json
import os
import dropbox
from crypto_manager import CryptoManager


class InvalidFilePath(Exception):
    def __init__(self):
        pass


class SafeBox(object):
    def __init__(self, drop_box_key, password):
        cherrypy.log("drop_box_key: {drop_box_key}, password: {password}"
                     .format(drop_box_key=drop_box_key, password=password))

        self.dbx = dropbox.Dropbox(drop_box_key)
        self.file_path = os.path.join('/tmp', 'safe.json')
        self.crypto = CryptoManager(password)

    def _enc(self):
        return self.file_path + '.enc'

    @staticmethod
    def remote():
        return '/world-travels/hello-baby.txt'

    def read_data(self):
        self.sync_data()
        return self.read_enc_file()

    def patch_data(self, sites):
        self.delete_enc_file()
        data = self.read_data()

        for site in sites.keys():
            data[site] = sites[site]

        self.create_enc_file(data)
        self.sync_data(write_op=True)

    def sync_data(self, write_op=False):
        if not os.path.exists(self._enc()):
            try:
                self.dbx.files_download_to_file(self._enc(), self.remote())
            except dropbox.exceptions.DropboxException as e:
                cherrypy.log(str(e))
                if type(e.error) is dropbox.files.DownloadError and e.error.get_path().is_not_found:
                    cherrypy.log('*** creating ' + self.remote())
                    self.create_enc_file({})
                else:
                    raise e
        elif write_op:
            with open(self._enc()) as enc_file:
                self.dbx.files_upload(enc_file, self.remote(), mode=dropbox.files.WriteMode('overwrite', None))

    def read_enc_file(self):
        data = {}
        if os.path.exists(self._enc()):
            self.crypto.decrypt_file(self._enc())
            with open(self.file_path, 'r') as data_file:
                data = json.load(data_file)
            os.unlink(self.file_path)

        return data

    def delete_enc_file(self):
        if os.path.exists(self._enc()):
            os.unlink(self._enc())

    def create_enc_file(self, data):
        with open(self.file_path, 'w') as safe_file:
            safe_file.write(json.dumps(data))

        self.crypto.encrypt_file(self.file_path)
        os.unlink(self.file_path)

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def save(self):
        sites = cherrypy.request.json
        cherrypy.log("sites: {sites}".format(sites=sites))
        self.patch_data(sites)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get(self, app):
        data = self.read_data()
        if app in data:
            return data[app]
        else:
            raise cherrypy.HTTPError(404, 'site not found')
