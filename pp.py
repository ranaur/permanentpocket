import argparse
import builtins

parser = argparse.ArgumentParser(description='command line metadata editor')
builtins.command_parser = parser.add_subparsers()

import commands
if __name__ == '__main__':
    args = parser.parse_args()

    import inspect
    if (hasattr(args, 'funcCommand') and inspect.isfunction(args.funcCommand)):
        args.funcCommand(args)
    else:
        parser.print_help()

