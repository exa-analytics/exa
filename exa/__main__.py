#! /usr/bin/env python
import os
import sys
import argparse
import webbrowser
import threading

sys.path.insert(0, os.path.abspath('./'))
from exa._app import serve


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
    parser.add_argument(
        '-w',
        '--workflow',
        type=str,
        help='high performance computing workflow',
        required=False,
        default=None
    )
    parser.add_argument(
        '-s',
        '--hosts',
        type=str,
        help='hostnames of compute nodes (for workflows)',
        required=False,
        default=None
    )
    return parser.parse_args()


def main():
    '''
    Main application entry point.

    The exa application has two modes; one starts a dynamic web application
    for managing data, performing postprocessing
    '''
    args = get_args()
    workflow = args.workflow    # When using a workflow, don't spawn the GUI
    if workflow is None:
        port = args.port
        browser = args.browser
        link = 'http://localhost:{port}'.format(port=port)
        threading.Timer(0.5, lambda: webbrowser.get(browser).open(link)).start()
        serve(port=port)
    else:
        # Here we have exa do high performance computing on a cluster
        raise NotImplementedError()
        hostnames = args.hosts
        if hostnames is None:
            raise NameError('hostnames are not defined, please use the -s option.')


if __name__ == '__main__':
    main()
