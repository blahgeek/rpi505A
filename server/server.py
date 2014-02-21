#!/usr/bin/env python2
# -*- coding=UTF-8 -*-
# Created at Mar 31 19:07 by BlahGeek@Gmail.com

import web
import subprocess
from subprocess import call, check_output, Popen
from config import config
import os
from os import path
from base64 import b64decode
from tempfile import NamedTemporaryFile

urls = (
        '/', 'Index',
        config['onpassword'], 'TurnOn',
        config['offpassword'], 'TurnOff',
        '/lightstatus', 'LightStatus',
        '/test', 'Test',
        '/env', 'Env',
        '/speak', 'Speak',
        '/play', 'Play',
        )

INDEX_HTML = open(path.join(path.dirname(path.abspath(__file__)), 'static/index.html')).read()
INDEX_HTML = INDEX_HTML.replace('{{onpassword}}', config['onpassword'])
INDEX_HTML = INDEX_HTML.replace('{{offpassword}}', config['offpassword'])


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
        if all([ord(k) < 128 for k in i.content]):
            call(['espeak', i.content])
        else:
            call(['espeak', '-v', 'zh', i.content])
        return 'ok'

class Play(object):
    def POST(self):
        data = web.data()
        music = b64decode(data)
        fname = '/tmp/music'
        with open(fname, 'wb') as f:
            f.write(music)
        Popen(['mplayer', fname, '-noconsolecontrols'])
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
    try:
        call('gpio -g mode 4 out'.split(' '))
    except OSError:
        print 'error executing gpio'
    app = web.application(urls, globals())
    app.run()
