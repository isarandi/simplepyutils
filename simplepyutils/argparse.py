import argparse

FLAGS = argparse.Namespace()
logger = logging.getLogger('')


class ParseFromFileAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        with values as f:
            lines = f.read().splitlines()
            args = [f'--{line}' for line in lines if line and not line.startswith('#')]
            parser.parse_args(args, namespace)


class HyphenToUnderscoreAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values.replace('-', '_'))


class BoolAction(argparse.Action):
    def __init__(self, option_strings, dest, default=False, required=False, help=None):
        positive_opts = option_strings
        if not all(opt.startswith('--') for opt in positive_opts):
            raise ValueError('Boolean arguments must be prefixed with --')
        if any(opt.startswith('--no-') for opt in positive_opts):
            raise ValueError(
                'Boolean arguments cannot start with --no-, the --no- version will be '
                'auto-generated')

        negative_opts = ['--no-' + opt[2:] for opt in positive_opts]
        opts = [*positive_opts, *negative_opts]
        super().__init__(
            opts, dest, nargs=0, const=None, default=default, required=required, help=help)

    def __call__(self, parser, namespace, values, option_string=None):
        if option_string.startswith('--no-'):
            setattr(namespace, self.dest, False)
        else:
            setattr(namespace, self.dest, True)


def initialize(parser, args=None):
    parser.add_argument('--loglevel', type=str, default='error')
    parser.parse_args(args=args, namespace=FLAGS)
    loglevel = dict(error=40, warning=30, info=20, debug=10)[FLAGS.loglevel]
    simple_formatter = logging.Formatter('{asctime}-{levelname:^1.1} -- {message}', style='{')

    if sys.stdout.isatty():
        # Make sure that the log messages appear above the tqdm progess bars
        import tqdm
        class TQDMFile:
            def write(self, x):
                if len(x.rstrip()) > 0:
                    tqdm.tqdm.write(x, file=sys.stdout)

        out_stream = TQDMFile()
    else:
        out_stream = sys.stdout

    print_handler = logging.StreamHandler(out_stream)
    print_handler.setLevel(loglevel)
    print_handler.setFormatter(simple_formatter)
    logger.setLevel(loglevel)
    for handler in logger.handlers:
        logger.removeHandler(handler)
    logger.addHandler(print_handler)
