#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# Created at Mar 31 19:07 by BlahGeek@Gmail.com

import web
import subprocess
from subprocess import call, check_output
from config import config

urls = (
        config['onpassword'], 'TurnOn',
        config['offpassword'], 'TurnOff',
        '/lightstatus', 'LightStatus',
        '/test', 'Test',
        '/env', 'Env',
        )


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
