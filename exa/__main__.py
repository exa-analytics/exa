#! /usr/bin/env python
'''
exa web app
=============
This script starts the exa web application. Navigate to hostname:port
(default http://localhost:8080) in your browser to access exa.
'''
#import sys
import argparse
import webbrowser
import threading
from exa.app import serve


NOT_KWARGS = ['server', 'port', 'browser']
DESCRIPTION = '''=======================================
exa application
=======================================
Usage: exa'''


def get_args():
    '''
    Argument parsing
    '''
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('-s', '--server', type=str,
                        help='hostname (default localhost)', required=False,
                        default='localhost')
    parser.add_argument('-p', '--port', type=str, help='port (default 8080)',
                        required=False, default=8080)
    args = parser.parse_args()
    host = args.server
    port = args.port
    obj = vars(args)
    kwargs = {k: v for k, v in vars(args).items() if k not in NOT_KWARGS}
    browser = obj['browser'] if 'browser' in obj else None
    return host, port, kwargs, browser


def main(args=None):
    '''
    Entry point for the exa web application.
    '''
    # Get the arguments
    host, port, kwargs, browser = get_args()
    link = 'http://{host}:{port}'.format(host=host, port=port)
    threading.Timer(0.5, lambda: webbrowser.get(browser).open(link)).start()
    serve(host=host, port=port)


if __name__ == "__main__":
    main()
