#!/usr/bin/env python3
import os

from xmasvideo.app import app

if __name__ == '__main__':
    # Set dev settings
    app.debug = True
    app.secret_key = os.urandom(32)
    app.run()
