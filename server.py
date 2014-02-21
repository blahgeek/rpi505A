#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# Created at Mar 31 19:07 by BlahGeek@Gmail.com

import web
import subprocess
import os
from os import path
from subprocess import call, check_output
from config import config

urls = (
        config['onpassword'], 'TurnOn',
        config['offpassword'], 'TurnOff',
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
                return check_output(['sudo',
                                     os.path.join(os.path.abspath(__file__),
                                                  'temp')])
            except subprocess.CalledProcessError:
                continue
        return 'error'


class TurnOn:
    def GET(self):
        call('gpio -g write 4 1'.split(' '))
        return 'ok'


class TurnOff:
    def GET(self):
        call('gpio -g write 4 0'.split(' '))
        return 'ok'


if __name__ == '__main__':
    call('gpio -g mode 4 out'.split(' '))
    app = web.application(urls, globals())
    app.run()
