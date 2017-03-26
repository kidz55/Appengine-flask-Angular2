#!/usr/bin/env python

"""Google App Engine uses this file to run your Flask application."""

import os
from wsgiref.handlers import CGIHandler
from utils import adjust_sys_path

adjust_sys_path()

from application import app

def main():
    CGIHandler().run(app)

if __name__ == '__main__':
    main()