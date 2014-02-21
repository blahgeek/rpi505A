#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# Created at Mar 31 19:07 by BlahGeek@Gmail.com

import web
import subprocess
from subprocess import call, check_output
from config import config
from os import path

urls = (
        '/', 'Index',
        config['onpassword'], 'TurnOn',
        config['offpassword'], 'TurnOff',
        '/lightstatus', 'LightStatus',
        '/test', 'Test',
        '/env', 'Env',
        '/speak', 'Speak',
        )

INDEX_HTML = open(path.join(path.abspath(__file__), 'static/index.html')).read()
INDEX_HTML = INDEX_HTML.replace('onpassword', config['onpassword'])
INDEX_HTML = INDEX_HTML.replace('offpassword', config['offpassword'])


class Index:
    def GET(self):
        return INDEX_HTML


class Test:
    def GET(self):
        return 'ok'


class Env:
    def GET(self):
        for i in xrange(3):
            try:
                return check_output(['sudo', config['temp_exe_path']])
            except subprocess.CalledProcessError:
                continue
        return 'error'


class Speak:
    def POST(self):
        i = web.input(content='')
        call(['espeak', i.content])
        return 'ok'


class TurnOn:
    def GET(self):
        call('gpio -g write 4 1'.split(' '))
        raise web.seeother('/lightstatus')


class TurnOff:
    def GET(self):
        call('gpio -g write 4 0'.split(' '))
        raise web.seeother('/lightstatus')


class LightStatus:
    def GET(self):
        return check_output('gpio -g read 4'.split(' '))


if __name__ == '__main__':
    call('gpio -g mode 4 out'.split(' '))
    app = web.application(urls, globals())
    app.run()
