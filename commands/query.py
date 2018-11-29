import argparse
import __builtin__
builtin = __builtin__
import pocket
import utils
import yaml
import json
import os

def method(args):
    access_token = utils.get_access_token(args.consumer_key, auth_file=args.auth_file)
    pocket_instance = pocket.Pocket(args.consumer_key, access_token)

    # perfoms all these actions in one request
    # NOTE: Each individual method returns the instance itself. The response
    # dictionary is not returned till commit is called on the instance.
    response, headers = pocket_instance.get(
        state=args.state, favorite=args.favorite, tag=args.tag,
        contentType=args.content_type, sort=args.sort,
        detailType=args.detail_type, search=args.search,
        domain=args.domain, since=args.since,
        count=args.count, offset=args.offset
    )

    if args.header_output is not None:
        header_file = args.header_output
        if os.path.splitext(header_file)[1] == '':
            header_file = header_file + "." + args.header_format
        with open(args.header_file, 'w+') as fp:
            if args.header_format == "yaml":
                fp.write(yaml.dump(headers))
            elif args.header_format == "json":
                fp.write(json.dumps([headers]))
            else:
                raise ArgumentError

    headers_dict = {}
    for key in headers:
        headers_dict[key] = headers[key]
    response["headers"] = headers_dict

    args_dict = {}
    for arg in vars(args):
        if type(getattr(args, arg)) in [str, int]:
            args_dict[arg] = getattr(args, arg)
    response["args"] = args_dict

    if args.response_format == "yaml":
        response_output = yaml.dump(response)
    elif args.response_format == "json":
        response_output = json.dumps([response])
    else:
        raise ArgumentError

    if args.response_output is None:
        print(response_output)
    else:
        response_file = args.response_output
        if os.path.splitext(response_file)[1] == '':
            response_file = response_file + "." + args.response_format

        with open(response_file, 'w+') as fp:
            fp.write(response_output)


local_parser = builtins.command_parser.add_parser("query", help="queries your pocket entries from getpocket server")
local_parser.add_argument("--consumer-key",
                          default=utils.CONSUMER_KEY,
                          nargs="?",
                          help="Consumer key used for the application")
local_parser.add_argument("--access-key",
                          nargs="?",
                          help="Access key (default read from --access-file or try to authenticate)")

local_parser.add_argument("--auth-file",
                          default="~/.pocketauth",
                          nargs="?",
                          help="File with auth keys")

local_parser.add_argument("--header-output",
                          nargs="?",
                          help="Filename to store headers")
local_parser.add_argument("--header-format",
                          default="yaml",
                          nargs="?",
                          choices=['json', 'yaml'],
                          help="Format to write headers")

local_parser.add_argument("--response-output",
                          nargs="?",
                          help="Filename to store response (default stdout)")
local_parser.add_argument("--response-format",
                          default="yaml",
                          nargs="?",
                          choices=['json', 'yaml'],
                          help="Format to write response")

local_parser.add_argument("--state",
                          choices=['unread', 'archive', 'all'],
                          nargs="?",
                          help="query itens from this state")
local_parser.add_argument("--favorite",
                          choices=['0', '1'],
                          nargs="?",
                          help="query only favorites (1), only unfavorites (0)")
local_parser.add_argument("--tag",
                          nargs="?",
                          help="query only specific tags (or __untagged__ for untagged itens)")
local_parser.add_argument("--content-type",
                          choices=['article', 'video', 'image'],
                          nargs="?",
                          help="query only thist content type")
local_parser.add_argument("--sort",
                          choices=['newest', 'oldest', 'title', 'site'],
                          nargs="?",
                          help="sort result by")
local_parser.add_argument("--detail-type",
                          choices=['simple', 'complete'],
                          nargs="?",
                          help="query basic info or complete info")
local_parser.add_argument("--search",
                          nargs="?",
                          help="Only return items whose title or url contain the search string")
local_parser.add_argument("--domain",
                          nargs="?",
                          help="Only return items from a particular domain ")
local_parser.add_argument("--since",
                          nargs="?",
                          help="return results newer than timestamp")
local_parser.add_argument("--count",
                          nargs="?",
                          help="Only return count number of items")
local_parser.add_argument("--offset",
                          nargs="?",
                          help="Used only with count; start returning from offset position of results")
local_parser.set_defaults(funcCommand=method)

