import imp
import ifind.search.engines as engines


def Engine(engine_string, **kwargs):
    return get_class(engine_string, **kwargs)


def get_class(engine_string, **kwargs):

    module_path = engines.__path__[0] + '/' + engine_string.lower() + '.py'
    module = imp.load_source('pass', module_path)

    return getattr(module, engine_string.lower().title())(**kwargs)
