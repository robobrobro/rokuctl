from .base import Action
import re
import socket
import sys

DISCO_MSG = """M-SEARCH * HTTP/1.1
Host: 239.255.255.250:1900
Man: "ssdp:discover"
ST: roku:ecp

"""

class Discover(Action):
    name = 'discover'
    aliases = ['disco']
    description = 'Discover Roku devices'
    arguments = {
        '-c': {
            'dest': 'count',
            'metavar': 'COUNT',
            'type': int,
            'help': 'Number of expected devices',
        },
    }

    @staticmethod
    def execute(args):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('0.0.0.0', 1900))

        sock.sendto(DISCO_MSG.encode('ascii'), ('239.255.255.250', 1900))
        count = 0

        try:
            while args.count is None or count < args.count:
                data, addr = sock.recvfrom(4096)
                msg = data.decode('utf-8')

                if not msg.startswith('HTTP/1.1 200 OK'):
                    print(msg.split('\r')[0], file=sys.stderr)
                    continue

                count += 1

                match = re.search('^USN:\s+uuid:roku:ecp:(?P<uuid>[A-Za-z0-9]+)\r$', msg, flags=re.M | re.S | re.I)
                uuid = match.group('uuid')
                match = re.search('^Server:\s+(?P<server>[^\r]+)\r$', msg, flags=re.M | re.S | re.I)
                server = match.group('server')
                match = re.search('^LOCATION:\s+(?P<location>[^\r]+)\r$', msg, flags=re.M | re.S | re.I)
                location = match.group('location')
                match = re.search('MAC=(?P<mac>([A-Fa-f0-9]{2}:){5}[A-Fa-f0-9]{2})', msg, flags=re.M | re.S | re.I)
                mac = match.group('mac')

                print('UUID: {}'.format(uuid))
                print('Server: {}'.format(server))
                print('Location: {}'.format(location))
                print('MAC: {}'.format(mac))
                print()

        except KeyboardInterrupt:
            pass
