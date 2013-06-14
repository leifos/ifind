def check(var, types):
    if not isinstance(var, types):
        raise TypeError('%s not %s' % (var, types))
