from .base import Action
from xml.etree import ElementTree
import requests
import sys

class Info(Action):
    name = 'info'
    aliases = []
    description = 'Get information about a Roku device'
    arguments = {
        'ip': {
            'help': 'IP address of Roku device',
        },
    }

    @staticmethod
    def execute(args):
        try:
            resp = requests.get('http://{}:8060/query/device-info'.format(args.ip.strip()))
        except requests.exceptions.ConnectionError as ex:
            print(str(ex), file=sys.stderr)
            return

        tree = ElementTree.fromstring(resp.text)
        fields_and_values = ((el.tag, el.text) for el in tree)
        print('\n'.join('{}: {}'.format(field, value) for field, value in fields_and_values))
