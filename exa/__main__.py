#! /usr/bin/env python
import argparse



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


def notebook():
    '''exa notebook application'''
    pass


def workflow():
    '''exa high performance computing'''
    pass


if __name__ == '__main__':
    main()
