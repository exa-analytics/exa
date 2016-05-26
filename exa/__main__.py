#! /usr/bin/env python
'''
exa Web Application
=====================
This module starts up the web GUI. Rather than having a standalone graphical
client, exa's GUI is presented as a web client.
'''
import argparse
import webbrowser
import threading
import sys
import os
sys.path.insert(0, os.path.abspath('./'))
from exa._web import serve


def get_args():
    '''
    Command line argument parsing and usage documentation.
    '''
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument(
        '-p',
        '--port',
        type=str,
        help='port (default 5000)',
        required=False,
        default=5000
    )
    parser.add_argument(
        '-b',
        '--browser',
        type=str,
        help='browser (system default)',
        required=False,
        default=None
    )
    return parser.parse_args()


def main():
    '''
    Parse command line arguments and start the (web-based) application.
    '''
    args = get_args()
    port = args.port
    browser = args.browser
    link = 'http://localhost:{port}'.format(port=port)
    threading.Timer(0.5, lambda: webbrowser.get(browser).open(link)).start()
    serve(port=port)
