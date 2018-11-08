import os
import importlib
import builtins

here = os.path.dirname(__file__)

savers = {}
builtins.commands = []
for fn in os.listdir(here):
    if fn.endswith(".py") and fn != "__init__.py":
        modname = fn[:-3]
        mod = importlib.import_module("." + modname, __package__)
        savers[mod.name] = mod.method

__all__ = ["savers"]
