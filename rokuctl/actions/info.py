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
        fields_and_values = [(el.tag, el.text) for el in tree]
        print('\n'.join('{}: {}'.format(field, value) for field, value in fields_and_values))

        try:
            resp = requests.get('http://{}:8060/query/active-app'.format(args.ip.strip()))
        except requests.exceptions.ConnectionError as ex:
            print(str(ex), file=sys.stderr)
            return

        tree = ElementTree.fromstring(resp.text)
        app = tree.find('app')
        print('app-name: {}'.format(app.text))
        print('\n'.join('app-{}: {}'.format(field, value) for field, value in app.attrib.items()))

        try:
            resp = requests.get('http://{}:8060/query/apps'.format(args.ip.strip()))
        except requests.exceptions.ConnectionError as ex:
            print(str(ex), file=sys.stderr)
            return

        tree = ElementTree.fromstring(resp.text)
        apps = tree.findall('app')
        for idx, app in enumerate(apps):
            print('app{}-name: {}'.format(idx, app.text))
            print('\n'.join('app{}-{}: {}'.format(idx, field, value) for field, value in app.attrib.items()))

        is_tv = any(str(v).lower() == 'true' for k, v in fields_and_values if k.lower() == 'is-tv')
        if not is_tv:
            return

        try:
            resp = requests.get('http://{}:8060/query/tv-active-channel'.format(args.ip.strip()))
        except requests.exceptions.ConnectionError as ex:
            print(str(ex), file=sys.stderr)
            return

        tree = ElementTree.fromstring(resp.text)
        fields_and_values = ((el.tag, el.text) for el in tree.find('channel'))
        print('\n'.join('channel-{}: {}'.format(field, value) for field, value in fields_and_values))

        try:
            resp = requests.get('http://{}:8060/query/tv-channels'.format(args.ip.strip()))
        except requests.exceptions.ConnectionError as ex:
            print(str(ex), file=sys.stderr)
            return

        tree = ElementTree.fromstring(resp.text)
        fields_and_values = ((idx, el.tag, el.text) for idx, ch in enumerate(tree.findall('channel')) for el in ch)
        print('\n'.join('channel{}-{}: {}'.format(idx, field, value) for idx, field, value in fields_and_values))

        
