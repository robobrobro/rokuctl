#!/usr/bin/env python3

from argparse import ArgumentParser
from .actions import Action
import sys

def parse_args(argv):
    parser = ArgumentParser(prog='rokuctl', description='Control Roku devices')
    parser.set_defaults(action=lambda args: parser.print_help())
    Action.setup_parser(parser)
    return parser.parse_args(argv)

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    args = parse_args(argv)
    args.action(args)

if __name__ == '__main__':
    main()
