class Action(object):
    @staticmethod
    def setup_parser(parser):
        subparsers = parser.add_subparsers(title='actions')
        for cls in Action.__subclasses__():
            subparser = subparsers.add_parser(cls.name, help=cls.description, aliases=cls.aliases)
            subparser.set_defaults(action=cls.execute)
            for name, args in cls.arguments.items():
                subparser.add_argument(name, **args)
