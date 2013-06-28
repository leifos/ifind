import imp
import ifind.search.engines as engines


def Engine(engine_string, **kwargs):
    return get_class(engine_string, **kwargs)


def get_class(engine_string, **kwargs):

    module = imp.load_source("dummy", '/home/strings/code/ifind/ifind/search/engines/bing.py')
    test = getattr(module, engine_string.lower().title())

    return getattr(module, "Bing")(**kwargs)
