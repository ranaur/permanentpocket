import argparse
import builtins
import pocket
import utils
import yaml
import json
import os

from .savers import savers

def method(args):
    if not os.path.isdir(args.output_dir):
        print("Making output dir %s" % args.output_dir)
        os.makedirs(args.output_dir)

    file_name = args.input_file
    if os.path.split(file_name)[0] == '': # no directory on pathname
        if os.path.isfile(os.path.join(args.output_dir, file_name)):
            file_name = os.path.join(args.output_dir, file_name)

    data = open(file_name, "r").read()
    if args.input_format == "yaml":
        data_tree = yaml.load(data)
    elif args.input_format ==  "json":
        data_tree = json.loads(data)
    else:
        raise ArgumentError

    articles = data_tree["list"]
    for article_id in articles:
        article = articles[article_id]
        if article["status"] != "2": # ignore deleted
            savers[args.save_format](args, article)

local_parser = builtins.command_parser.add_parser("download", help="download articles")
local_parser.add_argument("--input-file",
                          default="articles.yaml",
                          nargs="?",
                          help="sets the input file")

local_parser.add_argument("--input-format",
                          default="yaml",
                          nargs="?",
                          choices=['json', 'yaml'],
                          help="Format of the input file")

local_parser.add_argument("--output-dir",
                          nargs="?",
                          default="./articles",
                          help="sets the output directory")

local_parser.add_argument("--save-format",
                          nargs="?",
                          choices=savers.keys(),
                          default="pdf",
                          help="set the format of the output")
local_parser.set_defaults(funcCommand=method)

