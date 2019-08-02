from .base import Action
import requests
import sys
import time

class Keypress(Action):
    name = 'keypress'
    aliases = ['key']
    description = 'Press a remote control key on a Roku device'
    arguments = {
        'ip': {
            'help': 'IP address of Roku device',
        },
        '-k': {
            'help': 'Remote control key to press',
            'nargs': '+',
            'dest': 'keys',
            'required': True,
        },
        '-p': {
            'help': 'Period to wait between key presses (default: 1 sec)',
            'dest': 'period',
            'type': float,
            'default': 1,
        },
    }

    @staticmethod
    def execute(args):
        period = max(0, args.period)

        for key in args.keys:
            try:
                resp = requests.post('http://{}:8060/keypress/{}'.format(args.ip.strip(), key.strip()))
            except requests.exceptions.ConnectionError as ex:
                print(str(ex), file=sys.stderr)
                return

            if len(args.keys) > 1:
                time.sleep(period)
