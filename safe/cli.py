from __future__ import print_function

__author__ = 'sumeet'

import requests
import json
import subprocess


class ErrorSaving(Exception):
    pass


class ErrorQuerying(Exception):
    pass


class NotFound(Exception):
    pass


class Cli:
    def __init__(self, base_url):
        self.base_url = base_url

    def save(self, app, user, password):
        r = requests.post(self.base_url + '/save', json={app: {user: password}})
        if r.status_code != 200:
            raise ErrorSaving

    def get(self, app):
        r = requests.get(self.base_url + '/get', params={'app': app})
        if r.status_code != 200:
            if r.status_code == 404:
                raise NotFound
            else:
                raise ErrorQuerying

        data = json.loads(r.content)

        print("app: {app} user: {user} password: {password}".format(app=app,
                                                                    user=data.keys()[0],
                                                                    password=data.values()[0]))

        self.write_to_clipboard(data.values()[0])

    @staticmethod
    def write_to_clipboard(output):
        process = subprocess.Popen(
            'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
        process.communicate(output.encode())

