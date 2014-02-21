#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: config_example.py
# Date: Fri Feb 21 12:21:57 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from os import path

config = {'onpassword': '/haha',
          'offpassword': '/hehe',
          'temp_exe_path': path.join(path.abspath(__file__), 'temp')}
