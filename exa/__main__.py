#! /usr/bin/env python
'''
exa Web Application
=====================
This is the starter for exa's standalone web application.
'''
import argparse
import webbrowser
import threading
from exa.web import serve


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
        default=8080
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
    The main entry point for exa's web application.
    '''
    args = get_args()
    port = args.port
    browser = args.browser
    link = 'http://localhost:{port}'.format(port=port)
    threading.Timer(0.5, lambda: webbrowser.get(browser).open(link)).start()
    serve(port=port)


if __name__ == "__main__":
    main()
