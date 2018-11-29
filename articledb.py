import json
import yaml
import re

class ArticleDB():
    def __init__(self, args):
        self._data = None
        self._input_format = args["input_format"] if "input_format" in args else "json"
        if "file" in args:
            self.load(args["file"], self._input_format)

    def load(self, file, input_format = "json"):
        self._file = file

        with open(self._file, "r").read() as data:
            if input_format == "yaml":
                self._data = yaml.load(data)
            elif input_format == "json":
                self._data = json.loads(data)
            else:
                raise ArgumentError

    def get_every_articles(self):
        return list(self._data["list"].values())

    def get_articles(self, filters = {}):
        re_filters = {}
        for key, expression in filters:
            re_filters = re.compile(expression)

        for article in self._data["list"].values():
            for key in re_filters.keys():
                if re_filters[key].match(article[key]):
                    yield article


