from .base import Action
import requests
import sys

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
            'required': True,
            'dest': 'key',
        },
    }

    @staticmethod
    def execute(args):
        try:
            resp = requests.post('http://{}:8060/keypress/{}'.format(args.ip.strip(), args.key.strip()))
        except requests.exceptions.ConnectionError as ex:
            print(str(ex), file=sys.stderr)
            return

        print(resp.text)
