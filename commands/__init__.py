import os
import importlib
import __builtin__
builtins = __builtin__

here = os.path.dirname(__file__)
__all__ = []

builtins.commands = []
for fn in os.listdir(here):
    if fn.endswith(".py") and fn != "__init__.py":
        modname = fn[:-3]
        mod = importlib.import_module("." + modname, __package__)
        __all__.append(modname)
        builtins.commands.append(mod.method)

